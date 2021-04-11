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

# Database API views
class ArtworkView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ArtworkSerializer
    queryset = Artwork.objects.all()

class UserProfileView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()

class HistoryLineView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
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

        # Randomly get an art for the user
        num_arts = 6
        art = randint(1,6) % num_arts + 1
        queryset = Artwork.objects.get(pk=art)
        return Response(ArtworkSerializer(queryset).data)

class GetRecentHistory(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)

    # Returns the 10 most recent history entries for the user
    def list(self, request):
        # Resolve user profile then get the 10 more recent history lines
        userprofile = resolveuserfromrequest(request)[1]
        last_ten = HistoryLine.objects.filter(user=userprofile).order_by('-id')[:10]
        serialized = {}
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
