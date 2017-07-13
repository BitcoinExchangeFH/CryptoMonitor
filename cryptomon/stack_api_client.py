#!/bin/python
from slacker import Slacker  

class SlackApiClient(Slacker):
    """
    Slack API client
    """
    USERNAME = 'cryptomonitor'
    
    def __init__(self, key, channel):
        """
        Constructor
        """
        Slacker.__init__(key)
        self.channel = channel
    
    def post_message(self, message):
        """
        Post message
        """
        self.chat.post_message(self.channel, message, username=SlackApiClient.USERNAME)
        

if __name__ == '__main__':
    key = '<key>'
    slack = Slacker(key)
    slack.chat.post_message('#arbsignal', 'Hello world!', username='cryptomonitor')