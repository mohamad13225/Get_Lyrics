import os
import requests
import json
import re
import googleapiclient.discovery

def get_youtube_video_id(url):
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(pattern, url)
    
    if match:
        return match.group(1)
    else:
        return None
    
url = "https://music.youtube.com/watch?v=WaFD7Gs75hQ"
print(get_youtube_video_id(url))
                           
def getdata(link):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "unknown" # Put YOur API Key Here

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    request = youtube.videos().list(
        part="snippet",
        id= get_youtube_video_id(link)
    )
    response = request.execute()
    channel_title = response['items'][0]['snippet']['channelTitle']
    video_title = response['items'][0]['snippet']['title']

    if " - Topic" in channel_title:
        channel_title = channel_title.replace(" - Topic", "")

    return channel_title,video_title
