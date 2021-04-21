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
import recommender
import numpy as np
import copy
from scipy.spatial.distance import cosine

# PROFILING
import timeit

# Configuration
import sys
np.set_printoptions(threshold=sys.maxsize)
np.seterr(divide='ignore', invalid='ignore') # Always good practice to ignore errors, right?


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

    # TODO: This function is where the recommender should return the next piece of art to show
    # to the user. The function expects only the auth token in and, after verifying which user
    # the token belongs to, this is the function which should then return the next piece of art
    # Right now it's only returning a random piece of art, but all you have to do recommender-wise is
    # Set the value of 'art' to the ID of the piece of art we want to recommend
    # The userprofile object has a field 'recommenderUserId' which needs to be set on first processing
    # for the user, and is manually controlled
    def list(self, request):
        # Grabs the user object and the userprofile object from the auth token to be used later
        user, userprofile = resolveuserfromrequest(request)

        # This will probably be what we want to do
        #  art = recommender.recommendArt(user, userprofile)
        art = 0
        
        # Randomly get an art for the user if they've liked < 15 arts
        # (Set to 14 due to ASYNC nonsense)
        history = HistoryLine.objects.filter(user=userprofile, status='L')
        if len(history) < 14:
            # TODO: The upper bound should be found programatically
            # Generate random arts until we find one the user hasn't seen yet
            art = randint(0,6923)
            while HistoryLine.objects.filter(user=userprofile, artwork=Artwork.objects.get(recommenderArtId=art)).exists():
                art = randint(0,6923)
        
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

            # Find user's average profile
            profile = userprofile.feature_profile
            profile = np.asarray(profile)
            profile = profile / np.asarray(userprofile.feature_occurrences)
            np.nan_to_num(profile, copy=False)
            print("PROFILE AVERAGE: {}".format(np.average(profile)))
            #print("PROFILE:")
            #print(profile)
        
           # Get distances between user_profile and each piece of art
            distances = []
            for artId in range(6924):
                # Euclidean, using the feature_occurrences
                #distances.append(np.linalg.norm(profile - np.asarray(Artwork.objects.get(recommenderArtId=artId).features)))

                # Breakout for debugging
                #artfeatures = np.asarray(Artwork.objects.get(recommenderArtId=artId).features)
                #result = profile-artfeatures
                #np.nan_to_num(result, copy=False)
                #linalg = np.linalg.norm(result)
                #print("Profile: {}\nArtwork features: {}\nResult: {}\nLinalg: {}".format("", "", "result", linalg))
                #print("Is NORM Nan? {}".format("Yes" if np.isnan(linalg) else "no"))

                #distances.append(linalg)
                artfeatures = np.asarray(Artwork.objects.get(recommenderArtId=artId).features)
                distances.append(cosine(profile, artfeatures))
                #print(distances[-1])





                #print("ART:{}, DISTANCE:{} | ".format(artId, distances[-1]), end="")
                #print("PROGRESS: {}".format(artId))

            # Collect the art IDs of the closest art's to the user's profile (sort smallest to largest)
            #print(distances)
            closest_sorted = np.asarray(distances).argsort()
            
            print("Closest, front: {}".format(distances[closest_sorted[0]]))
            print("Closest, back:  {}".format(distances[closest_sorted[-1]]))

            # Debugging
            #print("Distance max: {}".format(max(distances)))
            #print("Distance min: {}".format(min(distances)))

            # Find 10 arts the user hasn't seen which are most similar to their current profile
            artQueue = []
            for artId in closest_sorted:
                # Get the art object from the art id
                art_object = Artwork.objects.get(recommenderArtId=artId)
                if not HistoryLine.objects.filter(user=userprofile, artwork=art_object).exists():
                    artQueue.append(int(artId))
                    if len(artQueue) == 10:
                        break

            # Take the most-similar art and queue the rest
            art = artQueue.pop(0)

            userprofile.queue8 = artQueue.pop(0)
            userprofile.queue7 = artQueue.pop(0)
            userprofile.queue6 = artQueue.pop(0)
            userprofile.queue5 = artQueue.pop(0)
            userprofile.queue4 = artQueue.pop(0)
            userprofile.queue3 = artQueue.pop(0)
            userprofile.queue2 = artQueue.pop(0)
            userprofile.queue1 = artQueue.pop(0)
            userprofile.queue0 = artQueue.pop(0)

            userprofile.save(update_fields=["queue8", "queue7", "queue6", "queue5", "queue4", "queue3", "queue2", "queue1", "queue0"])
            
            # PROFILING
            print("Recommended 10 arts in {} seconds".format((timeit.default_timer() - start)))

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
