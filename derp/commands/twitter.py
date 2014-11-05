import random
import re
import HTMLParser

import requests as _requests
requests = _requests.Session()

class TwitterCommand(object):

    command = 'tweets'

    tweet_re = re.compile('<p\ class="js-tweet-text tweet-text">(.*?)</p>')
    tags_re = re.compile('<[^>]*?>')

    def decode_entities(self, string):
        html_parser = HTMLParser.HTMLParser()
        return html_parser.unescape(string)

    def find_tweets(self, handle):
        response = requests.get('https://twitter.com/' + handle)
        matches = self.tweet_re.findall(response.text)
        if matches:
            match = random.choice(matches)
            return self.decode_entities('@' + handle + ':' + self.tags_re.sub('', match))

    def __call__(self, msg):
        handle = ' '.join(msg['body'].split(' ')[1:])
        return self.find_tweets(handle)

class TwitterHandleCommand(TwitterCommand):

    command = None
    handle = 'twitter'

    def __call__(self, msg):
        return self.find_tweets(self.handle)


class FmlCommand(TwitterHandleCommand):
    command = 'fml'
    handle = 'fml'


class DevopsCommand(TwitterHandleCommand):
    command = 'devops'
    handle = 'devops_borat'

class HulkCommand(TwitterHandleCommand):
    command = 'hulk'
    handle = 'DBAHULK'
