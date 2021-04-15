# Helper script:
# Makes a series of post requests (at most 10 concurrently)
# to the server to create new pieces of art from a file generated
# by uploadMe.py

import requests
from multiprocessing.dummy import Pool

# Sources: https://stackoverflow.com/questions/27021440/python-requests-dont-wait-for-request-to-finish

pool = Pool(10)

token = "[REDACTED]"
url = "http://104.236.113.146:8000/api/artworks/"

def makeArt(artist, file, id):
    headers = {"Authorization": "token " + token}
    payload = {
        "recommenderArtId": id,
        "filename": file,
        "artist": artist,
        "humanGenerated": True
    }
    requests.post(url, headers=headers, data=payload)



futures = []

art = open("output.txt", 'r')
count = 0
for line in art.readlines():
    line = line.replace('\n', '')
    artist, file = line.split(',')

    futures.append(pool.apply_async(makeArt, [artist, file, count]))

    print(count)
    count += 1
    

for future in futures:
    print(future.get())