import unittest
from bs4 import BeautifulSoup
from src.parser import extract_data

class TestParser(unittest.TestCase):
    
    def test_extract_data_links(self):
        """Test extract_data function for extracting links."""
        html_content = '<a href="https://example.com" title="Example Title">Link</a>'
        bs = BeautifulSoup(html_content, 'html.parser')
        container = bs.find_all('a')

        output, title, order = extract_data(container, type='link')
        
        # Test that the link is correctly extracted
        self.assertEqual(output[0], 'https://example.com')  # Check URL
        self.assertEqual(title[0], 'Example Title')  # Check title
        self.assertEqual(order, 'first')  # Ensure the correct order is returned
    
    def test_extract_data_content(self):
        """Test extract_data function for extracting text content."""
        html_content = '<div>Sample content</div>'
        bs = BeautifulSoup(html_content, 'html.parser')
        container = bs.find_all('div')
        
        output, title, order = extract_data(container, type='content')
        
        # Test that the content is correctly extracted
        self.assertEqual(output[0], 'Sample content')  # Check content
        self.assertEqual(order, 'last')  # Ensure the correct order is returned

if __name__ == '__main__':
    unittest.main()
