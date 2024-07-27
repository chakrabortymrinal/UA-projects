from webScrape import scrape_and_prase , get_first_movie_meta , get_all_movie_info , get_movie_details ,get_movie_details_df
import pandas as pd

# global var for df schema
# cols=["movie_name","movie_rating","movie_url","movie_genres","movie_cast"]
# df = pd.DataFrame(columns=cols)


def get_tmdb_content(url):
    try:
        tmdb_content = scrape_and_prase(url)
        # print(f"Title : {tmdb_content}")
        # first_movie_name , first_movie_rating, first_movie_url = get_first_movie_meta(tmdb_content)
        # print(f" first movie name: {first_movie_name}; and rating is: {first_movie_rating} , the url is: {first_movie_url}")

        all_movies_info = get_all_movie_info(tmdb_content)
        for movie_no,(movie_name,movie_rating,movie_url) in enumerate(all_movies_info, start=1):
            print(f" movie no: {movie_no}")
            print(f" movie name: {movie_name}")
            print(f" movie rating is: {movie_rating}")
            print(f" movie  url is: {movie_url}")

            movie_genres, movie_cast = get_movie_details(movie_url)
            print(f"  Genres: {', '.join(movie_genres)}")
            print(f"  Cast: {', '.join(movie_cast)}")

    except ValueError as e:
        print(f"Error : {e}")

def get_tmdb_content_df(url,page):
    try:
        df=get_movie_details_df(url)
        print(df)
        df.to_csv(f"tmdb-{page}.csv", index=False)
    except ValueError as e:
        print(f"Error : {e}")

if __name__ == "__main__":
    # get_tmdb_content('https://www.themoviedb.org/movie/now-playing?page=2')
    for page in range(1, 6):
        url = f"https://www.themoviedb.org/movie/now-playing?page={page}"
        get_tmdb_content_df(url,page)
    