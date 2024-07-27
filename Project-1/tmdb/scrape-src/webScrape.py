import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_and_prase(url):
    try:
        needed_headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"}
        response = requests.get(url, headers=needed_headers , verify=False)
        response.raise_for_status()  
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Failed to fetch the URL: {e}")
    
    # Create and return the BeautifulSoup instance
    return BeautifulSoup(response.content, 'html.parser')

def get_first_movie_meta(data):
    first_card = data.select_one('#page_1 > div:nth-child(1)')

    if not first_card:
        raise ValueError("not the first movie")
    movie_name_ele=first_card.select_one('div.content > h2 > a')
    movie_name= movie_name_ele.get_text(strip=True) if movie_name_ele else 'n/a'
    movie_url=movie_name_ele.get('href') if movie_name_ele else 'n/a'

    movie_rating_ele=first_card.select_one('div.content > div.consensus > div.outer_ring > div.user_score_chart')
    movie_rating=movie_rating_ele['data-percent'] if movie_rating_ele else 'not rated'
    
    return movie_name, movie_rating , movie_url

def get_all_movie_info(data):

    movie_info=[]
    # movie=data.select('#page_1 > div.card.style_1')
    movie=data.select('div.card.style_1')

    for movie in movie:
        movie_name_ele=movie.select_one('div.content > h2 > a')
        movie_name= movie_name_ele.get_text(strip=True) if movie_name_ele else 'n/a'
        movie_url=movie_name_ele.get('href') if movie_name_ele else 'n/a'

        movie_rating_ele=movie.select_one('div.content > div.consensus > div.outer_ring > div.user_score_chart')
        movie_rating=movie_rating_ele['data-percent'] if movie_rating_ele else 'not rated'

        if movie_name and movie_name.lower() !='n/a':
            movie_info.append((movie_name,movie_rating,movie_url))
    
    return movie_info

def get_movie_details(url):
    base_url = "https://www.themoviedb.org"
    full_url = f"{base_url}{url}"
    
    # Check if the URL is empty or null
    if not url:
        print("URL is empty or null. Moving on to the next one.")
        return ['n/a'],['n/a']
    
    try:
        data = scrape_and_prase(full_url)
        
        # Extract genres
        genres_elements = data.select('#original_header > div.header_poster_wrapper.false > section > div.title.ott_false > div > span.genres > a')
        genres = [genre.get_text(strip=True) for genre in genres_elements]
        
        # Extract cast
        cast_elements = data.select('#cast_scroller > ol > li > p:nth-child(2) > a')
        cast = [actor.get_text(strip=True) for actor in cast_elements]
        return genres, cast
    except ValueError as e:
        # print(f"Error : {e}")
        return ['n/a'],['n/a']


def get_movie_details_df(url):
    data = scrape_and_prase(url)
    movies_info = get_all_movie_info(data)
    
    movies_data = []
    for movie_name, movie_rating, movie_url in movies_info:
        movie_genres, movie_cast = get_movie_details(movie_url)
        movies_data.append({
            'movie_title': movie_name,
            'movie_user_rating': movie_rating,
            'movie_genres': ', '.join(movie_genres),
            'movie_cast': ', '.join(movie_cast)
        })
    
    return pd.DataFrame(movies_data)