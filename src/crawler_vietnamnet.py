import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# Hàm lấy chi tiết từ từng bài báo
def extract_article_details(article_url, seen_urls):
    try:
        # Kiểm tra nếu URL đã tồn tại trong set seen_urls
        if article_url in seen_urls:
            print(f"Duplicate article: {article_url}")
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
        
        # Lấy nội dung từ <h2 class="content-detail-sapo sm-sapo-mb-0">
        sapo = soup.find('h2', class_='content-detail-sapo sm-sapo-mb-0')
        content_sapo = sapo.get_text(strip=True) if sapo else ""
        
        # Lấy nội dung chính từ <div class="maincontent main-content">
        main_content = soup.find('div', class_='maincontent main-content')
        content_paragraphs = main_content.find_all('p') if main_content else []
        content_body = "\n".join([para.get_text(strip=True) for para in content_paragraphs])
        
        # Kết hợp <h2> và nội dung chi tiết từ <div class="maincontent main-content">
        content = content_sapo + "\n" + content_body if content_body else content_sapo
        
        # Lấy ngày đăng bài từ <div class="bread-crumb-detail__time">
        time_div = soup.find('div', class_='bread-crumb-detail__time')
        published_date = time_div.get_text(strip=True) if time_div else None
        
        # Lấy tên tác giả từ <div class="article-detail-author__main">
        author_wrapper = soup.find('div', class_='article-detail-author__main')
        author = "Unknown"
        
        if author_wrapper:
            # Tìm thẻ <a> có thuộc tính title bên trong article-detail-author__main
            author_tag = author_wrapper.find('a', {'title': True})
            if author_tag:
                author = author_tag['title']  # Lấy thuộc tính title của thẻ <a>
        
        # Lấy category từ <div class="bread-crumb-detail"> -> <li><a>
        breadcrumb = soup.find('div', class_='bread-crumb-detail')
        category_tags = breadcrumb.find_all('li') if breadcrumb else []
        category = category_tags[-1].get_text(strip=True) if category_tags else "Unknown"  # Lấy thẻ <li> cuối cùng (category)
        
        
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
            title = link.get('title')  # Extract title from 'title' attribute
            
            # Kiểm tra số từ trong tiêu đề (ít nhất 6 từ)
            if title and len(title.split()) >= 6:
                if href.startswith('/'):
                    href = 'https://vietnamnet.vn' + href  # Build full URL
                
                # Sử dụng hàm extract_article_details với seen_urls để tránh trùng lặp
                article_details = extract_article_details(href, seen_urls)  # Crawl article details
                if article_details:
                    article_data.append(article_details)
    
    return article_data

# Hàm tạo danh sách URL theo ngày
def create_url_for_date(date):
    # Định dạng ngày phù hợp với URL của vietnamnet.vn (dd/mm/yyyy)
    date_str = date.strftime("%d/%m/%Y")  # Định dạng ngày theo d/m/yyyy
    
    # Mã hóa URL: chuyển dấu "/" thành "%2F"
    encoded_date_str = date_str.replace("/", "%2F")
    
    # Tạo URL với ngày được mã hóa và đúng định dạng
    url = f"https://vietnamnet.vn/tin-tuc-24h?bydate={encoded_date_str}-{encoded_date_str}&cate=000003"
    
    return [url]

# Hàm lấy tất cả bài viết trong khoảng thời gian
def collect_articles_between_dates(start_date, end_date):
    current_date = start_date
    all_articles = []
    seen_urls = set()
    
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
