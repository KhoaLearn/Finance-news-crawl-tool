from datetime import datetime
import json
import os
from src.crawler_cafebiz import collect_articles_between_dates as cafebiz_collect
from src.crawler_vnexpress import scrape_articles as vnexpress_collect
from src.crawler_cafef import collect_articles_between_dates as cafef_collect
from src.utils import save_to_json
from src.clean import clean_articles  # Import the cleaning function

def get_valid_date_input(prompt):
    while True:
        date_input = input(prompt)
        try:
            date_obj = datetime.strptime(date_input, "%Y-%m-%d")
            if date_obj > datetime.now():
                print("Date cannot be in the future. Please enter a valid date.")
            else:
                return date_obj
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

# Hàm chạy chương trình chính
def main():
    # Ensure 'data' directory exists
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # Lựa chọn website cần thu thập dữ liệu
    website_choice = input("Select website to scrape (1: Cafebiz, 2: VNExpress, 3: Cafef): ")
    
    if website_choice not in ["1", "2", "3"]:
        print("Invalid selection. Please select 1, 2, or 3.")
        return

    # Nhập ngày bắt đầu và kết thúc từ người dùng theo định dạng YYYY-MM-DD
    start_date = get_valid_date_input("Enter the start date (YYYY-MM-DD): ")
    end_date = get_valid_date_input("Enter the end date (YYYY-MM-DD): ")
    
    # Kiểm tra nếu ngày kết thúc nhỏ hơn ngày bắt đầu
    if end_date < start_date:
        print("End date cannot be earlier than start date.")
        return

    # Thu thập dữ liệu từ website được chọn
    if website_choice == "1":
        print(f"Scraping Cafebiz from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}...")
        articles = cafebiz_collect(start_date, end_date)
        output_file = "data/cafebiz_articles.json"  # Save to 'data/' folder
    elif website_choice == "2":
        print(f"Scraping VNExpress from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}...")
        articles = vnexpress_collect(start_date, end_date)
        output_file = "data/vnexpress_articles.json"  # Save to 'data/' folder
    elif website_choice == "3":
        print(f"Scraping Cafef from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}...")
        articles = cafef_collect(start_date, end_date)
        output_file = "data/cafef_articles.json"  # Save to 'data/' folder

    # Clean the articles before saving
    cleaned_articles = clean_articles(articles)

    # Lưu kết quả vào file JSON trong thư mục 'data/'
    save_to_json(cleaned_articles, output_file)
    print(f"Collected {len(cleaned_articles)} articles. Saved to {output_file}.")

if __name__ == "__main__":
    main()
