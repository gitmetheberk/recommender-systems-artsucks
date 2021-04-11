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

# Authentication imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Database API views
class ArtworkView(viewsets.ModelViewSet):
    permission_classes = (None)
    serializer_class = ArtworkSerializer
    queryset = Artwork.objects.all()

class UserProfileView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()

class HistoryLineView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = HistoryLineSerializer
    queryset = HistoryLine.objects.all()
