import pandas as pd

file='all_jobs_glassdoor.csv'

df=pd.read_csv(file)

# print(df.info())

final_df=df[['title','company','location','date_posted','salary_source','interval','min_amount','max_amount','currency','is_remote','listing_type']]

print(final_df.info())
print(final_df.head(10))