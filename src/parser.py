# src/parser.py
import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime

def extract_article_details(article_url):
    """Extract details from an article."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:11.0) Gecko/20100101'}
        request = urllib.request.Request(article_url, headers=headers)
        
        # Send request and get response
        response = urllib.request.urlopen(request)
        article_html = response.read()
        
        # Parse HTML
        soup = BeautifulSoup(article_html, 'html.parser')
        
        # Extract title
        title = soup.find('h1', class_='title-detail').text.strip() if soup.find('h1', class_='title-detail') else None
        
        # Extract content
        content_paragraphs = soup.find_all('p')
        content = "".join([para.get_text(separator=" ") + "\n" for para in content_paragraphs])
        
        # Extract published date
        published_date = soup.find('span', class_='date').text.strip() if soup.find('span', class_='date') else None
        
        # Extract author from the last sentence
        author_info = "Unknown"
        if "." in content:
            last_sentence = content.split('.')[-1].strip()
            if '(' in last_sentence:
                author_info = last_sentence.replace('\n', '').replace(',', '').strip()
                content = content.rsplit('.', 1)[0].strip()  # Remove author from content
        
        # Get current date for when data was collected
        collected_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
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
