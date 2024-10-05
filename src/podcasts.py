# src/podcasts.py

from urllib.request import urlopen
from bs4 import BeautifulSoup

def vne_podcast_list(url, key):
    html = urlopen(url)
    bs = BeautifulSoup(html.read(), 'lxml')
    ls = [a['href'] for a in bs.select(f'{key} a[href]')]
    return ls

def get_vne_podcast(url):
    html = urlopen(url)
    bs = BeautifulSoup(html.read(), 'lxml')
    container = bs.find_all('audio')
    for url in container:
        audio_url = url['src']
    return audio_url