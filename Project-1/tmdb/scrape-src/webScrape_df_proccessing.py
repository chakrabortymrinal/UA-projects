import pandas as pd

files = ["tmdb-1.csv", "tmdb-2.csv", "tmdb-3.csv", "tmdb-4.csv"]
dfs = [pd.read_csv(file) for file in files]
final_df=pd.concat(dfs,ignore_index=False)
# print 
print(final_df)