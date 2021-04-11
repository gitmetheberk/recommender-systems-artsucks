from django.db import models
from django.contrib.auth.models import User

# Authentication imports
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.core.signals import request_finished
from django.dispatch import receiver

# Create your models here.
# One entry for every piece of art in our database
class Artwork(models.Model):
    # id
    filename = models.CharField(max_length=200)  # Ex. Eugene_Delacroix_7.jpg
    artist = models.CharField(max_length=200)  # Ex. Eugene Delacroix

    # Will be used later when determining a user's computer/human generated art score ()
    humanGenerated = models.BooleanField()
    

# One entry for every user, creating a new user should create a new UserProfile
class UserProfile(models.Model):
    # Manually defined internalUserId to prevent any issues related to the ratings matrix/feature vectors
    internalUserId = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Will be used later when determining a user's computer/human generated art score ()
    humanArtLiked = models.IntegerField(default=0)
    computerArtLiked = models.IntegerField(default=0)


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
        Token.objects.create(user=instance)
        UserProfile(user=instance).save()