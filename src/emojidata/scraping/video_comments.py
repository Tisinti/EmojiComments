import googleapiclient.discovery
import googleapiclient.errors
from dotenv import load_dotenv
import os
import advertools as adv

load_dotenv()

API_KEY: str = os.getenv('YT_API')
api_service_name: str = "youtube"
api_version: str = "v3"


def get_comments(videoID: str) -> list[str]:
    comments = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=API_KEY)

    request = comments.commentThreads().list(
        part="snippet",
        videoId=videoID,
        maxResults=100
    )
    response = request.execute()

    return [item['snippet']['topLevelComment']['snippet']['textDisplay']
            for item in response['items']]


def get_emoji_comments(comments: list[str]) -> list[str]:
    return [comment for comment in comments
            if adv.extract_emoji([comment])['overview']['num_emoji'] > 0]
