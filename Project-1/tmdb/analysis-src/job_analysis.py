import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv('../tmdb-scrape/jobs.csv')
# print(df.head())
# print("Number of rows:", len(df))
# print("Number of columns:", len(df.columns))
# print("Variable types:\n", df.dtypes)
# print(df.info())
# # Descriptive Statistics
# print("Descriptive Statistics:")
# print(df.describe(include='all'))

job_by_dept=df.groupby('department')['jobs'].nunique()

u_job_by_dept=job_by_dept.reset_index()
u_job_by_dept.columns=['department','job_count']
print(u_job_by_dept)

sns.histplot(data=u_job_by_dept, x='department')
plt.xlabel('department')
plt.ylabel('job count')
plt.title('jobs by department');