import random
import re

import requests as _requests
requests = _requests.Session()

class TwitterCommand(object):

    command = 'larry'
    handle = 'lawrencemhwong'

    tweet_re = re.compile('<p\ class="js-tweet-text">(.*?)</p>')
    tags_re = re.compile('<[^>]*?>')

    def __call__(self, msg=None):
        response = requests.get('https://twitter.com/' + self.handle)
        matches = self.tweet_re.findall(response.text)
        if matches:
            match = random.choice(matches)
            return self.tags_re.sub('', match)

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


