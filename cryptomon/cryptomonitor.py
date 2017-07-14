#!/bin/python
from cryptomon.html_extractor import HtmlExtractor
from cryptomon.stack_api_client import SlackApiClient
import sys
import argparse
import time

def main():
    parser = argparse.ArgumentParser(description='Cryptocurrency monitor.')
    parser.add_argument('-pair', 
                        action='append', 
                        dest='pair',
                        help='Symbol with an arbitrage level.',
                        nargs='+',
                        metavar=('symbol', 'value'))
    parser.add_argument('-nerror', 
                        action='store', 
                        dest='nerror',
                        help='Exception tolerance level.',
                        default=10)    
    parser.add_argument('-sleep', 
                        action='store', 
                        dest='sleep',
                        help='Sleep time between each request.',
                        default=10)       
    parser.add_argument('-key', 
                        action='store', 
                        dest='key',
                        help='Slack API key.')
    parser.add_argument('-channel', 
                        action='store', 
                        dest='channel',
                        help='Slack channel.',
                        default='#arbsignal')                        
                        
    args = parser.parse_args()
    
    if args.pair is None or len(args.pair) == 0:
        print("[ERROR] No symbol pair.")
        parser.print_help()
        sys.exit(1)
    
    #####################################################################################
    # Initialize variables
    print("Currency pairs:")
    for pair in args.pair:
        if len(pair) != 2:
            print("[ERROR] First value is the symbol and the second value is the level.")
            parser.print_help()
            sys.exit(1)
        else:
            pair[1] = float(pair[1])
            print("\tSymbol: %s, Level: %.2f%%" % (pair[0], pair[1] * 100))
    
    if args.key is None:
        print("[ERROR] Slack API key is mandatory.")
        parser.print_help()
        sys.exit(1)
    
    if args.channel is None or len(args.channel) == 0:
        print("[ERROR] Slack channel cannot be empty.")
        parser.print_help()
        sys.exit(1)
    elif args.channel[0] != '#':
        print("[ERROR] Slack channel must begin with #.")
        parser.print_help()
        sys.exit(1)
        
    if not isinstance(args.nerror, int):
        args.nerror = int(args.nerror)
        
    if not isinstance(args.sleep, int):
        args.sleep = int(args.sleep)
    
    
    #####################################################################################
    
    # Variables
    slack = SlackApiClient(args.key, args.channel)
    extractor = HtmlExtractor()
    error_count = 0
    arb_pairs = {}
    
    while True:
        for pair in args.pair:
            symbol = pair[0]
            level = pair[1]
            
            try:
                arb = extractor.get_arbitrage_pair(symbol, level)
            except Exception as e:
                error_count += 1
                if error_count >= args.nerror:
                    print("[ERROR] Number of exceptions exceeds the tolerance level (%d)." % 
                            (args.nerror))
                    raise e
                else:
                    continue
                    
            if arb is not None:
                signal_arb = False
                if symbol not in arb_pairs.keys():
                    signal_arb = True
                else:
                    prev_arb = arb_pairs[symbol]
                    if (prev_arb[0].exchange == arb[0].exchange and
                        prev_arb[0].pair == arb[0].pair and 
                        prev_arb[1].exchange == arb[1].exchange and
                        prev_arb[1].pair == arb[1].pair):
                        # Same as the previous arbitrage signal
                        signal_arb = False
                    else:
                        # Different from the previous arbitrage signal 
                        signal_arb = True
                        
                if signal_arb:
                    arb_pairs[symbol] = arb
                    # print("Arbitrage pair on %s:\n%s\n%s" % (symbol, arb[0], arb[1]))
                    slack.post_message("Arbitrage pair on %s:\n%s\n%s" % (symbol, arb[0], arb[1]))
                
            time.sleep(args.sleep)
    
        
if __name__ == '__main__':
    main()
        