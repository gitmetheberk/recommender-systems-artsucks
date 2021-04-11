from django.shortcuts import render

from rest_framework import viewsets

# Import the serialziers
from .serializers import ArtworkSerializer
from .serializers import UserProfileSerializer
from .serializers import HistoryLineSerializer

# Import the models
from .models import Artwork
from .models import UserProfile
from .models import HistoryLine

class ArtworkView(viewsets.ModelViewSet):
    serializer_class = ArtworkSerializer
    queryset = Artwork.objects.all()

class UserProfileView(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()

class HistoryLineView(viewsets.ModelViewSet):
    serializer_class = HistoryLineSerializer
    queryset = HistoryLine.objects.all()

    