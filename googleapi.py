import os
import requests
import json

import googleapiclient.discovery

def getdata():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyB5HOyipuWNrwSZy1n1CHvR4sTsJoe0gRA"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    request = youtube.videos().list(
        part="snippet",
        id="puJVkAxr0l8"
    )
    response = request.execute()
    song_name = response.get('title')
    artist = response.get('channelTitle')

    print(f"{song_name} {artist}")

if __name__ == "__main__":
    getdata()