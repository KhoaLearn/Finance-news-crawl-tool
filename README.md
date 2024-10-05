# Finance News Crawl Tool

This repository contains Python scripts to crawl and scrape articles from various financial news websites, including Cafebiz, Cafef, and VNExpress. The tool is designed to collect, clean, and store articles in a structured format, allowing you to analyze and retrieve key financial data. The collected data is stored in JSON format for easy integration into other data pipelines.

## Project Structure

```bash
FINANCE-NEWS-CRAWL-TOOL/
│
├── data/  # Contains collected articles in JSON format
│   ├── cafebiz_articles.json
│   ├── cafef_articles.json
│   └── vnexpress_articles.json
│
├── notebooks/  # Jupyter Notebooks for exploring scraping logic
│   ├── crawling_cafebiz.ipynb
│   ├── crawling_cafef.ipynb
│   └── crawling_vnexpress.ipynb
│
├── src/  # Source code for crawlers and utilities
│   ├── clean.py  # Contains functions to clean article data before saving
│   ├── crawler_cafebiz.py  # Crawler for Cafebiz
│   ├── crawler_cafef.py  # Crawler for Cafef
│   └── crawler_vnexpress.py  # Crawler for VNExpress
│
├── main.py  # Main entry point for running the crawlers
├── requirements.txt  # Python dependencies for the project
└── README.md  # You're reading it now!
```

## Features

- **Cafebiz, Cafef, VNExpress Scrapers**: Extract articles with details like title, content, author, and published date from each of these news sources.
- **Date Range Selection**: Specify a date range for scraping articles.
- **Data Cleaning**: Titles are cleaned of unwanted characters (`'`, `"`, `(`), and `published_date` is standardized into the `YYYY-MM-DD` format, handling different input formats such as `01-01-2023 - 11:19 AM` and `05/10/2024 16:45 PM`.
- **JSON Output**: The scraped articles are saved in JSON format for further use or analysis.

## Requirements

To install the required dependencies, run:

```bash
pip install -r requirements.txt
```

## Usage

### Running the Crawler

To start crawling and scraping articles from Cafebiz, Cafef, or VNExpress, run the `main.py` script:

```bash
python main.py
```

You will be prompted to select which website to scrape, and you can input the start and end dates for the articles.

### Example Interaction

```bash
Select website to scrape (1: Cafebiz, 2: VNExpress, 3: Cafef): 1
Enter the start date (YYYY-MM-DD): 2024-09-25
Enter the end date (YYYY-MM-DD): 2024-09-30
Scraping Cafebiz from 2024-09-25 to 2024-09-30...
Collected 15 articles. Saved to data/cafebiz_articles.json.
```

### Data Cleaning

Before saving the articles, the data is cleaned by the `clean.py` script:

- **Null Titles**: Articles without titles are discarded.
- **Title Cleaning**: Unwanted characters such as `'`, `"`, `(` are removed from titles.
- **Published Date Formatting**: Published dates are converted to the `YYYY-MM-DD` format, handling different input formats such as `01-01-2023 - 11:19 AM` and `05/10/2024 16:45 PM`.

### Output

The cleaned and formatted data is stored in the `data/` folder as JSON files:

- `cafebiz_articles.json`
- `cafef_articles.json`
- `vnexpress_articles.json`

### Example JSON Output

```json
[
    {
        "title": "New Financial Regulations",
        "url": "https://cafebiz.vn/new-regulations",
        "content": "The new regulations are expected to improve the financial market...",
        "published_date": "2024-10-01",
        "author": "John Doe",
        "collected_date": "2024-10-05"
    },
    ...
]
```

## Contributing

Feel free to submit issues or contribute by creating pull requests. Any improvements or new ideas to enhance the crawling and scraping are always welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```

