from scraper import scrape_articles
from utils import save_to_json
from datetime import datetime

def main():
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")

    # Convert input to datetime objects
    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return
    
    articles = scrape_articles(start_date, end_date)
    save_to_json(articles, "articles.json")
    print("Data saved to articles.json")

if __name__ == "__main__":
    main()
