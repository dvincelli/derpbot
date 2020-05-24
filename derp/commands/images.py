import requests as _requests
import random
import time
import re
import logging


logger = logging.getLogger(__name__)


requests = _requests.Session()


class ImageCommand(object):
    command = "image"
    safe_search = "strict"

    def parse(self, body):
        return " ".join(body.split(" ")[1:])

    def _encode_safe_search(self, safe_search):
        if safe_search == "off":
            return "0"
        elif safe_search == "moderate":
            return "1"
        elif safe_search == "strict":
            return "2"

    def qwant_image_search(self, query, start=0):
        params = {
            "uiv": "4",
            "locale": "en_US",
            "q": query,
            "t": "image",
            "count": 10,
            "safe_search": self._encode_safe_search(self.safe_search),
            "offset": start,
            "f": "",
        }
        # TODO: support other search types:
        #   "web", "images", "news", "social", "videos", "music"
        response = requests.get(
            "https://api.qwant.com/api/search/images",
            params=params,
            headers={
                "User-Agent": 'Mozilla/5.0 (X11; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0'
            }
        )
        results = response.json().get('data', {}).get('result', {}).get('items', [])
        return results

    def query_image(self, query, random_result=False):
        try:
            images = self.qwant_image_search(query)
            # TODO:
            # 
            # Random result from later page:
            #   1st search: get the number of results
            #   2nd search: get result page and a random result from that page
            #   But it should be done optionally
            # 
            # This is code that worked with google a few years ago
            # start = random.choice(images["responseData"]["cursor"]["pages"])["start"]
            # images = self.qwant_image_search(query, start)
            if images:
                if random_result:
                    path = random.choice(images)["media_fullsize"] # + "#.png"
                else:
                    path = images[0]["media_fullsize"] # + "#.png"
                return 'https:' + path
        except Exception as e:
            logger.exception(str(e))

    def __call__(self, msg):
        query = self.parse(msg["body"])
        return self.query_image(query)


class ImgCommand(ImageCommand):
    command = "img"


class HardcoreImageCommand(ImageCommand):
    command = "hc"
    safe_search = "off"

    def __call__(self, msg):
        if 9 <= int(time.strftime("%H")) <= 18:
            self.safe_search = random.choice(["moderate", "strict"])
        else:
            self.safe_search = "off"
        query = self.parse(msg["body"])
        return self.query_image(query)


class ModerateImageCommand(ImageCommand):
    command = "mod"
    safe_search = "moderate"


class FixedImageCommand(ImageCommand):
    command = None

    def __call__(self, msg):
        return self.query_image(self.command)


class KittyImage(FixedImageCommand):
    command = "kitty"


class KittiesImage(FixedImageCommand):
    command = "kitties"


class KittenImage(FixedImageCommand):
    command = "kitten"


class KittensImage(FixedImageCommand):
    command = "kittens"


class CatImage(FixedImageCommand):
    command = "cat"


class CatsImage(FixedImageCommand):
    command = "cats"


class PugImage(FixedImageCommand):
    command = "pug"


class PugsImage(FixedImageCommand):
    command = "pugs"


class AwwImage(FixedImageCommand):
    command = "aww"

    def __call__(self, msg):
        return self.query_image("/r/aww")


class RandomImage(ImageCommand):
    command = "random"

    def __call__(self, msg):
        query = random.choice(open("/usr/share/dict/words").readlines())
        return self.query_image(query)


class SlothImage(FixedImageCommand):
    command = "sloth"


class SlothsImage(FixedImageCommand):
    command = "sloths"


class SlothBucketImage(FixedImageCommand):
    command = "slothbucket"


class PuppyImage(FixedImageCommand):
    command = "puppy"


class PuppiesImage(FixedImageCommand):
    command = "puppies"


class ImgurCommand(object):
    command = "imgur"

    img_re = re.compile('src="//i.imgur.com/(.+?)"')

    def parse(self, body):
        return " ".join(body.split(" ")[1:])

    def __call__(self, msg):
        keyword = self.parse(msg["body"])
        rss = requests.get("https://imgur.com/r/" + keyword)
        images = self.img_re.findall(rss.text)
        return f"https://i.imgur.com/{random.choice(images)}"


class GifBinCommand(object):
    command = "gif"

    img_re = re.compile('<img src="([^"]+?)">')

    def __call__(self, msg):
        rss = requests.get("http://www.gifbin.com/feed/")
        images = self.img_re.findall(rss.text)
        return random.choice(images).replace("/tn_", "/")


class JjDotAmCommand(object):
    command = "jj"

    img_re = re.compile(
        '<img border="0" src="((http://forgifs.com/gallery/./)([\\d]+?-[\\d])/([^"]+?))"'
    )

    def __call__(self, msg):
        rss = requests.get("http://forgifs.com/gallery/srss/7")
        images = self.img_re.findall(rss.text)
        url, base_url, num, filename = random.choice(images)
        if num.endswith("-2"):
            base, term = num.split("-")
            base, term = int(base), int(term)
            base -= 1
            term = 1
            new_num = str(base) + "-" + str(term)
            return "".join([base_url, new_num, "/", filename])
        else:
            return "".join([base_url, num, "/", filename])


class ForGifsCommand(object):

    command = "4gifs"

    img_re = re.compile('&lt;img src="([^"]+?)"/&gt;')

    def __call__(self, msg):
        rss = requests.get("http://4gifs.tumblr.com/rss")
        images = self.img_re.findall(rss.text)
        return random.choice(images)


class CringeCommand(ImgurCommand):
    command = "cringe"

    def __call__(self, msg):
        msg["body"] = "!imgur cringepics"
        return ImgurCommand.__call__(self, msg)
