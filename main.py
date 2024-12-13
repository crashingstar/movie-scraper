from scraper import IMDbScraper
from rank_tracker import IMDbRankTracker

def main():
    try:
        scraper = IMDbScraper()

        movies = scraper.scrape_top_250()

        rank_tracker = IMDbRankTracker()

        rank_tracker.compare_rank_changes(movies)

    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()