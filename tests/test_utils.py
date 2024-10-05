# tests/test_utils.py

import unittest
from src.utils import fix_url

class TestUtils(unittest.TestCase):
    
    def test_fix_url_with_host(self):
        """Test fix_url function with a relative URL."""
        host = 'https://vnexpress.net/kinh-doanh'
        url = '/some/path'
        result = fix_url(host, url)
        self.assertEqual(result, 'https://vnexpress.net/kinh-doanh/some/path')
    
    def test_fix_url_with_full_url(self):
        """Test fix_url function with an absolute URL."""
        host = 'https://vnexpress.net/kinh-doanh'
        url = 'https://another.com/path'
        result = fix_url(host, url)
        self.assertEqual(result, 'https://another.com/path')

if __name__ == '__main__':
    unittest.main()
