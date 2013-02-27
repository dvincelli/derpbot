import requests
import random

class ImageCommand(object):
    command = 'image'

    def __call__(self, msg):
        query = self.parse(str(msg['body']))
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
            'safe': 'active',
        }
        response = requests.get('http://ajax.googleapis.com/ajax/services/search/images',
                                params=params)
        return response.json()

    def parse(self, body):
        return ' '.join(body.split(' ')[1:])
