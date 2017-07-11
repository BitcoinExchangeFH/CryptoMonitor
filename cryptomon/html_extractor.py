import requests
from bs4 import BeautifulSoup

class HtmlExtractor(object):
    """
    Extract the cryptocurrency price information from the website coinmarketcap.
    By default, only the first 10 records (more than 10% of market cap) is recorded.
    """
    URL = "https://coinmarketcap.com/currencies/%s/#markets"
    NUMBER = 10
    
    def __init__(self):
        """
        Constructor
        """
        pass
    
    