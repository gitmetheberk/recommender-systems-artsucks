from django.contrib import admin

# Import the models
from .models import Artwork
from .models import UserProfile
from .models import HistoryLine

# Other imports
import time

# Define list views for the models
class ArtworkAdmin(admin.ModelAdmin):
    list_display = ('recommenderArtId', 'filename', 'artist', 'humanGenerated')


# Used to generate reports for the userprofiles in the queryset
def UserProfile_generateReports(modeladmin, request, queryset):
    print("I generated a report (believe me (it happened (definitely)))")

    # Open the report file for writing
    filepath = "static/reports/" + "report_" + time.strftime("%Y%m%d-%H%M%S") + ".txt"
    file = open(filepath, 'x')

    # Loop through each profile in the queryset
    for profile in queryset:
        file.write("BEGIN REPORT FOR USER: {}\n".format(profile.user.username))

        # Get all historyLine information for the user
        history = HistoryLine.objects.filter(user=profile)
        history_count = history.count()
        history_likes = HistoryLine.objects.filter(user=profile, status='L').count()
        history_dislikes = HistoryLine.objects.filter(user=profile, status='D').count()
        file.write("Total HistoryLines: {}\nTotal Likes:        {}\nTotal Dislikes:     {}\n\n"
                  .format(history_count, history_likes, history_dislikes))

        # TODO: Some complex stuff needs to happen here to implement the metrics




        file.write("-----------------------\n")

    print("REPORT GENERATED: {}".format(filepath))
    print("It can be accessed at 104.236.113.146:8000/{}".format(filepath))
    file.close()

UserProfile_generateReports.short_description = "Generate report"


class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
            'id', 
            'recommenderUserId', 
            'user', 
            'humanArtLiked', 
            'computerArtLiked'
    )

    readonly_fields = (
    'id',
    'user',
    'humanArtLiked',
    'computerArtLiked',
    'feature_profile',
    'feature_occurrences'
    )

    actions = [UserProfile_generateReports, ]    


class HistoryLineAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'weight', 'updated')
    raw_id_fields = ('artwork','user',)


# Register the models
admin.site.register(Artwork, ArtworkAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(HistoryLine, HistoryLineAdmin)
