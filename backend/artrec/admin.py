# Django imports
from django.contrib import admin
from django.shortcuts import redirect

# Import the models
from .models import Artwork
from .models import UserProfile
from .models import HistoryLine

# Other imports
import time
import numpy as np
from sklearn.model_selection import train_test_split

# Define list views for the models
class ArtworkAdmin(admin.ModelAdmin):
    list_display = ('recommenderArtId', 'filename', 'artist', 'humanGenerated')


# Used to generate reports for the userprofiles in the queryset
def UserProfile_generateReports(modeladmin, request, queryset):
    # Open the report file for writing
    filepath = "static/reports/" + "report_" + time.strftime("%Y%m%d-%H%M%S") + ".txt"
    file = open(filepath, 'x')

    # Loop through each profile in the queryset
    for profile in queryset:
        file.write("BEGIN REPORT FOR USER: {}\n".format(profile.user.username))

        # Get all historyLine information for the user
        history = HistoryLine.objects.filter(user=profile).order_by('updated')
        history_count = history.count()
        history_likes = HistoryLine.objects.filter(user=profile, status='L').count()
        history_dislikes = HistoryLine.objects.filter(user=profile, status='D').count()
        file.write("Total HistoryLines: {}\nTotal Likes:        {}\nTotal Dislikes:     {}\n\n"
                  .format(history_count, history_likes, history_dislikes))

        # If this user doesn't have enough likes/total ratings skip
        if history_count < 25 or history_likes < 15:
            file.write("Report generation aborted due to low interactions\n\n")
            file.write("-----------------------\n")
            continue

        # Load all user history into a list for ease of use where 1 = L and 0 = D
        histArr = []
        processed = False
        likeCount = 0
        for line in history:
            # Process out the randomly generated interactions from the beginning of the user's history
            if not processed:
                if line.status == 'L':
                    likeCount += 1
                    if likeCount == 20:
                        processed = True
                
            # Processing complete, proceed normally
            else:
                histArr.append(1 if line.status == 'L' else 0)
        
        # Print updated information following removal of random items
        file.write("Recommended history: {}\nTotal Likes:         {}\nTotal Dislikes:      {}\n\n"
                  .format(len(histArr), np.sum(histArr), len(histArr) - np.sum(histArr)))

        # List of splits to use for metrics (In percent to evaluate vs. history)
        splits = (0.5, 0.33, 0.25)
        for split in splits:
            # Split the history into a recent piece and a new piece
            hist, new = train_test_split(histArr, shuffle=False, test_size=split)
            
            # DEBUGGING
            # print(hist,end="")
            # print(new)
            # print(histArr)
            # print("you got lucky")


            # Sum likes against total
            hist_likes = np.sum(hist)
            new_likes = np.sum(new)

            # Calculate the ratios
            hist_ratio = hist_likes / len(hist)
            new_ratio = new_likes / len(new)
            percentChange = ((new_ratio / hist_ratio) - 1) * 100

            # Write the results (in a very inefficient manner since the multi-line string didn't want to cooperate)
            file.write("Evaluating performance of most recent interactions ({1:}/{0:})\n".format(round(split*100), 100-round(split*100)))
            file.write("    Historical data | Newest Data\n")
            file.write("Num. Likes: {0:<5}   | {1:<5}  \n".format(hist_likes, new_likes))
            file.write("% Liked:    {0:<5} % | {1:<5} %\n".format(round(hist_ratio * 100, 2),round(new_ratio * 100, 2)))
            file.write("Change in newer data: {} %\n".format(round(percentChange, 2)))
            file.write("STATUS: {}\n\n".format("IMPROVED" if percentChange > 0 else ("WORSE" if percentChange < 0 else "NO CHANGE")))

        file.write("-----------------------\n")

    print("REPORT GENERATED: {}".format(filepath))
    print("It can be accessed at 104.236.113.146:8000/{}".format(filepath))
    file.close()

    # Direct to the new report
    return redirect('/{}'.format(filepath))

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
