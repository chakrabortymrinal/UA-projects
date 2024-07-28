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


def like_vs_view_ratio (top10_video_df):
  
    # top10_video_df.loc['likes']=pd.to_numeric(top10_video_df['likes'])
    # top10_video_df.loc['views']=pd.to_numeric(top10_video_df['views'])

    total_likes=top10_video_df['likes'].sum()
    total_views=top10_video_df['views'].sum()

    ratio =total_likes/total_views

    
    top10_video_df['ratio']=top10_video_df['likes'] / top10_video_df['views']


    return top10_video_df , ratio


ratio_df, ratio =like_vs_view_ratio(top10_videos_df)
print("ratio per row of like v/s views: ")
print(ratio_df)
print ('===============================')
print ('Total ratio of top 10 like v/s views')
print(ratio)