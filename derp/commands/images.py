import requests as _requests
import random
import time
import re

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
        response = requests.get('http://ajax.googleapis.com/ajax/services/search/images',
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
            print e

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

class AdultCommand(object):
    pattern = re.compile('like an adult', re.IGNORECASE)
    images = [
        "http://1.bp.blogspot.com/_D_Z-D2tzi14/TBpOnhVqyAI/AAAAAAAADFU/8tfM4E_Z4pU/s400/responsibility12(alternate).png",
        "http://2.bp.blogspot.com/_D_Z-D2tzi14/TBpOglLvLgI/AAAAAAAADFM/I7_IUXh6v1I/s400/responsibility10.png",
        "http://4.bp.blogspot.com/_D_Z-D2tzi14/TBpOY-GY8TI/AAAAAAAADFE/eboe6ItMldg/s400/responsibility11.png",
        "http://2.bp.blogspot.com/_D_Z-D2tzi14/TBpOOgiDnVI/AAAAAAAADE8/wLkmIIv-xiY/s400/responsibility13(alternate).png",
        "http://3.bp.blogspot.com/_D_Z-D2tzi14/TBpa3lAAFQI/AAAAAAAADFs/8IVZ-jzQsLU/s400/responsibility14.png",
        "http://3.bp.blogspot.com/_D_Z-D2tzi14/TBpoOlpMa_I/AAAAAAAADGU/CfZVMM9MqsU/s400/responsibility102.png",
        "http://4.bp.blogspot.com/_D_Z-D2tzi14/TBpoVLLDgCI/AAAAAAAADGc/iqux8px_V-s/s400/responsibility12(alternate)2.png",
        "http://2.bp.blogspot.com/_D_Z-D2tzi14/TBpqGvZ7jVI/AAAAAAAADGk/hDTNttRLLks/s400/responsibility8.png"
    ]
    def __call__(self, msg):
        return random.choice(self.images)

class BoogyCommand(object):
    command = 'boogy'
    images = [
        "http://www.vh1.com/celebrity/bwe/images/2011/09/Mister-Rogers-Dance-1316710648.gif"
    ]
    def __call__(self, msg):
        return random.choice(self.images)

class WatCommand(object):
    command = 'wat'
    links = [
        'http://i.imgur.com/QPtxtUG.gif',
        'http://i.imgur.com/3DQmFtG.jpeg',
        'http://i.imgur.com/4cRDoiZ.gif',
        'http://i.imgur.com/gyBkr.gif',
        'http://i.imgur.com/2xYGsuG.gif',
        'http://i.imgur.com/47k8P7I.jpg',
        'http://i.imgur.com/C8LE0.gif',
        'http://i.imgur.com/yrqr3qi.jpg',
        'http://i.imgur.com/0z7pboO.gif',
        'http://i.imgur.com/aOkyxdg.jpg',
        'http://i.imgur.com/OKdtaaB.gif',
        'http://i.imgur.com/S3yUoE0.gif',
        'http://i.imgur.com/YIGnwFp.gif',
        'http://i.imgur.com/xoOmhJC.gif',
        'http://i.imgur.com/Xs0twqW.jpg',
        'http://i.imgur.com/hByu9.gif',
        'http://i.imgur.com/rRcyf7t.gif',
        'http://i.imgur.com/YtmTXxW.gif',
        'http://i.imgur.com/wjfWfRP.jpg',
        'http://i.imgur.com/TGFOfJD.gif',
        'http://i.imgur.com/uBMDJtk.jpg'
    ]

    def __call__(self, msg):
        return random.choice(self.links)

class ImgurCommand(object):
    command = 'imgur'

    img_re = re.compile('src=\&quot;(.+?)\&quot;')

    def parse(self, body):
        return ' '.join(body.split(' ')[1:])

    def __call__(self, msg):
        keyword = self.parse(msg['body'])
        rss = requests.get('http://imgur.com/r/' + keyword + '/rss')
        images = self.img_re.findall(rss.text)
        return random.choice(images)

class GifBinCommand(object):
    command = 'gif'

    img_re = re.compile('<img src="([^"]+?)">')

    def __call__(self, msg):
        rss = requests.get('http://www.gifbin.com/feed/')
        images = self.img_re.findall(rss.text)
        return random.choice(images).replace('/tn_', '/')

