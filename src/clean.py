import re
from datetime import datetime

def clean_articles(articles, stopwords):
    """
    Clean the list of articles:
    - Remove articles where the title is null or empty.
    - Clean title from unwanted characters like ', ", (.
    - Format the 'published_date' to %Y-%m-%d if it follows the 
      formats "01-01-2023 - 11:19 AM" or "05/10/2024 16:45 PM".
    
    :param articles: List of article dictionaries
    :return: Cleaned list of articles
    """
    cleaned_articles = []
    
    for article in articles:
        title = article.get("title")
        content = article.get("content")
        # published_date = article.get("published_date")
        
        # Skip article if title is None or empty
        if not title:
            continue
        
        # Clean unwanted characters from title
        cleaned_title = re.sub(r"[\'\"()]", "", title)
        article["title"] = cleaned_title
        
        # Clean unwanted characters from content
        if content:
            cleaned_content = clean_content(content, stopwords)
            article["content"] = cleaned_content
        
        # Add the cleaned article to the final list
        cleaned_articles.append(article)
    
    return cleaned_articles

def clean_content(content, stopwords):
    """
    Clean the content:
    - Remove unwanted characters and patterns.
    - Replace escaped double quotes (\") with regular double quotes (").
    - Remove stopwords from the content.
    
    :param content: String content of the article
    :param stopwords: List of stopwords to remove
    :return: Cleaned content string
    """
    # Add period before removing newline characters if there isn't one
    content = re.sub(r'([^\.\!\?])[\n\r]+', r'\1. ', content)
    
    # Remove remaining \n and \r characters (if they appear consecutively)
    content = re.sub(r'[\n\r]', ' ', content)
    
    # Remove excess white spaces
    content = re.sub(r'\s+', ' ', content).strip()

    # Cut content after unwanted phrases
    content = re.split(r'BÌNH LUẬN HAY|Tặng sao|Hiện bình luận nào|Nạp sao|Tặng thành công|Tổng biên tập|Giấy phép hoạt động|Tổng số từ|Vui lòng viết tiếng Việt có dấu', content)[0]
    
    # Remove backslashes and replace escaped double quotes (from \" to ")
    content = content.replace('\\', '')  
    content = content.replace('\\"', '"')

    # Remove extra periods
    content = re.sub(r'\.\s*\.', '.', content)

    # Remove stop words
    words = content.split()
    filtered_words = [word for word in words if word.lower() not in stopwords]
    content = ' '.join(filtered_words)

    return content

def load_stopwords(stopwords_path):
    """
    Load stopwords from a file.
    
    :param stopwords_path: Path to the stopwords file
    :return: List of stopwords
    """
    with open(stopwords_path, 'r', encoding='utf-8') as f:
        stopwords = f.read().splitlines()
    return stopwords