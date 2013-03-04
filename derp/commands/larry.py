import random
import re

import requests as _requests
requests = _requests.Session()

class LarryCommand(object):

    command = 'larry'
    tweet_re = re.compile('<p\ class="js-tweet-text">(.*?)</p>')
    tags_re = re.compile('<[^>]*?>')

    def __call__(self, msg=None):
        response = requests.get('https://twitter.com/lawrencemhwong')
        matches = self.tweet_re.findall(response.text)
        if matches:
            match = random.choice(matches)
            return self.tags_re.sub('', match)


