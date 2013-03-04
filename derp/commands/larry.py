import random
import re
import HTMLParser

import requests as _requests
requests = _requests.Session()

class TwitterCommand(object):

    command = 'larry'
    handle = 'lawrencemhwong'

    tweet_re = re.compile('<p\ class="js-tweet-text">(.*?)</p>')
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

    def __call__(self, msg=None):
        return self.find_tweets(self.handle)

class TwitterHandleCommand(TwitterCommand):

    command = 'tweets'

    def __call__(self, msg):
        matches = msg['body'].split(' ')[1:]
        return self.find_tweets(' '.join(matches))


class OwenCommand(TwitterCommand):
    command = 'owen'
    handle = 'derspiny'

class JaneCommand(TwitterCommand):
    command = 'jane'
    handle = 'FreshAwake'

class AngrySheyCommand(TwitterCommand):
    command = 'shey'
    handle = 'AngryShey'

class NoxCommand(TwitterCommand):
    command = 'nox'
    handle = 'NoxDineen'

class SmoynesCommand(TwitterCommand):
    command = 'smoynes'
    handle = 'smoynes'

class DianaCommand(TwitterCommand):
    command = 'diana'
    handle = 'diana_clarke'

class CoeCommand(TwitterCommand):
    command = 'coe'
    handle = 'BenjaminCoe'


