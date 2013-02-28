import requests as _requests
import random
import re

requests = _requests.Session()

class ImageCommand(object):
    command = 'image'
    safe_search = 'active'

    def __call__(self, msg):
        query = self.parse(msg['body'])
        return self.query_image(query)

    def query_image(self, query):
        try:
            images = self.google_image_search(query)
            images = images['responseData']['results']
            if images:
                return random.choice(images)['unescapedUrl'] + '#.png'
        except Exception as e:
            print e

    def google_image_search(self, query):
        params = {
            'v': '1.0',
            'rsz': '8',
            'q': query,
            'safe': self.safe_search,
        }
        response = requests.get('http://ajax.googleapis.com/ajax/services/search/images',
                                params=params)
        return response.json()

    def parse(self, body):
        return ' '.join(body.split(' ')[1:])

class HardcoreImageCommand(ImageCommand):
    command = 'hc'
    safe_search = 'off'

class ModerateImageCommand(ImageCommand):
    command = 'mod'
    safe_search = 'moderate'

class FixedImageCommand(ImageCommand):
    command = None

    def __call__(self, msg):
        return self.query_image(self.command)

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
