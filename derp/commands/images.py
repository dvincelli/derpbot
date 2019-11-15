import requests as _requests
import random
import time
import re
import logging


logger = logging.getLogger(__name__)


requests = _requests.Session()

class ImageCommand(object):
    command = 'image'
    safe_search = 'active'

    def parse(self, body):
        return ' '.join(body.split(' ')[1:])

    def google_image_search(self, query, start=0):
        params = {
            'v': '1.0',
            'rsz': '8',
            'q': query,
            'safe': self.safe_search,
            'start': start
        }
        response = requests.get('https://ajax.googleapis.com/ajax/services/search/images',
                                params=params)
        return response.json()

    def query_image(self, query):
        try:
            images = self.google_image_search(query)
            start = random.choice(images['responseData']['cursor']['pages'])["start"]
            images = self.google_image_search(query, start)
            images = images['responseData']['results']
            if images:
                return random.choice(images)['unescapedUrl'] + '#.png'
        except Exception as e:
            logger.error(e)

    def __call__(self, msg):
        query = self.parse(msg['body'])
        return self.query_image(query)

class ImgCommand(ImageCommand):
    command = 'img'

class HardcoreImageCommand(ImageCommand):
    command = 'hc'
    safe_search = 'off'

    def __call__(self, msg):
        if 9 <= int(time.strftime('%H')) <= 18:
            self.safe_search = random.choice(['moderate', 'active'])
        else:
            self.safe_search = 'off'
        query = self.parse(msg['body'])
        return self.query_image(query)

class ModerateImageCommand(ImageCommand):
    command = 'mod'
    safe_search = 'moderate'

class FixedImageCommand(ImageCommand):
    command = None

    def __call__(self, msg):
        return self.query_image(self.command)

class KittyImage(FixedImageCommand):
    command = 'kitty'

class KittiesImage(FixedImageCommand):
    command = 'kitties'

class KittenImage(FixedImageCommand):
    command = 'kitten'

class KittensImage(FixedImageCommand):
    command = 'kittens'

class CatImage(FixedImageCommand):
    command = 'cat'

class CatsImage(FixedImageCommand):
    command = 'cats'

class PugImage(FixedImageCommand):
    command = 'pug'

class PugsImage(FixedImageCommand):
    command = 'pugs'

class AwwImage(FixedImageCommand):
    command = 'aww'

    def __call__(self, msg):
        return self.query_image('/r/aww')

class RandomImage(ImageCommand):
    command = 'random'

    def __call__(self, msg):
        query = random.choice(open("/usr/share/dict/words").readlines())
        return self.query_image(query)

class SlothImage(FixedImageCommand):
    command = 'sloth'

class SlothsImage(FixedImageCommand):
    command = 'sloths'

class SlothBucketImage(FixedImageCommand):
    command = 'slothbucket'

class PuppyImage(FixedImageCommand):
    command = 'puppy'

class PuppiesImage(FixedImageCommand):
    command = 'puppies'


class ImgurCommand(object):
    command = 'imgur'

    img_re = re.compile('src="//i.imgur.com/(.+?)"')

    def parse(self, body):
        return ' '.join(body.split(' ')[1:])

    def __call__(self, msg):
        keyword = self.parse(msg['body'])
        rss = requests.get('https://imgur.com/r/' + keyword)
        images = self.img_re.findall(rss.text)
        return f'https://i.imgur.com/{random.choice(images)}'


class GifBinCommand(object):
    command = 'gif'

    img_re = re.compile('<img src="([^"]+?)">')

    def __call__(self, msg):
        rss = requests.get('http://www.gifbin.com/feed/')
        images = self.img_re.findall(rss.text)
        return random.choice(images).replace('/tn_', '/')

class JjDotAmCommand(object):
    command = 'jj'

    img_re = re.compile('<img border="0" src="((http://forgifs.com/gallery/./)(\d+?-\d)/([^"]+?))"')

    def __call__(self, msg):
        rss = requests.get('http://forgifs.com/gallery/srss/7')
        images = self.img_re.findall(rss.text)
        url, base_url, num, filename = random.choice(images)
        if num.endswith('-2'):
            base, term = num.split('-')
            base, term = int(base), int(term)
            base -= 1
            term = 1
            new_num = str(base) + '-' + str(term)
            return ''.join([base_url, new_num, '/', filename])
        else:
            return ''.join([base_url, num, '/', filename])

class ForGifsCommand(object):

    command = '4gifs'

    img_re = re.compile('&lt;img src="([^"]+?)"/&gt;')

    def __call__(self, msg):
        rss = requests.get('http://4gifs.tumblr.com/rss')
        images = self.img_re.findall(rss.text)
        return random.choice(images)

class CringeCommand(ImgurCommand):
    command = 'cringe'

    def __call__(self, msg):
        msg['body'] = '!imgur cringepics'
        return ImgurCommand.__call__(self, msg)
