import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# Hàm chuyển đổi datetime sang Unix timestamp
def date_to_timestamp(date_obj):
    return int(date_obj.timestamp())

# Hàm lấy danh sách bài viết từ trang chủ
def collect_articles_from_page(page_url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:11.0) Gecko/20100101'}
    request = urllib.request.Request(page_url, headers=headers)
    
    response = urllib.request.urlopen(request)
    page_html = response.read()
    
    soup = BeautifulSoup(page_html, 'html.parser')
    
    article_tags = soup.find_all('h3') or soup.find_all('article')
    
    article_urls = []
    for tag in article_tags:
        link = tag.find('a', href=True)
        if link:
            href = link['href']
            if href.startswith('/'):
                href = 'https://vnexpress.net' + href
            article_urls.append(href)
    
    return article_urls

# Hàm lấy chi tiết từ từng bài báo
def extract_article_details(article_url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:11.0) Gecko/20100101'}
        request = urllib.request.Request(article_url, headers=headers)
        
        response = urllib.request.urlopen(request)
        article_html = response.read()
        
        soup = BeautifulSoup(article_html, 'html.parser')
        
        title = soup.find('h1', class_='title-detail').text.strip() if soup.find('h1', class_='title-detail') else None
        
        content_paragraphs = soup.find_all('p')
        content = ""
        for para in content_paragraphs:
            content += para.get_text(separator=" ") + "\n"
        
        published_date = soup.find('span', class_='date').text.strip() if soup.find('span', class_='date') else None
        
        author_info = "Unknown"
        if len(content) > 0:
            content_lines = content.strip().split("\n")
            last_line = content_lines[-1].strip()
            author_info = last_line.replace("\n", "").replace(",", "").replace(".", "").strip()
            content = content.rsplit('.', 1)[0].strip()
        
        collected_date = datetime.now().strftime('%Y-%m-%d')
        
        return {
            "title": title,
            "url": article_url,
            "content": content,
            "published_date": published_date,
            "author_info": author_info,
            "collected_date": collected_date
        }
    except Exception as e:
        print(f"Could not retrieve article {article_url}: {e}")
        return None

# Hàm để tạo các URL cho khoảng thời gian
def generate_urls_for_date_range(start_date, end_date):
    urls = []
    current_date = start_date
    while current_date <= end_date:
        timestamp = date_to_timestamp(current_date)
        url = f'https://vnexpress.net/category/day/cateid/1003159/fromdate/{timestamp}/todate/{timestamp}/allcate/1003159'
        urls.append(url)
        current_date += timedelta(days=1)
    return urls

def scrape_articles(start_date, end_date):
    urls_by_date = generate_urls_for_date_range(start_date, end_date)
    collected_articles = []
    
    for page_url in urls_by_date:
        print(f"Collecting articles from: {page_url}")
        article_urls = collect_articles_from_page(page_url)
        
        for article_url in article_urls:
            article_details = extract_article_details(article_url)
            if article_details:
                collected_articles.append(article_details)
    
    return collected_articles
