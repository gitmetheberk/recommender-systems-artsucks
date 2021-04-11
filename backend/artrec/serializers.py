from rest_framework import serializers

# Import the models
from .models import Artwork
from .models import UserProfile
from .models import HistoryLine

class ArtworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artwork
        fields = ('id', 'filename', 'artist', 'humanGenerated')

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('internalUserId', 'user', 'humanArtLiked', 'computerArtLiked')

class HistoryLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoryLine
        fields = ('artwork', 'user', 'status', 'weight', 'updated')