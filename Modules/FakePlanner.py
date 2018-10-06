import Class
import Tool
import random
from collections import deque
import Logger

logger = Logger.Logger("FakePlanner")
# player_ids_to_fake = [1421, 2563, 2011, 4033, 5842, 2835, 1125, 83, 2288, 594, 8487, 212, 4199, 2729, 3114]
player_ids_to_fake = [2288, 212]
player_ids_from_fake = [("3586", "15"), ("5015", "1"), ("3909", "1"), ("4212", "1"), ("164", "1"), ("3523", "1"),
                        ("5843", "1"), ("3666", "1"), ("3772", "1"), ("4086", "1"), ("9534", "1"), ("3675", "1"),
                        ("3618", "1"), ("3797", "1"), ("3848", "1"), ("3544", "15"), ("5421", "1"), ("4338", "1")]



def enter_work_account():
    email = 'email123@gmail.com'
    password = '1'
    player = Class.Player(email, password, 1)
    result = player.enter()
    logger.log(1, "enter_work_account", "account entered with result {}".format(result[0]))
    return player


class TargetsDeque:

    def __init__(self, llist):
        queue = deque(llist)
        self.queue = queue

    def is_empty(self):
        return len(self.queue) == 0

    def pop_few(self, n):
        items = []
        counter = 0
        while (not self.is_empty()) and counter < n:
            items.append(self.queue.pop())
            counter += 1
        return items

    def __len__(self):
        return len(self.queue)


class Faker:
    name = ''
    id = ''
    coefficient = ''
    link = ''

    def __init__(self, info, c, targets=None):
        player = info[1]['Data']['Player'][0]
        self.name = player['nick']
        self.id = player['id']
        self.coefficient = c
        self.calc_link()
        if targets is None:
            self.targets = []

    def calc_link(self):
        self.link = 'l+k://player?{}&193'.format(self.id)

    def print_envelope(self):
        env = 'Конверт {}\n{}\n\n'.format(self.name, self.link)
        env += 'Время: 04:00 МСК\n'
        env += 'Дата: 08/07\n'
        for target in self.targets:
            env += '{}\n{}\n\n'.format(target.name, target.link)
        env += '--------------------------------------------------'
        Tool.Sprint(env)

class Habitat:
    name = None
    link = None
    type = None
    points = None
    mapX = None
    mapY = None

    def __init__(self, info):
        habitat = info[1]['Data']['Habitat'][0]
        self.points = habitat['points']
        self.mapX = habitat['mapX']
        self.mapY = habitat['mapY']
        self.calc_type()
        self.calc_link()
        try:
            self.name = habitat['name']
        except KeyError:
            self.generate_name(habitat['id'])

    def calc_type(self):
        if int(self.points) in range(0, 1000):
            self.type = 'CAST'
        if int(self.points) in range(1000, 10000):
            self.type = 'FORT'
        if int(self.points) in range(10000, 100000):
            self.type = 'CITY'

    def calc_link(self):
        self.link = 'l+k://coordinates?{},{}&193'.format(self.mapX, self.mapY)

    def generate_name(self, hab_id):
        if self.type == 'CAST':
            self.name = 'Свободный замок {}'.format(hab_id)
        if self.type == 'FORT':
            self.name = 'Свободная крепость {}'.format(hab_id)
        if self.type == 'CITY':
            self.name = 'Свободный город {}'.format(hab_id)


def main():
    habitat_ids_to_fake = []
    habitats = []
    fakers = []
    player = enter_work_account()

    counter = 1
    for player_id_to_fake in player_ids_to_fake:
        info = player.player_info(player_id_to_fake)
        habitat_ids = info[1]['Data']['Player'][0]['habitatArray']
        habitat_ids_to_fake += habitat_ids
        player_name = info[1]['Data']['Player'][0]['nick']
        message = '{}/{}: Loaded habitats({}) of player called {}'.format(counter, len(player_ids_to_fake),len(habitat_ids), player_name)
        logger.log(0, "main", message)
        counter += 1

    counter = 1
    for habitat_id_to_fake in habitat_ids_to_fake:
        info = player.habitat_info(habitat_id_to_fake)
        try:
            habitat_name = info[1]['Data']['Habitat'][0]['name']
        except KeyError:
            habitat_name = "(ID: {})".format(info[1]['Data']['Habitat'][0]['id'])
        new_habitat = Habitat(info)
        habitats.append(new_habitat)
        message = '{}/{}: Loaded info of habitat called {}'.format(counter, len(habitat_ids_to_fake), habitat_name)
        logger.log(0, "main", message)
        counter += 1

    random.shuffle(habitats)

    counter = 1
    for faker in player_ids_from_fake:
        info = player.player_info(faker[0])
        player_name = info[1]['Data']['Player'][0]['nick']
        new_faker = Faker(info, faker[1])
        fakers.append(new_faker)
        message = '{}/{}: Loaded Faker called {}'.format(counter, len(player_ids_from_fake), player_name)
        logger.log(0, "main", message)
        counter += 1

    targets_deque = TargetsDeque(habitats)

    while not targets_deque.is_empty():
        for faker in fakers:
            faker.targets += targets_deque.pop_few(int(faker.coefficient))
            if targets_deque.is_empty():
                break

    for faker in fakers:
        message = '{} has {} targets'.format(faker.name, len(faker.targets))
        logger.log(0, "main", message)

    for faker in fakers:
        faker.print_envelope()
main()