# Helper script:
# Makes a series of post requests (at most 10 concurrently)
# to the server to add art and art features

import requests
import re
import csv

# Sources: https://stackoverflow.com/questions/27021440/python-requests-dont-wait-for-request-to-finish

output = open('output.csv', 'a')

def makeArt(artist, file, id, features):
    output.write(str(id) + "\t" + str(id) + "\t" + file + "\t" + artist + "\t" + "1" + '\t' + str(features) + '\n')

art = open("labels.txt", 'r')
csvfile = open("features.csv", 'r')
csvdata = csv.reader(csvfile, delimiter=',')

data = []
for line in csvdata:
    if line[0] == '':
        continue
    else:
        workingList = []
        for obj in line:
            workingList.append(float(obj))
        data.append(workingList)

print("CSV processing complete")

count = 0
for line in art.readlines():
    filename = line.replace('\n','')

    artist = line.replace('_', ' ')
    artist = re.sub(r'[0-9]*\.jpg\n', '',artist)[:-1]

    features = data[count] 

    makeArt(artist, filename, count, features)

    print(count)
    count += 1

art.close()
csvfile.close()
output.close()