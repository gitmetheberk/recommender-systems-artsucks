from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
)

# Import the serialziers
from .serializers import ArtworkSerializer
from .serializers import UserProfileSerializer
from .serializers import HistoryLineSerializer

# Import the models
from .models import Artwork
from .models import UserProfile
from .models import HistoryLine

# Authentication imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

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

# Advanced/functional APIs
class GetNewArt(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)


    # TODO: This function is where the recommender should return the next piece of art to show
    # to the user. The function expects only the auth token in and, after verifying which user
    # the token belongs to, this is the function which should then return the next piece of art
    # Right now it's only returning a random piece of art, but all you have to do recommender-wise is
    # Set the value of 'art' to the ID of the piece of art we want to recommend
    def list(self, response):
        num_arts = 6
        art = randint(1,6) % num_arts + 1

        queryset = Artwork.objects.get(pk=art)
        return Response(ArtworkSerializer(queryset).data)
