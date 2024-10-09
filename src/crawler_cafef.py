import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# Hàm lấy chi tiết từ từng bài báo
# Hàm lấy chi tiết từ từng bài báo
# Hàm lấy chi tiết từ từng bài báo
def extract_article_details(article_url, seen_urls):
    try:
        # Kiểm tra nếu URL đã tồn tại trong set seen_urls
        if article_url in seen_urls:
            # print(f"Duplicate article: {article_url}")
            return None
        
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
        
        # Lấy ngày đăng bài từ <span class="pdate">
        time_span = soup.find('span', class_='pdate')
        published_date = time_span.get_text(strip=True) if time_span else None
        
        # Lấy tác giả từ <p class="author">
        author_info = soup.find('p', class_='author')
        author = author_info.get_text(strip=True) if author_info else "Unknown"
        
        # Lấy chuyên mục (category) từ <a data-role="cate-name" class="category-page__name cat">
        category_tag = soup.find('a', {'data-role': 'cate-name', 'class': 'category-page__name cat'})
        category = category_tag.get_text(strip=True) if category_tag else "Unknown"
        
        
        # Ngày thu thập dữ liệu
        collected_date = datetime.now().strftime('%Y-%m-%d')
        
        # Thêm URL vào set để đánh dấu đã thu thập
        seen_urls.add(article_url)
        
        return {
            "title": title,
            "url": article_url,
            "content": content,
            "published_date": published_date,
            "author": author,
            "category": category,
            "collected_date": collected_date
        }
    except Exception as e:
        print(f"Could not retrieve article {article_url}: {e}")
        return None


# Hàm lấy danh sách bài viết từ trang
def collect_articles_from_page(page_url, seen_urls):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:11.0) Gecko/20100101'}
    request = urllib.request.Request(page_url, headers=headers)
    
    response = urllib.request.urlopen(request)
    page_html = response.read()
    
    soup = BeautifulSoup(page_html, 'html.parser')
    
    # Tìm tất cả các thẻ <h3> chứa link bài báo
    article_tags = soup.find_all('h3')
    
    article_data = []
    
    for tag in article_tags:
        link = tag.find('a', href=True)
        if link:
            href = link['href']
            title = link.get('title')
            
            # Kiểm tra số từ trong tiêu đề (ít nhất 6 từ)
            if title and len(title.split()) >= 6:
                if href.startswith('/'):
                    href = 'https://cafef.vn' + href  # Build full URL
                
                # Sử dụng hàm extract_article_details với seen_urls để tránh trùng lặp
                article_details = extract_article_details(href, seen_urls)  # Crawl article details
                if article_details:
                    article_data.append(article_details)
    
    return article_data

# Sử dụng set để lưu trữ URL đã thu thập
seen_urls = set()

# Hàm lấy tất cả bài viết trong khoảng thời gian
def collect_articles_between_dates(start_date, end_date):
    current_date = start_date
    all_articles = []
    
    while current_date <= end_date:
        urls = create_url_for_date(current_date)
        print(f"Collecting articles for date: {current_date.strftime('%d-%m-%Y')}")
        
        # Duyệt qua tất cả các URL trong danh sách theo ngày
        for url in urls:
            articles = collect_articles_from_page(url, seen_urls)
            all_articles.extend(articles)
        
        # Tăng ngày hiện tại lên 1
        current_date += timedelta(days=1)
    
    return all_articles

# Hàm tạo danh sách URL theo ngày
def create_url_for_date(date):
    # Định dạng ngày phù hợp với URL của cafef.vn
    date_str_cf = date.strftime("%-d/%-m/%Y")  # Định dạng ngày với dấu "/" thay vì dấu "-"
    
    urls = [
        f"https://cafef.vn/tai-chinh-ngan-hang/{date_str_cf}.chn",
        f"https://cafef.vn/xa-hoi/{date_str_cf}.chn",
        f"https://cafef.vn/thi-truong-chung-khoan/{date_str_cf}.chn",
        f"https://cafef.vn/bat-dong-san/{date_str_cf}.chn",
        f"https://cafef.vn/doanh-nghiep/{date_str_cf}.chn",
        f"https://cafef.vn/smart-money/{date_str_cf}.chn",
        f"https://cafef.vn/tai-chinh-quoc-te/{date_str_cf}.chn",
        f"https://cafef.vn/vi-mo-dau-tu/{date_str_cf}.chn",
        f"https://cafef.vn/kinh-te-so/{date_str_cf}.chn",
        f"https://cafef.vn/thi-truong/{date_str_cf}.chn"
    ]
    return urls


# Sử dụng set để lưu trữ URL đã thu thập
seen_urls = set()

# Hàm lấy tất cả bài viết trong khoảng thời gian
def collect_articles_between_dates(start_date, end_date):
    current_date = start_date
    all_articles = []
    
    while current_date <= end_date:
        urls = create_url_for_date(current_date)
        print(f"Collecting articles for date: {current_date.strftime('%d-%m-%Y')}")
        
        # Duyệt qua tất cả các URL trong danh sách theo ngày
        for url in urls:
            articles = collect_articles_from_page(url, seen_urls)
            all_articles.extend(articles)
        
        # Tăng ngày hiện tại lên 1
        current_date += timedelta(days=1)
    
    return all_articles
