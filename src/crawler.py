# src/crawler.py
import urllib.request
from bs4 import BeautifulSoup
from src.parser import extract_article_details

def collect_articles_from_page(page_url, key='h3'):
    """Crawl and collect all article URLs from a given page."""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:11.0) Gecko/20100101'}
    request = urllib.request.Request(page_url, headers=headers)
    
    response = urllib.request.urlopen(request)
    page_html = response.read()
    
    soup = BeautifulSoup(page_html, 'html.parser')
    
    # Find all tags (default h3) that contain article URLs
    article_tags = soup.find_all(key) or soup.find_all('article')
    
    article_urls = []
    for tag in article_tags:
        link = tag.find('a', href=True)
        if link:
            href = link['href']
            if href.startswith('/'):
                href = 'https://vnexpress.net' + href
            article_urls.append(href)
    
    return article_urls

def crawl_articles(pages=5):
    """Loop through multiple pages and crawl articles."""
    for page_num in range(1, pages + 1):
        page_url = 'https://vnexpress.net/kinh-doanh' if page_num == 1 else f'https://vnexpress.net/kinh-doanh-p{page_num}'
        
        print(f"Collecting articles from: {page_url}")
        
        # Collect all article URLs from the current page
        article_urls = collect_articles_from_page(page_url)
        
        # Process each article
        for article_url in article_urls:
            article_details = extract_article_details(article_url)
            
            # If article details are extracted, print them
            if article_details:
                print(article_details)
            else:
                print(f"Skipping article: {article_url}")

