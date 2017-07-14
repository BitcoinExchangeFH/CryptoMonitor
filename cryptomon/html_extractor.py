#!/bin/python
import requests
from bs4 import BeautifulSoup

class CurrencyPair(object):
    """
    Information of exchange, pair, price, market share.
    """
    def __init__(self, exchange, pair, price, market_share):
        """
        Constructor
        """
        self.exchange = exchange
        self.pair = pair
        self.price = price
        self.market_share = market_share
    
    def __str__(self):
        return ("Currency: %s, Pair: %s, Price: %.8f, Market share: %.2f%%" %
                (self.exchange, self.pair, self.price, self.market_share))

class HtmlExtractor(object):
    """
    Extract the cryptocurrency price information from the website coinmarketcap.
    By default, only the first 10 records (more than 10% of market cap) is recorded.
    """
    URL = "https://coinmarketcap.com/currencies/%s/#markets"
    MAX_COMPARE_PAIRS = 10
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
                    ret.append(CurrencyPair(exchange, pair, price, market_share))
        else:
            # Failed
            raise Exception("Http request error: %d" % response.status_code)
        
        return ret
    
    def get_arbitrage_pair(self, symbol, price_diff):
        """
        Get arbitrage pair
        :param symbol       Symbol name
        :param price_diff   Price difference
        :return Tuple of arbitrage pair. None if not found.
        """
        pairs = self.get_data(symbol)
        num_of_pairs = min(len(pairs), HtmlExtractor.MAX_COMPARE_PAIRS)
        arb_pairs = []
        
        # Find all the arbitrage pairs
        for i in range(0, num_of_pairs):
            for j in range(i+1, num_of_pairs):
                if (pairs[i].price / pairs[j].price > 1 + price_diff or
                    pairs[j].price / pairs[i].price > 1 + price_diff):
                    arb_pairs.append((pairs[i], pairs[j]))
        
        if len(arb_pairs) > 0:
            arb_pairs = sorted(arb_pairs, 
                                key=(lambda x: x[0].market_share + x[1].market_share),
                                reverse=True)
            return arb_pairs[0]
        else:
            return None
        
if __name__ == '__main__':
    extractor = HtmlExtractor()
    currency = "ripple"
    response = extractor.get_arbitrage_pair(currency, 0.1)
    if response is not None:
        print("Arbitrage pair on %s:\n%s\n%s" % (currency, response[0], response[1]))
    else:
        print("No arbitrage pair on %s." % currency)