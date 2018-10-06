from Class import Player
from Tool import Sprint, surrogate_decoding
import sqlite3
from datetime import datetime, timedelta


def main2():
    database_name = 'Database.db'
    conn = sqlite3.connect(database_name)
    conn.execute('DELETE FROM attack_fakes')
    conn.execute('DELETE FROM attack_fakes_transits')
    conn.commit()
    conn.close()


def calc_distance(x1, x2, y1, y2):

    if y1 & 1:
        _x1 = x1 + 0.5
    else:
        _x1 = x1
    if y2 & 1:
        _x2 = x2 + 0.5
    else:
        _x2 = x2

    _y1 = y1
    _y2 = y2

    xdif = abs(_x1 - _x2)
    ydif = abs(_y1 - _y2)

    if ydif * 0.5 >= xdif:
        return ydif
    else:
        return ydif * 0.5 + xdif


def alliance_ids_into_player_ids(alliance_id, account):
    result = account.alliance_info(alliance_id)
    return_data = [player['id'] for player in result[1]["Data"]['Player']]
    Sprint('<> Loaded {} players for alliance {}'.format(len(return_data), result[1]["Data"]['Alliance'][0]['name']))
    return return_data


def player_ids_into_habitat_ids(player_id, account):
    result = account.player_info(player_id)
    return_data = [habitat['id'] for habitat in result[1]["Data"]['Habitat']]
    Sprint('<> Loaded {} habitats for alliance {}'.format(len(return_data), result[1]["Data"]['Player'][0]['nick']))
    return return_data


def calc_arrival_time():
    time_now = datetime.now()
    days_2_delta = timedelta(days=2)
    time_in_2_days = time_now + days_2_delta
    return int(time_in_2_days.timestamp() * 1000)

def main():
    email = 'email123@gmail.com'
    password = '1'
    database_name = 'Database.db'
    account = Player(email, password, 0)
    account.smart_enter()

    alliance_ids = []  # '593'
    player_ids = ['3083']
    habitat_ids = []
    for alliance_id in alliance_ids:
        player_ids += alliance_ids_into_player_ids(alliance_id, account)
    for player_id in player_ids:
        habitat_ids += player_ids_into_habitat_ids(player_id, account)

    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    elza_player_id = 3992
    letitgo1_habitat_id = 18640
    letitgo1_x = 16502
    letitgo1_y = 16451
    attacker_players = '{};'.format(elza_player_id)
    index = 0
    for habitat_id in habitat_ids:
        habitat_info = account.habitat_info(habitat_id)
        alliance_id = int(habitat_info[1]["Data"]["Alliance"][0]["id"])
        alliance_name = habitat_info[1]["Data"]["Alliance"][0]["name"]
        arrival_time =calc_arrival_time()
        destination_id = int(habitat_info[1]["Data"]["Habitat"][0]["id"])
        try:
            destination_name = habitat_info[1]["Data"]["Habitat"][0]["name"]
        except KeyError:
            destination_name = 'Free Habitat {}'.format(destination_id)

        Sprint('{}/{}<> Loaded habitat {} info'.format(index, len(habitat_ids), destination_name))
        index += 1

        destination_x = int(habitat_info[1]["Data"]["Habitat"][0]["mapX"])
        destination_y = int(habitat_info[1]["Data"]["Habitat"][0]["mapY"])
        destination_points = int(habitat_info[1]["Data"]["Habitat"][0]["points"])
        public_type = str(4)
        destination_player_id = int(habitat_info[1]["Data"]["Player"][0]["id"])
        destination_player_nick = habitat_info[1]["Data"]["Player"][0]["nick"]
        units_players = attacker_players
        create_attack_statement = "INSERT INTO attack_fakes ('alliance_id', 'alliance_name', 'arrival_time', 'arrival_time_dispersion', 'attack_power', 'destination_habitat_id', 'destination_habitat_name', 'destination_habitat_map_x', 'destination_habitat_map_y', 'destination_habitat_points', 'destination_habitat_public_type', 'enabled', 'invader_id', 'invader_nick', 'join_attack', 'knocking_down', 'minimum_transits', 'player_id', 'player_attack_protection_end_date', 'player_is_on_vacation', 'player_nick', 'public_habitat_types', 'server_id', 'speculative_fire', 'travel_time_max', 'travel_time_min', 'units_players', 'units_types') VALUES({}, '{}', {}, 0, 1, {}, '{}', {}, {}, {}, '{}', -1, 0, '', 0, 0, 1, {}, 0, 0, '{}', '4;', 193, 0, 864000, 0, '{}', 'Offensive Common;Vikings;Siege Weapons;')".format(alliance_id, alliance_name, arrival_time, destination_id, destination_name, destination_x, destination_y, destination_points, public_type, destination_player_id, destination_player_nick, units_players)
        cursor.execute(surrogate_decoding(create_attack_statement))  # create attack
        attack_id = cursor.lastrowid

        distance = calc_distance(destination_x, destination_y, letitgo1_x, letitgo1_y)
        departure_time = calc_arrival_time() - (8 * 60 + 26) * 1000 * distance # 8min, 26sec for spearman
        create_transit_statement = "INSERT INTO attack_fakes_transits ('arrival_time_dispersion', 'departure_time', 'distance', 'knocking_down_transit', 'player_id', 'player_nick', 'server_id', 'source_habitat_id', 'source_habitat_name', 'source_habitat_public_type', 'status', 'sync_transit_id', 'units', 'attack_fake_id') VALUES(748, {}, {}, 0, {}, '{}', 193, {}, '{}', '4', 0, 0, '{}', {})".format(departure_time, distance, elza_player_id, 'ELZA', letitgo1_habitat_id, 'LET IT GO 1', '1=1;', attack_id)
        cursor.execute(create_transit_statement)
    conn.commit()
    conn.close()

main()