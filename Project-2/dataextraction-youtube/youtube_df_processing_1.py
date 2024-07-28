import pandas as pd

df=pd.read_csv('youTube.csv')
# print 
# print(df)

# Sort the data by top 10 comments in descending order and consider
# the video IDs and Titles of top 10 videos which have highest comments 
df['comments']=pd.to_numeric(df['comments'])
sort_by_comments_df = df.sort_values(by='comments',ascending=0)
top10_videos_df=sort_by_comments_df.head(10)

top10_videos_df=top10_videos_df.copy()
# print(sort_by_comments_df.head(10))

top_video_ids = top10_videos_df['video_id'].tolist()

print(top_video_ids)


