# Django imports
from django.shortcuts import render
from django.http import JsonResponse

# Import the serialziers
from .serializers import ArtworkSerializer
from .serializers import UserProfileSerializer
from .serializers import HistoryLineSerializer
from .serializers import UserSerializer

# Import the models
from .models import Artwork
from .models import UserProfile
from .models import HistoryLine
from .models import User

# Rest imports
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token

# Functional API imports
from random import randint
import numpy as np
import copy
from scipy.spatial.distance import cosine

# PROFILING
import timeit

# Configuration
import sys
np.set_printoptions(threshold=sys.maxsize)


# Database API views
class ArtworkView(viewsets.ModelViewSet):
#    permission_classes = (IsAuthenticated,)
    serializer_class = ArtworkSerializer
    queryset = Artwork.objects.all()

class UserProfileView(viewsets.ModelViewSet):
#    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()

class HistoryLineView(viewsets.ModelViewSet):
#    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,) 
    serializer_class = HistoryLineSerializer
    queryset = HistoryLine.objects.all()

    # Override create so the userId is set based on the user's token
    def perform_create(self, serializer):
        userprofile = resolveuserfromrequest(self.request)[1]
        serializer.save(user=userprofile)

# Advanced/functional APIs
class GetNewArt(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)

    # This function contains the recommender engine
    def list(self, request):
        # Configure numpy to ignore some warnings
        np.seterr(divide='ignore', invalid='ignore')  # As far as I can tell, this doesn't work, but I can't explain it

        # Grabs the user object and the userprofile object from the auth token to be used later
        user, userprofile = resolveuserfromrequest(request)

        # This will probably be what we want to do
        #  art = recommender.recommendArt(user, userprofile)
        art = 0
        
        # Randomly get an art for the user if they've liked < 20 arts
        history = HistoryLine.objects.filter(user=userprofile, status='L')
        if len(history) < 20:
            # TODO: The upper bound should be found programatically
            # FIXME: This upper bound needs to be updated following database reformatting with new features
            # Generate random arts until we find one the user hasn't seen yet
            art = randint(0,6661)

            # FIXME: This doesn't appear to be working as expected
            while HistoryLine.objects.filter(user=userprofile, artwork=Artwork.objects.get(recommenderArtId=art)).exists():
                art = randint(0,6661)
        
        elif userprofile.queue0 != -1:
            # Return an art from the queue
            # The reason we're using individual queue objects is not a good reason, but I can't be bothered to change it back since it still works
            if userprofile.queue8 != -1:
                art = userprofile.queue8
                userprofile.queue8 = -1
                userprofile.save(update_fields=["queue8"])
            elif userprofile.queue7 != -1:
                art = userprofile.queue7
                userprofile.queue7 = -1
                userprofile.save(update_fields=["queue7"])
            elif userprofile.queue6 != -1:
                art = userprofile.queue6
                userprofile.queue6 = -1
                userprofile.save(update_fields=["queue6"])
            elif userprofile.queue5 != -1:
                art = userprofile.queue5
                userprofile.queue5 = -1
                userprofile.save(update_fields=["queue5"])
            elif userprofile.queue4 != -1:
                art = userprofile.queue4
                userprofile.queue4 = -1
                userprofile.save(update_fields=["queue4"])
            elif userprofile.queue3 != -1:
                art = userprofile.queue3
                userprofile.queue3 = -1
                userprofile.save(update_fields=["queue3"])
            elif userprofile.queue2 != -1:
                art = userprofile.queue2
                userprofile.queue2 = -1
                userprofile.save(update_fields=["queue2"])
            elif userprofile.queue1 != -1:
                art = userprofile.queue1
                userprofile.queue1 = -1
                userprofile.save(update_fields=["queue1"])
            else:
                art = userprofile.queue0
                userprofile.queue0 = -1
                userprofile.save(update_fields=["queue0"])

        else:
            start = timeit.default_timer()
            print("BEGIN PROCESSING RECOMMENDATIONS for {}".format(user.username))
            
            # Find user's average profile
            profile = userprofile.feature_profile
            profile = np.asarray(profile)
            profile = profile / np.asarray(userprofile.feature_occurrences)
            np.nan_to_num(profile, copy=False)

            # Find the 1000 most "important" features for this user
            # (Aka find the 1000 features which have appeared the most in art's the user liked)
            mostImportant = np.asarray(userprofile.feature_occurrences).argsort()[::-1][:1000]

             # Get distances between user_profile and each piece of art
            num_features = []  # This is purely used for profiling/debugging
            distances = []
            for artId in range(6662):
                # Option Z:
                # Euclidean, using the feature_occurrences
                # distances.append(np.linalg.norm(profile - np.asarray(Artwork.objects.get(recommenderArtId=artId).features)))
                


                # Grab the features for the artwork
                artfeatures = np.asarray(Artwork.objects.get(recommenderArtId=artId).features)
                
                # Create an array detailing which features are non-zero
                validArtFeatures = np.where(artfeatures > 0)


                # Option A: Don't use the "mostImportant" features
                # Find the intersection of the user's most important features and this art's non-zero features
                # featuresToCheck = validArtFeatures#np.intersect1d(validArtFeatures, mostImportant)
                # num_features.append(len(validArtFeatures[0]))
                

                # Option B: Use only the "mostImportant" features
                # Find the intersection of the user's most important features and this art's non-zero features
                featuresToCheck = np.intersect1d(validArtFeatures, mostImportant)
                num_features.append(featuresToCheck.shape[0])

                # Option A2: Use the cosine distance
                # Append the cosine distance between the featuresTocheck for this user and this art
                distances.append(cosine(profile[featuresToCheck], artfeatures[featuresToCheck]))
                
                
                # Option B2: Use the euclidean distance
                # Append the euclidean distance between the featuresToCheck for this user and this art
                # distances.append(np.linalg.norm(profile[featuresToCheck] - artfeatures[featuresToCheck]))
                

            # Collect the art IDs of the closest art's to the user's profile (sort smallest to largest)
            #print(distances)
            closest_sorted = np.asarray(distances).argsort()
            
            # Print some information about the calculations which just took place
            print("Average user profile feature value: {}".format(round(np.average(profile), 5)))
            print("Average features used: {}".format(round(np.sum(num_features)/len(distances))))
            print("Max features used: {}, Min features used: {}".format(max(num_features), min(num_features)))
            print("Distance max: {}, Distance min: {}".format(round(distances[closest_sorted[-1]], 2), round(distances[closest_sorted[0]], 2)))

            # Find 10 arts the user hasn't seen which are most similar to their current profile
            already_seen = 0  # This variable is used purely for debugging
            artQueue = []
            for artId in closest_sorted:
                # Get the art object from the art id
                art_object = Artwork.objects.get(recommenderArtId=artId)
                if not HistoryLine.objects.filter(user=userprofile, artwork=art_object).exists():
                    artQueue.append(int(artId))
                    if len(artQueue) == 10:
                        break
                else:
                    already_seen += 1

            # Take the most-similar art and queue the rest
            art = artQueue.pop(0)

            userprofile.queue8 = artQueue.pop(0)
            userprofile.queue7 = artQueue.pop(0)
            userprofile.queue6 = artQueue.pop(0)
            userprofile.queue5 = artQueue.pop(0)
            userprofile.queue4 = artQueue.pop(0)
            userprofile.queue3 = artQueue.pop(0)

            # TODO: Implement a random art for this queue slot to produce serendipity
            userprofile.queue2 = artQueue.pop(0)
            
            userprofile.queue1 = artQueue.pop(0)
            userprofile.queue0 = artQueue.pop(0)

            # Update the user profile queue fields
            userprofile.save(update_fields=["queue8", "queue7", "queue6", "queue5", "queue4", "queue3", "queue2", "queue1", "queue0"])
            
            # Logging
            print("Ignored {} arts already seen by the user".format(already_seen))
            print("FINISH PROCESSING RECOMMENDATIONS for {}, processed in {} seconds".format(user.username, round((timeit.default_timer() - start), 1)))

        queryset = Artwork.objects.get(recommenderArtId=art)
        return Response(ArtworkSerializer(queryset).data)

class GetRecentHistory(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)

    # Returns the 10 most recent history entries for the user
    def list(self, request):
        # Resolve user profile then get the 10 more recent history lines
        userprofile = resolveuserfromrequest(request)[1]
        last_ten = HistoryLine.objects.filter(user=userprofile).order_by('-id')[:10]
        serialized = {}
        # TODO: Loop through queryset not iterate over length
        for i in range(len(last_ten)):
            serialized_line = HistoryLineSerializer(last_ten[i]).data

            # Get the art and extract artist & computer generated
            art = Artwork.objects.get(pk=last_ten[i].artwork.id)
            serialized_line['artist'] = art.artist
            serialized_line['humangenerated'] = art.humanGenerated

            serialized.update({i : serialized_line})

        return Response(serialized)


# AUTH functions
class UserCreate(generics.CreateAPIView):
    permission_classes = (AllowAny, )
    queryset = User.objects.all()
    serializer_class = UserSerializer

# AUTH resolver, returns (user, userProfile) from an http request with an auth token
def resolveuserfromrequest(request):
    token = request.headers['Authorization'].replace('token ', '')
    user = Token.objects.get(key=token).user
    return (user, UserProfile.objects.get(user=user))
