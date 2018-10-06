import json
import requests
import urllib
import Data


class Telegram:
    """This class sends messages to main chat and some debug info to debug chat. There is only one debug and chat
    for messages can be chosen.
    """
    url = None
    last_update_id = None
    chat_id = None
    debug_chat_id = None

    def __init__(self, chat_id):
        self.url = "https://api.telegram.org/bot{}/".format(Data.telegram_token)
        self.chat_id = chat_id
        self.debug_chat_id = Data.tripwire_data["telegram_debug_chat_id"]
        self.check()

    def check(self):
        pass
        # look for some way to check if this chat exists and if not throw an error

    def send_message(self, text, debug=False):
        text = urllib.parse.quote_plus(text)
        if debug:
            chat_id = self.debug_chat_id
        else:
            chat_id = self.chat_id
        url = self.url + "sendMessage?text={}&chat_id={}".format(text, chat_id)
        return self._get_request()

    def get_updates(self, offset):
        url = self.url + "getUpdates"
        if offset:
            url += "?offset={}".format(offset)
        return self._get_json_request(url)

    def _get_request(self, url):
        response = requests.get(url)
        content = response.content.decode("utf8")
        return content

    def _get_json_request(self, url):
        content = self._get_request(url)
        js = json.loads(content)
        return js
