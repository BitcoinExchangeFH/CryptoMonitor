#!/bin/python
import requests
from bs4 import BeautifulSoup

class HtmlExtractor(object):
    """
    Extract the cryptocurrency price information from the website coinmarketcap.
    By default, only the first 10 records (more than 10% of market cap) is recorded.
    """
    URL = "https://coinmarketcap.com/currencies/%s/#markets"
    NUMBER = 10
    ID_INDEX = 0
    EXCHANGE_INDEX = 1
    PAIR_INDEX = 2
    VOLUME_INDEX = 3
    PRICE_INDEX = 4
    MARKET_SHARE_INDEX = 5
    LATEST_UPDATE_INDEX = 6
    
    def __init__(self):
        """
        Constructor
        """
        pass
    
    def get_data(self, symbol):
        """
        Get data from the symbol and parse it.
        :param symbol: Symbol
        :returns Array of market volume
        """
        ret = []
        response = requests.get(HtmlExtractor.URL % symbol)
        if response.status_code == 200:
            # Successful
            soup = BeautifulSoup(response.text, 'html.parser')
            tables = soup.find_all('table')
            market_table = None
            for table in tables:
                if table.has_attr('id'):
                    market_table = table
            assert market_table is not None, "Cannot find table markets-table"
            table_body = market_table.find_all('tbody')
            assert len(table_body) == 1, \
                    "Number of table body (%d) should be equal to 1." % len(table_body)
            records = table_body[0].find_all('tr')
            
            # Parse each record
            for record in records:
                entries = record.find_all('td')
                exchange = entries[HtmlExtractor.EXCHANGE_INDEX].text
                pair = entries[HtmlExtractor.PAIR_INDEX].text
                price = float(entries[HtmlExtractor.PRICE_INDEX].text
                              .replace("$", "").replace(",", ""))
                market_share = float(entries[HtmlExtractor.MARKET_SHARE_INDEX]
                                     .text.replace("%", ""))
                update = entries[HtmlExtractor.LATEST_UPDATE_INDEX].text
                if update == "Recently":
                    ret.append((exchange, pair, price, market_share))
        else:
            # Failed
            # TBD
            raise NotImplementedError("Not yet implemented failed case.")
        
        return ret

if __name__ == '__main__':
    extractor = HtmlExtractor()
    response = extractor.get_data("ripple")
    print(response)