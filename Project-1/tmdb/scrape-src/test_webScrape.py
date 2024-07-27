# Tests for the function written

from webScrape import scrape_and_prase


def test_scrape_and_prase1(url):
    try:
        soup1 = scrape_and_prase(url)
        print(f"Title : {soup1.title.string}")
    except ValueError as e:
        print(f"Error : {e}")

if __name__ == "__main__":
    #200 OK
    test_scrape_and_prase1('https://www.themoviedb.org/movie')
    #404 NOT FOUND
    test_scrape_and_prase1('https://www.themoviedb.org/movieFALSE')
