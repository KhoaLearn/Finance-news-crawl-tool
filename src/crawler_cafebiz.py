import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# Hàm lấy chi tiết từ từng bài báo
def extract_article_details(article_url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:11.0) Gecko/20100101'}
        request = urllib.request.Request(article_url, headers=headers)
        
        # Gửi yêu cầu lấy trang bài báo
        response = urllib.request.urlopen(request)
        article_html = response.read()
        
        # Parse bài báo
        soup = BeautifulSoup(article_html, 'html.parser')
        
        # Lấy tiêu đề
        title = soup.find('h1').get_text(strip=True) if soup.find('h1') else None
        
        # Lấy nội dung từ <h2> và <div class="detail-content">
        sapo = soup.find('h2', class_='sapo')
        content_sapo = sapo.get_text(strip=True) if sapo else ""
        
        detail_content = soup.find('div', class_='detail-content')
        content_paragraphs = detail_content.find_all('p') if detail_content else []
        content_body = "\n".join([para.get_text(strip=True) for para in content_paragraphs])
        
        # Kết hợp <h2> và <div class="detail-content">
        content = content_sapo + "\n" + content_body if content_body else content_sapo
        
        # Lấy ngày đăng bài từ <span class="time">
        time_span = soup.find('span', class_='time')
        published_date = time_span.get_text(strip=True) if time_span else None
        
        # Lấy tác giả
        author_info = soup.find('strong', class_='detail-author').get_text(strip=True) if soup.find('strong', class_='detail-author') else "Unknown"
        content = content.rsplit('.', 1)[0].strip()
        

        # Ngày thu thập dữ liệu
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

# Hàm lấy danh sách bài viết từ trang theo ngày
def collect_articles_from_page(page_url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:11.0) Gecko/20100101'}
    request = urllib.request.Request(page_url, headers=headers)
    
    response = urllib.request.urlopen(request)
    page_html = response.read()
    
    soup = BeautifulSoup(page_html, 'html.parser')
    
    # Tìm tất cả các thẻ <h3> chứa link bài báo
    article_tags = soup.find_all('h3')
    
    article_data = []
    seen_urls = set()  # Set to track unique URLs
    
    for tag in article_tags:
        link = tag.find('a', href=True)
        if link:
            href = link['href']
            title = link.get('title')  # Extract title from 'title' attribute
            
            # Kiểm tra số từ trong tiêu đề (ít nhất 6 từ) và loại bỏ URL trùng
            if title and len(title.split()) >= 6:
                if href.startswith('/'):
                    href = 'https://cafebiz.vn' + href  # Build full URL
                
                if href not in seen_urls:  # Check for duplicates
                    article_details = extract_article_details(href)  # Crawl article details
                    if article_details:
                        article_data.append(article_details)
                    seen_urls.add(href)  # Add URL to seen set to avoid duplicates
    
    return article_data

# Hàm tạo URL theo ngày
def create_url_for_date(date):
    date_str = date.strftime("%d-%m-%Y")  # Định dạng ngày
    url = f'https://cafebiz.vn/xem-theo-ngay-c176114-{date_str}.chn'
    return url

# Hàm lấy tất cả bài viết trong khoảng thời gian
def collect_articles_between_dates(start_date, end_date):
    current_date = start_date
    all_articles = []
    
    while current_date <= end_date:
        url = create_url_for_date(current_date)
        # print(f"Collecting articles for date: {current_date.strftime('%d-%m-%Y')}")
        
        # Thu thập bài viết từ trang theo ngày
        articles = collect_articles_from_page(url)
        all_articles.extend(articles)
        
        # Tăng ngày hiện tại lên 1
        current_date += timedelta(days=1)
    
    return all_articles
