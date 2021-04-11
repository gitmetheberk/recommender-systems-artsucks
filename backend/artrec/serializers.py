from rest_framework import serializers

# Import the models
from .models import Artwork
from .models import UserProfile
from .models import HistoryLine
from .models import User

class ArtworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artwork
        fields = ('id', 'filename', 'artist', 'humanGenerated')

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'recommenderUserId', 'user', 'humanArtLiked', 'computerArtLiked')

class HistoryLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoryLine
        read_only_fields = ('user',)
        fields = ('artwork', 'user', 'status', 'weight', 'updated')


# Used in new account creation
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user