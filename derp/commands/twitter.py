import random
import re
from html.parser import HTMLParser

import lxml.html
from lxml.cssselect import CSSSelector

import requests as _requests


requests = _requests.Session()


class TwitterCommand:
    command = "tweets"

    def find_tweets(self, handle):
        response = requests.get("https://twitter.com/" + handle)
        tree = lxml.html.fromstring(response.text)
        sel = CSSSelector("div.js-tweet-text-container p")
        results = sel(tree)
        return random.choice([result.text for result in results])

    def __call__(self, msg):
        handle = " ".join(msg["body"].split(" ")[1:])
        return self.find_tweets(handle)


class TwitterHandleCommand(TwitterCommand):

    command = None
    handle = "twitter"

    def __call__(self, msg):
        return self.find_tweets(self.handle)


class FmlCommand(TwitterHandleCommand):
    command = "fml"
    handle = "fml"


class DevopsCommand(TwitterHandleCommand):
    command = "devops"
    handle = "devops_borat"


class HulkCommand(TwitterHandleCommand):
    command = "hulk"
    handle = "DBAHULK"
