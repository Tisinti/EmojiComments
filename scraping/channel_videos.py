import googleapiclient.discovery
import googleapiclient.errors
from dotenv import load_dotenv
from .video_comments import get_comments, get_emoji_comments
import os

load_dotenv()

API_KEY: str = os.getenv('YT_API')
api_service_name: str = "youtube"
api_version: str = "v3"


def search_channels(find: str) -> str:
    search = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=API_KEY)

    request = search.search().list(
        part='snippet',
        type='video',
        q=find,
        relevanceLanguage = 'en',
        regionCode = 'US',
        maxResults=50
    )

    response = request.execute()
    print(response)
    channel_ids = [item['snippet']['channelId'] for item in response['items']]

    return list(set(channel_ids))


def get_channel_vid(channel_id: str) -> list[str]:
    channel = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=API_KEY)

    request = channel.search().list(
        part="snippet",
        channelId=channel_id,
        type='video',
        order='viewCount',
        maxResults=50
    )
    response = request.execute()

    vidIds = [item['id']['videoId'] for item in response['items']]

    return vidIds


def search_comments(search: str) -> dict[str, str]:
    channels = search_channels(search)

    vidIDs = []
    emoji_comments = []

    for channel in channels:
        vidIDs.extend(get_channel_vid(channel_id=channel))

    for vidID in vidIDs:
        try:
            comments = get_comments(vidID)
            emoji_comments.extend(get_emoji_comments(comments))
        except Exception:
            print("Comments disabled for Video:" + vidID)

    emoji_dict = {i: comment for i, comment in enumerate(emoji_comments)}
    return emoji_dict
