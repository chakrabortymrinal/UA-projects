import requests
import pandas as pd
import configparser
import json

# seperate out secrets and general configs and protect secrets. 
# get apikey form secrets.ini file
config = configparser.ConfigParser()
config.read('secrets.ini')
api_key = config['settings']['api_key']

# as per the API documenation https://developer.themoviedb.org/reference/configuration-jobs
url = 'https://api.themoviedb.org/3/configuration/jobs'

# disabling SSL verification as i have a Proxy in between .
response = requests.get(url, params={'api_key': api_key}, verify=False)

if response.status_code == 200:
    data = response.json()
    with open('./out/movie_jobs_data.json', 'w') as file:
        json.dump(data, file, indent=4)

    print("Data save to movie_jobs_data.json successful")

else:
    print(f"data fetch failed with reponse : {response.status_code}")


## getting data into CSV 

# # df = pd.DataFrame([data])
# # print(df.head())

# # flattern format [{department: value, jobs: []}] 

# flat_data = []
# for item in data:
#     dep = item['department']
#     for job in item['jobs']:
#         flat_data.append({'department':dep, 'jobs':job})

# df = pd.DataFrame(flat_data)
# print(df.head())
# df.to_csv('./out/jobs.csv',index=False)