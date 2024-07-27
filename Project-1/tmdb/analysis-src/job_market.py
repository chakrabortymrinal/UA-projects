import requests

url = "https://jsearch.p.rapidapi.com/search"

querystring = {"query":"movie crew","page":"1"}

headers = {
    "X-RapidAPI-Key": "YOUR_RAPIDAPI_KEY",
    "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring ,verify=False)
job_listings = response.json()

for job in job_listings['data']:
    print(f"Job title: {job['title']}")
    print(f"Company: {job['company_name']}")
    print(f"Location: {job['location']}")
    print(f"Description: {job['description']}\n")