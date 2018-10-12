import WorldAccount
import time
from collections import deque
import threading
import Tool


accounts_data = [
    ["email123@gmail.com", "1"],
    ["fir.danya2@mail.ru", "1"],
    ["fir.danya3@mail.ru", "1"],
    ["fir.danya4@mail.ru", "1"],
    ["fir.danya5@mail.ru", "1"],
    ["fir.danya6@mail.ru", "1"],
]


def load_topic():
    with open("topic.txt", "r") as file:
        content = file.read()
    return content


def load_message():
    with open("message.txt", "r") as file:
        content = file.read()
    return content


def test_message_on_myself():
    pass


def main():
    #our_alliances = ["611", "835", "824", "2899", "1867", "3063", "815", "121", "2010", "2034", "2044", "3084", "882", "2995"]
    our_alliances = []
    topic = load_topic()
    message = load_message()
    if len(accounts_data) == 0:
        raise ValueError("Need at least one accounts to work")
    entered_accounts = enter_all_accounts(accounts_data)
    root_account = entered_accounts[0]
    alliances_data = load_all_alliances(root_account)
    alliance_ids = [alliance_id["id"] for alliance_id in alliances_data[1]["allianceRanks"]]
    alliance_ids = [alliance_id for alliance_id in alliance_ids if alliance_id not in our_alliances]
    players_data = alliance_to_player(root_account, alliance_ids)
    player_ids = [player_id["id"] for player_id in players_data]
    print(player_ids)
    print(topic)
    print(message)
    send_all_messages(player_ids, entered_accounts, topic, message, players_data)
    # root_account.create_message(topic, "3586", message)  # for testing message


def enter_all_accounts(accounts_data_inn):
    accounts = []
    for account_data_one in accounts_data_inn:
        account = WorldAccount.WorldAccount(account_data_one[0], account_data_one[1])
        account.smart_enter()
        accounts.append(account)
    return accounts


def alliance_to_player(account, alliance_ids):
    all_players = []
    print("alliances: {}".format(alliance_ids))
    for alliance_id in alliance_ids:
        done = False
        while not done:
            result = account.alliance_info(alliance_id)
            done = result[0]
            if done:
                print("loading players for alliance {} succeeded".format(alliance_id))
                all_players += result[1]["Data"]["Player"]
            else:
                print("loading players for alliance {} not succeeded".format(alliance_id))
                account.smart_enter()
    return all_players


def load_all_alliances(player):
    done = False
    while not done:
        result = player.load_alliance_rating()
        done = result[0]
        if done:
            print("loading rating by {} succeeded".format(player.email))
            return result
        else:
            print("loading rating by {} not succeeded, retry in 5 sec".format(player.email))
            time.sleep(5)


class SendThread(threading.Thread):

    def __init__(self, account, idd, topic, content, nick):
        threading.Thread.__init__(self)
        self.id = idd
        self.topic = topic
        self.account = account
        self.content = content
        self.nick = nick

    def run(self):
        done = False
        while not done:
            result = self.account.create_message(self.topic, self.id, self.content)
            done = result[0]
            if done:
                Tool.Sprint("sending message from {} to player {} succeeded".format(self.account.email, self.nick))
                self.account.available = True
                return result
            else:
                Tool.Sprint("sending message from {} to player {} not succeeded".format(self.account.email, self.nick))
                time.sleep(5)


def send_all_messages(player_ids, accounts, topic, content, players_data):
    queue = deque()
    for player_id in player_ids:
        queue.append(player_id)
    while queue:
        for account in accounts:
            if account.available or account.available is None:
                if queue:
                    next_player = queue.pop()
                    print("players remaining: {}".format(len(queue)))
                else:
                    continue
                account.available = False
                player_nick = player_name_by_id(players_data, next_player)
                new_thread = SendThread(account, next_player, topic, content, player_nick)
                new_thread.start()
        print("no iddle accounts, waiting")
        time.sleep(0.1)


def player_name_by_id(players_data, player_id):
    for player in players_data:
        if player["id"] == player_id:
            return player["nick"]
    return "has no name"


main()
