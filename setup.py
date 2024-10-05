from setuptools import setup, find_packages

setup(
    name="finance-news-crawl-tool",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4',
        'lxml'
    ],
    entry_points={
        'console_scripts': [
            'crawl-news=src.crawler:main',
        ],
    },
)
