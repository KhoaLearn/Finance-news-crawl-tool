# tests/test_podcasts.py

import unittest
from unittest import mock
from src.podcasts import vne_podcast_list, get_vne_podcast

class TestPodcasts(unittest.TestCase):
    
    @mock.patch('src.podcasts.urlopen')
    def test_vne_podcast_list(self, mock_urlopen):
        """Test podcast list extraction from vnexpress."""
        html_content = '<a href="https://vnexpress.net/kinh-doanh/podcast">Podcast</a>'
        mock_urlopen.return_value.read.return_value = html_content
        
        url = 'https://vnexpress.net/podcasts'
        key = 'div'
        result = vne_podcast_list(url, key)
        
        self.assertEqual(result[0], 'https://vnexpress.net/kinh-doanh/podcast')
    
    @mock.patch('src.podcasts.urlopen')
    def test_get_vne_podcast(self, mock_urlopen):
        """Test extracting podcast audio URLs."""
        html_content = '<audio src="https://vnexpress.net/kinh-doanh/audio.mp3"></audio>'
        mock_urlopen.return_value.read.return_value = html_content
        
        url = 'https://vnexpress.net/podcast/episode'
        result = get_vne_podcast(url)
        
        self.assertEqual(result[0], 'https://vnexpress.net/kinh-doanh/audio.mp3')

if __name__ == '__main__':
    unittest.main()
