import websockets
from websockets.exceptions import ConnectionClosedError


TEXTSYNTH_WEBSOCKET_URL = "ws://163.172.76.10:8080/"


class TextSynthCommand:
    command = "textsynth"
    is_async = True

    socket_url = TEXTSYNTH_WEBSOCKET_URL

    def parse(self, msg):
        return msg['body'][len('!textsynth '):]

    async def __call__(self, msg):
        input_text = self.parse(msg)
        output_text = ""
        extra_headers = (('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/2019.04 Iridium/2019.04 Safari/537.36 Chrome/73.0.0.0'), ('Origin', 'http://textsynth.org'))

        async with websockets.connect(self.socket_url, extra_headers=extra_headers) as ws:
            await ws.send("g," + input_text)

            data = await ws.recv()
            while data != '':
                output_text += data
                try:
                    data = await ws.recv()
                except ConnectionClosedError:
                    break

            return input_text + output_text
