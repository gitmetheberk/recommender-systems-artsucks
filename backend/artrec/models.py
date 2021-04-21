from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

# Authentication imports
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.core.signals import request_finished
from django.dispatch import receiver

# Other imports
import numpy as np

# PERFORMANCE PROFILING
import timeit

# Create your models here.
# One entry for every piece of art in our database
class Artwork(models.Model):
    # id
    recommenderArtId = models.IntegerField(blank=True, null=True, unique=True)  # Used internally by the recommender
    filename = models.CharField(max_length=200)  # Ex. Eugene_Delacroix_7.jpg
    artist = models.CharField(max_length=200)  # Ex. Eugene Delacroix


    # Will be used later when determining a user's computer/human generated art score ()
    humanGenerated = models.BooleanField()

    # Track features for this piece of art
    features = models.JSONField(default=list)

# One entry for every user, creating a new user should create a new UserProfile
class UserProfile(models.Model):
    id = models.BigAutoField(primary_key=True)

    # This value will help us locate this user in the ratings matrix and will be hardcoded at the time of calculations, etc.
    recommenderUserId = models.IntegerField(blank=True, null=True, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Will be used later when determining a user's computer/human generated art score ()
    humanArtLiked = models.IntegerField(default=0)
    computerArtLiked = models.IntegerField(default=0)

    # Track the user's feature profile
    feature_profile = models.JSONField(default=list)

    # Track the user's current art queue
    queue8 = models.IntegerField(default=-1)
    queue7 = models.IntegerField(default=-1)
    queue6 = models.IntegerField(default=-1)
    queue5 = models.IntegerField(default=-1)
    queue4 = models.IntegerField(default=-1)
    queue3 = models.IntegerField(default=-1)
    queue2 = models.IntegerField(default=-1)
    queue1 = models.IntegerField(default=-1)
    queue0 = models.IntegerField(default=-1)

    # Note: There is a strong liklihood this turns out to be a very bad idea
    # JSONField to track individual sums for each feature (just go with it)
    feature_occurrences = models.JSONField(default=list)



# One entry for every user interaction, a like or a dislike
class HistoryLine(models.Model):
    # Setup foreign key for the Artwork
    artwork = models.ForeignKey("Artwork", on_delete=models.PROTECT)

    # Setup foreign key for the UserProfile
    user = models.ForeignKey("UserProfile", on_delete=models.CASCADE)
    
    # Define choices to be used in validation of status
    LIKE = 'L'
    DISLIKE = 'D'
    NOT_SEEN = 'N'
    CHOICES = [
        (LIKE, "Like"),
        (DISLIKE, "Dislike"),
        (NOT_SEEN, "Not viewed")
    ]

    status = models.CharField(
        max_length=1,
        choices=CHOICES,
        default=NOT_SEEN
    )

    # Potentially used later to assign weights based on how long ago this history line was created
    weight = models.SmallIntegerField(default=None, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)

# When a new user is created, create an AUTH token & user profile
@receiver(post_save, sender=User)
def new_user(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)  # Create a new token
        UserProfile(user=instance).save()  # Create a new userProfile
        instance.groups.add(Group.objects.get(name="uncultured_student"))  # Set default group


# Triggers after save of a new historyLine from a post request
@receiver(post_save, sender=HistoryLine)
def new_history(sender, instance=None, created=False, **kwargs):
    if created:
        start = timeit.default_timer()

        # If the user liked the art, add the tally and add to their feature profile
        if instance.status == "L":
            if instance.artwork.humanGenerated:
                instance.user.humanArtLiked += 1
            else:
                instance.user.computerArtLiked += 1

            # If this is the user's first art, it is their entire profile
            if not instance.user.feature_profile:
                instance.user.feature_profile = instance.artwork.features

                # Initalize zero vector for occurrences
                instance.user.feature_occurrences = [0] * 2048
            else:
                # Add the image's features to this user's feature set
                instance.user.feature_profile = [sum(i) for i in zip(instance.user.feature_profile, instance.artwork.features)]

            # Implement: A very bad idea
            # Only add to individual sums if the artwork in question has some value for that feature
            instance.user.feature_occurrences = (np.where(np.asarray(instance.artwork.features)>0,1,0) + np.asarray(instance.user.feature_occurrences)).tolist()


            # To avoid race conditions, only update needed fields
            instance.user.save(update_fields=["feature_profile", "humanArtLiked", "computerArtLiked", "feature_occurrences"])
            print("user.feature_profile update took {} seconds".format((timeit.default_timer() - start)))
