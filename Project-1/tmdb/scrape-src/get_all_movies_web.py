import requests
from bs4 import BeautifulSoup

# get reponse (had to disable SSL verfication as i am behind a proxy)
url = 'https://www.themoviedb.org/movie'
response = requests.get(url,verify=False)

 
status_code = response.status_code
print(f'Status Code: {status_code}')

# status code 200 to be verified
if status_code == 200:
    # save contents into var and print
    page_content = response.content
    # print(page_content)
    
    # display the first 200 characters
    print(f'dataType of the var: {type(page_content)}')

    soup = BeautifulSoup(page_content, 'html.parser')
    # print(soup.prettify()[:1000])
    title = soup.title.string
    print(f"Title : {title}")

    # print(f'First 200 characters of the content: {page_content[:200]}')
else:
    print('Failed to retrieve the webpage.')
