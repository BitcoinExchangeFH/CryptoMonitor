#!/bin/python
from datetime import datetime
import time

class ArbitrageMonitor(object):
    """
    Arbitrage monitor
    """
    def __init__(self, 
                 pairs,
                 killer,
                 extractor,
                 slack,
                 sleep_sec,
                 max_error_count):
        """
        Constructor
        """
        self.arb_pairs_store = {}
        self.error_count = 0
        self.pairs = pairs
        self.killer = killer
        self.extractor = extractor
        self.slack = slack
        self.sleep_sec = sleep_sec
        self.max_error_count = max_error_count
    
    def check_if_signal(self, arb, pair):
        """
        Check whether to singal the arbitrage pair
        """
        if arb is None:
            return False
        
        symbol = pair[0]
        
        if symbol not in self.arb_pairs_store.keys():
            self.arb_pairs_store[symbol] = arb
            return True
        else:
            prev_arb = self.arb_pairs_store[symbol]
            if (prev_arb[0].exchange == arb[0].exchange and
                prev_arb[0].pair == arb[0].pair and 
                prev_arb[1].exchange == arb[1].exchange and
                prev_arb[1].pair == arb[1].pair):
                # Same as the previous arbitrage signal
                return False
            else:
                # Different from the previous arbitrage signal 
                self.arb_pairs_store[symbol] = arb    
                return True            
    
    def post(self, message):
        """
        Post message
        """
        message = (("[%s]\n" % datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")) +
                    message + "\n")
        print(message)
        self.slack.post_message(message)
        
    def run(self):
        """
        Run
        """
        message = "CryptoMonitor is started...\n"
        for pair in self.pairs:
            message += ("\tSymbol: %s, Level: %.2f%%\n" % (pair[0], pair[1] * 100))
        self.post(message)
        
        try:
            while not self.killer.kill_now:
                for pair in self.pairs:
                    # Quick exit if signal is received.
                    if self.killer.kill_now:
                        break
                    
                    symbol = pair[0]
                    level = pair[1]
                    
                    # Try to get the arbitage pair.
                    # If the exception tolerance count is met, the program will exit.
                    try:
                        arb = self.extractor.get_arbitrage_pair(symbol, level)
                    except Exception as e:
                        self.error_count += 1
                        if self.error_count >= self.max_error_count:
                            print("[ERROR] Number of exceptions exceeds the tolerance level (%d).\n%s" % 
                                    (self.max_error_count, e))
                            raise e
                        else:
                            continue
                    
                    if self.check_if_signal(arb, pair):
                        if arb[0].price > arb[1].price:
                            ratio = arb[0].price/arb[1].price - 1
                        else:
                            ratio = arb[1].price/arb[0].price - 1
                        ratio *= 100
                            
                        message = ("Arbitrage pair on %s [%.2f%%]:\n%s\n%s" % 
                                    (symbol, 
                                     ratio,
                                     arb[0], 
                                     arb[1]))
                        self.post(message)
                        
                    time.sleep(self.sleep_sec)
                    
        except Exception as e:
            self.post("CryptoMonitor is closed.")
            raise e
        finally:
            self.post("CryptoMonitor is closed.")