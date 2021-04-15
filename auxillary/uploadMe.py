# Helper script:
# Used to create a list of artist names and file names for the
# best artworks of all time dataset to be used by
# createArt.py to create the art records in the server

import os

information = {}

for directory in os.listdir():
    if directory == "uploadMe.py":
        continue
    files = []
    for count, filename in enumerate(os.listdir(directory)):
        files.append(filename)

    information[directory.replace('_', ' ')] = files

output = open("output.txt", "w+")
for artist in information.keys():
    for file in information[artist]:
        output.write(artist + "," + file + "\n")

output.close()