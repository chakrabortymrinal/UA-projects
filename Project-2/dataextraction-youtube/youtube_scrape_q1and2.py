import googleapiclient.discovery
from googleapiclient.errors import HttpError
import configparser
import pandas as pd

# DO NOT COMMIT 'youtube_api_key' in secrets file, add to .gitignore
config = configparser.ConfigParser()
config.read('secrets.ini')
api_service_name = "youtube"
api_version = "v3"
api_key = config['settings']['youtube_api_key']

# init youTube client
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=api_key
)

# search videos def with region code and results as params
def search_videos(query, region_code='US', max_results=50):
    try:
        request = youtube.search().list(
            part="id",
            type='video',
            q=query,
            regionCode=region_code,
            maxResults=max_results
        )
        response = request.execute()
        video_ids = [item['id']['videoId'] for item in response['items']]
        return video_ids
    except HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred: {e.content}")
        return []

# get stats of the id's returned and return dataframe
def get_video_details(video_ids):
    try:
        request = youtube.videos().list(
            part='snippet,statistics',
            id=','.join(video_ids)
        )
        response = request.execute()

        video_details = []
        for item in response['items']:
            video_id = item['id']
            snippet =item['snippet']
            title = item['snippet']['title']
            views = item['statistics'].get('viewCount', 0)
            likes = item['statistics'].get('likeCount', 0)
            comments = item['statistics'].get('commentCount', 0)

            video_details.append({
                'video_id': video_id,
                'title': title,
                # 'snippet':snippet,
                'views': views,
                'likes': likes,
                'comments': comments
            })

        return pd.DataFrame(video_details)
    except HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred: {e.content}")
        return []

# combined function to get the required details
def cq_get_videos_details (query, region_code='US', max_results=50):
    video_ids = search_videos(query, region_code, max_results)
    return get_video_details(video_ids)


# pass params and save to csv
query = "good bad and the ugly"
video_details_df = cq_get_videos_details(query)
print(video_details_df)
video_details_df.to_csv('youTube.csv',index=False)