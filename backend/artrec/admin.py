from django.contrib import admin

# Import the models
from .models import Artwork
from .models import UserProfile
from .models import HistoryLine

# Define list views for the models
class ArtworkAdmin(admin.ModelAdmin):
    list_display = ('id', 'recommenderArtId', 'filename', 'artist', 'humanGenerated')


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'recommenderUserId', 'user', 'humanArtLiked', 'computerArtLiked')


class HistoryLineAdmin(admin.ModelAdmin):
    list_display = ('id', 'artwork', 'user', 'status', 'weight', 'updated')


# Register the models
admin.site.register(Artwork, ArtworkAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(HistoryLine, HistoryLineAdmin)