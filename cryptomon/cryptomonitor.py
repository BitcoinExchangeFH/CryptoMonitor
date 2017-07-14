#!/bin/python
from cryptomon.html_extractor import HtmlExtractor
from cryptomon.stack_api_client import SlackApiClient
from cryptomon.graceful_killer import GracefulKiller
from cryptomon.arbitrage_monitor import ArbitrageMonitor
import sys
import argparse
import time
import requests

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
                        default=30)       
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
    for pair in args.pair:
        if len(pair) != 2:
            print("[ERROR] First value is the symbol and the second value is the level.")
            parser.print_help()
            sys.exit(1)
        else:
            pair[1] = float(pair[1])
    
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
    killer = GracefulKiller()
    monitor = ArbitrageMonitor(pairs=args.pair,
                               killer=killer,
                               slack=slack,
                               extractor=extractor,
                               sleep_sec=args.sleep,
                               max_error_count=args.nerror)
    monitor.run()
        
if __name__ == '__main__':
    main()
        