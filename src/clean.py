import re
from datetime import datetime

def clean_articles(articles):
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
        published_date = article.get("published_date")
        
        # Skip article if title is None or empty
        if not title:
            continue
        
        # Clean unwanted characters from title
        cleaned_title = re.sub(r"[\'\"()]", "", title)
        article["title"] = cleaned_title
        
        # Clean and format 'published_date' field
        if published_date:
            try:
                # Try to handle both formats
                if "-" in published_date:
                    # Format: "01-01-2023 - 11:19 AM"
                    date_str = published_date.split(" - ")[0]  # Extract date part
                    date_obj = datetime.strptime(date_str, "%d-%m-%Y")
                elif "/" in published_date:
                    # Format: "05/10/2024 16:45 PM"
                    date_str = published_date.split(" ")[0]  # Extract date part
                    date_obj = datetime.strptime(date_str, "%d/%m/%Y")
                else:
                    raise ValueError("Unknown date format")
                
                # Format the date to %Y-%m-%d
                article["published_date"] = date_obj.strftime("%Y-%m-%d")
            except ValueError:
                # If the date format is invalid, skip this article
                print(f"Invalid date format for article: {title}, skipping.")
                continue
        
        # Add the cleaned article to the final list
        cleaned_articles.append(article)
    
    return cleaned_articles
