from Class import Player
import time
import os
from Tool import additional_surrogate_decoding


class KeyBase:
    folder_path = 'KeyBase'
    work_account_email = None
    work_account_password = None
    keys = []

    def read_all_keys(self):
        for path, dirs, files in os.walk(self.folder_path):
            for file_name in files:
                with open("{}/{}".format(path, file_name)) as file:
                    print(file.read())



    def write_all_keys(self):
        pass

    def add_new_key(self):
        pass

    def is_account_valid(self):
        pass


class Key:
    player_comment = None
    player_real_name = None
    player_telegram_name = None
    player_telegram_chat_id = None
    account_id = None
    account_link = None
    account_name = None
    email = None
    password = None
    points = None
    cast_amount = 0
    fort_amount = 0
    city_amount = 0
    alliance_id = None
    alliance_link = None
    alliance_name = None
    account = None

    def create_new(self, email, password, player_comment, player_real_name, player_telegram_name, player_telegram_chat_id):
        self.email = email
        self.password = password
        self.player_comment = player_comment
        self.player_real_name = player_real_name
        self.player_telegram_chat_id = player_telegram_chat_id
        self.player_telegram_name = player_telegram_name
        result = self.login()
        self.parse_result(result)

    def read_from_file(self, full_path):
        with open(full_path) as file:
            data = file.read().split("<SPLITTER>")
            (self.email, self.password, self.player_comment, self.player_real_name, self.player_telegram_name,
             self.player_telegram_chat_id, self.account_id, self.account_link, self.account_name, self.points,
             self.cast_amount, self.fort_amount, self.city_amount, self.alliance_id, self.alliance_name,
             self.alliance_link) = data

    def login(self):
        secs_before_retry = 10
        self.account = Player(self.email, self.password)
        done = False
        while not done:
            result = self.account.enter_account()
            done = result[0]
            if done:
                print("entering account {} succeeded".format(self.account.email))
                return result
            else:
                print("entering account {} not succeeded, retry in {} sec".format(self.account.email, secs_before_retry))
                print("error message is: {}".format(result[1]))
                time.sleep(secs_before_retry)

    def parse_result(self, result):
        self.account_id = self.account.header_info["playerID"]
        self.account_link = "l+k://player?{}&193".format(self.account_id)
        for player in result[1]["Data"]["Player"]:

            if player["id"] == self.account_id:

                self.account_name = additional_surrogate_decoding(player["nick"])
                self.points = player["points"]

                if "Habitat" in result[1]["Data"]:
                    for habitat in result[1]["Data"]["Habitat"]:
                        if habitat["player"] == self.account_id:
                            if habitat["points"] in range(13, 1000):
                                self.cast_amount += 1
                            if habitat["points"] in range(1000, 2000):
                                self.fort_amount += 1
                            if habitat["points"] in range(10000, 20000):
                                self.city_amount += 1
                else:
                    print("Couldn't load habitats, left as 0s")

                if "alliance" in player:
                    self.alliance_id = player["alliance"]
                    if "Alliance" in result[1]["Data"]:
                        for alliance in result[1]["Data"]["Alliance"]:
                            if alliance["id"] == self.alliance_id:
                                self.alliance_name = additional_surrogate_decoding(alliance["name"])
                                self.alliance_link = "l+k://alliance?{}&193".format(self.alliance_id)
                    else:
                        print("couldn't load alliance, left Nones")
                else:
                    print("Player has no alliance")

    def __str__(self):
        string = "Name: {}\nLink: {}\nAlliance: {}\nAlliance link: {}\nEmail: {}\nPassword: {}\nPlayer Name: {}\n Player Telegram Name: {}\nChat ID:: {}\nComment: {}\n"
        return string.format(
            self.account_name, self.account_link,
            self.alliance_name, self.alliance_id,
            self.email, self.password,
            self.player_real_name, self.player_telegram_name,
            self.player_telegram_chat_id, self.player_comment
        )
        return string



def main():
    # test_key = Key("email123@gmail.com", "1", "comment replacement", 'realnameVasyyyaaaa', "ptelegramname", "chatid")
    # test_key.create_new("email123@gmail.com", "1", "comment replacement", 'realnameVasyyyaaaa', "ptelegramname", "chatid")
    # print(test_key)
    key_base = KeyBase()
    key_base.read_all_keys()


main()