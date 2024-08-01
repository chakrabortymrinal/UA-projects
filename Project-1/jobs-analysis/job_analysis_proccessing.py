import pandas as pd
import glob
import csv
# import matplotlib.pyplot as plt
# import seaborn as sns
# from pandas_profiling import ProfileReport
# from IPython.display import display
csv_files = glob.glob('jobs-glassdoor-*.csv')
all_jobs_df = pd.DataFrame()

for file in csv_files:
    jobs_df = pd.read_csv(file)
    all_jobs_df = pd.concat([all_jobs_df, jobs_df], ignore_index=True)

# Now all_jobs_df contains data from all matching CSV files
print(f"Total jobs found: {len(all_jobs_df)}")

# Optional: Save the consolidated DataFrame to a new CSV file
all_jobs_df.to_csv('all_jobs_glassdoor.csv', index=False, quoting=csv.QUOTE_NONNUMERIC, escapechar="\\")