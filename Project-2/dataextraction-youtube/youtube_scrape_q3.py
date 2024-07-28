import googleapiclient.discovery
from googleapiclient.errors import HttpError
from pprint import pprint
import configparser
import pandas as pd
import json

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
            title = item['snippet']['title']
            # converted the collected items to int (as they were object datatype)
            # removed pd.to_numeric conversions later in the code 
            views = int(item['statistics'].get('viewCount', 0))
            likes = int(item['statistics'].get('likeCount', 0))
            comments = int(item['statistics'].get('commentCount', 0))

            video_details.append({
                'video_id': video_id,
                'title': title,
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

# get top 10 comments
def get_video_comments(video_id, max_results=10):
    try:
        request = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            maxResults=max_results,
            # textFormat='plainText'
        )
        response = request.execute()

        comments = []
        
        for item in response['items']:
            comment_data = {
                'etag': item['etag'],
                'id': item['id'],
                'kind': item['kind'],
                'comments': item['snippet']['topLevelComment']['snippet']['textDisplay']
            }
            comments.append(comment_data)
            # pprint(item)

        return comments 
    except HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred: {e.content}")
        return []



# Get to 10 comments in a decending order for the top 10 videos within the 50 videos previously got 

def get_top_comments_for_videos(query, region_code='US', max_results=50):
    # Get the top 10 comments for the top 10 videos sorted by number of comments
    video_details_df = cq_get_videos_details(query, region_code, max_results)
    
    # convert dataType of commments to numeric
    video_details_df['comments']=pd.to_numeric(video_details_df['comments'])
    # Sort by number of comments and get top 10 videos which has highest comments
    sorted_by_comments_df = video_details_df.sort_values(by='comments', ascending=0).head(10)
    
    # Retrieve top 10 videos which has highest comments
    top_video_ids = sorted_by_comments_df['video_id'].tolist()
    top_comments = {}

    for video_id in top_video_ids:
        comments = get_video_comments(video_id)
        top_comments[video_id]=comments


    # return sorted_by_comments_df, top_comments
    return top_comments




# def likeVSview_ratio (top10_video_df):
#     top10_video_df['likes']=pd.to_numeric(top10_video_df['likes'])
#     top10_video_df['views']=pd.to_numeric(top10_video_df['views'])

#     total_likes=top10_video_df['likes'].sum()
#     total_views=top10_video_df['views'].sum()

#     top10_video_df['ratio']=total_likes/total_views

#     return top10_video_df

# def likeVSview_ratio (query, region_code='US', max_results=10):
#     video_details_df = cq_get_videos_details(query, region_code, max_results)
#     # convert dataType of commments to numeric
#     video_details_df['likes']=pd.to_numeric(video_details_df['likes'])
#     video_details_df['views']=pd.to_numeric(video_details_df['views'])

#     total_likes=video_details_df['likes'].sum()
#     total_views=video_details_df['views'].sum()

#     # video_details_df['ratio']=total_likes/total_views
#     video_details_df['ratio']=total_likes/total_views

#     result_df = video_details_df[['video_id', 'title', 'ratio']]

#     return result_df


# def get_likes_vs_views_ratio(top_videos_df):
#     top_videos_df['likes_vs_views_ratio'] = top_videos_df.apply(
#         lambda row: row['likes'] / row['views'] if row['views'] > 0 else 0,
#         axis=1
#     )
#     result_df = top_videos_df[['video_id', 'title', 'likes_vs_views_ratio']]
#     return result_df



query = "good bad and the ugly"
# print(video_details_df.sort_values(by='comments',ascending=0).head(10))
# sorted_by_comments_df = video_details_df.sort_values(by='comments', ascending=0).head(10)
# top_video_ids = sorted_by_comments_df['video_id'].tolist()
# print(top_video_ids)
top_comments = get_top_comments_for_videos(query)
# top_videos_df, top_comments = get_top_comments_for_videos(query)
# print("Top Comments for Top 10 Videos:")
# pprint(top_comments)
pprint(top_comments)

# print("Top 10 Videos Sorted by Comments:")
# pprint(top_videos_df[['video_id', 'title', 'comments']])

# likes_vs_views_ratio_df = likeVSview_ratio(top_videos_df)
# print("\nLikes vs Views Ratio for Top 10 Videos:")
# pprint(likes_vs_views_ratio_df)

with open('all_video_comments.json', 'w', encoding='utf-8') as json_file:
    json.dump(top_comments, json_file, indent=4)
