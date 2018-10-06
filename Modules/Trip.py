import Class
import time
import Tool
import random

def tripwire_real_detected(account, report_id, habitat_id):
    account.public_report(report_id)
    report_link = "l%2Bk://report?" + str(report_id) + "%26" + str(habitat_id) + "%26" + "174"
    message = report_link
    return account.send_message(message)


def funct1():
    while True:
        try:
            account = Class.Player("bantikru15@bk.ru", "130206")
            enter_result = account.gui_enter_account()[0]
            fetch_results = account.fetch_reports()[0]
            print(enter_result)
            print(fetch_results)
            reports = account.reports_result["Data"]["Report"]
            world_datetime = account.reports_result["time"]
            for report in reports:
                report_datetime = report["date"]
                if Tool.compare_GMT_time(world_datetime, report_datetime):
                    if report["type"] == "8" and "ownOffenderUnitDictionary" not in report["content"]:  # только доклады битв и только оборона
                        if Tool.losses_ratio_counter(report): # если в докладах битвы что то стоющее
                            res = tripwire_real_detected(account, report["id"], report["habitat"])
                            print("sent message for report {} with result {}".format(report["id"], res[1]))
                        else:
                            res = account.delete_report(report["id"])
                            print("deleted report {} with result {}".format(report["id"], res[0]))
            print("waiting 10 mins...\n")
            time.sleep(60 * 10)
        except:
            pass


def funct2():
    alliance_habitat_id_array = []
    account = Class.Player("bantikru15@bk.ru", "130206")
    players = []
    enter_account_result = account.gui_enter_account()

    alliance_info = account.get_alliance_info(355)
    players += alliance_info[1]["Data"]["Player"]

    alliance_info = account.get_alliance_info(378)
    players += alliance_info[1]["Data"]["Player"]

    alliance_info = account.get_alliance_info(775)
    players += alliance_info[1]["Data"]["Player"]

    for player in players:
        done = False
        while not done:
            player_info_result = account.get_player_info(player["id"])
            if player_info_result[0]:
                habitat_ids = player_info_result[1]["Data"]["Player"][0]["habitatArray"]
                alliance_habitat_id_array += habitat_ids
                #alliance_habitat_id_array += random.sample(habitat_ids, len(habitat_ids)//5)
                print(str(player["id"]) + " - player habitats added to list")
                done = True
            else:
                pass
                #time.sleep(0.5)
            #-----------alliance_habitat_id_array
    #  at this point we have all habitat id`s collected in alliance_habitat_id_array
    counter = 0
    excluded = []
    particularly_excluded = {1: [], 2: [], 3: [], 4: []}
    for habitat_unit in enter_account_result[1]["Data"]["HabitatUnit"]:
        if habitat_unit["battleType"] == "1" and habitat_unit["amount"] == "5" and (habitat_unit["unitId"] in ["1", "201", "102"]):
            excluded.append(habitat_unit["habitat"])
        if habitat_unit["battleType"] == "1" and (habitat_unit["unitId"] in ["1", "201", "102"]):
            if int(habitat_unit["amount"]) in particularly_excluded:
                particularly_excluded[int(habitat_unit["amount"])].append(habitat_unit["habitat"])
    #total_amount = len(alliance_habitat_id_array)
    transits = enter_account_result[1]["Data"]["Transit"]
    print(transits)
    needy_transits = []
    #needy_transits = [transit["destinationHabitat"] for transit in transits if (("unitDictionary" in transit) and ("1" in transit["unitDictionary"] and transit["unitDictionary"]["1"] in ["1", "2", "3", "4", "5"]) or ("102" in transit["unitDictionary"] and transit["unitDictionary"]["102"] in ["1", "2", "3", "4", "5"]) or ("201" in transit["unitDictionary"] and transit["unitDictionary"]["201"] in ["1", "2", "3", "4", "5"]))]
    for transit in transits:
        if "unitDictionary" in transit:
            if ("1" in transit["unitDictionary"] and transit["unitDictionary"]["1"] in ["1", "2", "3", "4", "5"]) or ("102" in transit["unitDictionary"] and transit["unitDictionary"]["102"] in ["1", "2", "3", "4", "5"]) or ("201" in transit["unitDictionary"] and transit["unitDictionary"]["201"] in ["1", "2", "3", "4", "5"]):
                needy_transits.append(transit["destinationHabitat"])

    #print(alliance_habitat_id_array)
    alliance_habitat_id_array = [element for element in alliance_habitat_id_array if (element not in excluded and element not in needy_transits)]
    total_amount = len(alliance_habitat_id_array)
    print(total_amount)
    for habitat_id in alliance_habitat_id_array:
        counter += 1
        if habitat_id in particularly_excluded[1]:
            trans_result = account.tripwire(habitat_id, "{1=4;}")
        elif habitat_id in particularly_excluded[2]:
            trans_result = account.tripwire(habitat_id, "{1=3;}")
        elif habitat_id in particularly_excluded[3]:
            trans_result = account.tripwire(habitat_id, "{1=2;}")
        elif habitat_id in particularly_excluded[4]:
            trans_result = account.tripwire(habitat_id, "{1=1;}")
        else:
            trans_result = account.tripwire(habitat_id, "{1=5;}")
        print(trans_result[0])
        if not trans_result[0]:
            print(trans_result[1])
        print("sent: " + str(habitat_id))

        print(str(counter) + "/" + str(total_amount))
        #print("estimating time left: " + str(int(total_amount - counter) * 8))
        print()
        #time_to_wait = random.randint(5, 9)
        #if trans_result[0]:
        #    time.sleep(time_to_wait)
        #else:
        #   time.sleep(2)


def funct3():
    account = Class.Player("frog@mail.ru", "daneg")
    result = account.gui_enter_account()
    for name in result[1]["Data"]["Habitat"]:
        print(name)


def funct4(unit_dic):
    habitat_id_to_use = None
    alliance_habitat_id_array = []
    account = Class.Player("chromebrutus3259@gmail.com", "3259")
    players = []
    enter_account_result = account.gui_enter_account()
    for element in enter_account_result[1]["Data"]["Player"]:
        if account.header_info["playerID"] == element["id"]:
            habitat_id_to_use = element["habitatArray"][0]

    alliance_info = account.get_alliance_info(593)
    players += alliance_info[1]["Data"]["Player"]
    alliance_info = account.get_alliance_info(2025)
    players += alliance_info[1]["Data"]["Player"]
    alliance_info = account.get_alliance_info(1147)
    players += alliance_info[1]["Data"]["Player"]
    alliance_info = account.get_alliance_info(1340)
    players += alliance_info[1]["Data"]["Player"]
    alliance_info = account.get_alliance_info(2159)
    players += alliance_info[1]["Data"]["Player"]
    alliance_info = account.get_alliance_info(1948)
    players += alliance_info[1]["Data"]["Player"]
    alliance_info = account.get_alliance_info(2800)
    players += alliance_info[1]["Data"]["Player"]
    alliance_info = account.get_alliance_info(1221)
    players += alliance_info[1]["Data"]["Player"]
    alliance_info = account.get_alliance_info(2134)
    players += alliance_info[1]["Data"]["Player"]
    alliance_info = account.get_alliance_info(1995)
    players += alliance_info[1]["Data"]["Player"]
    alliance_info = account.get_alliance_info(2158)
    players += alliance_info[1]["Data"]["Player"]
    alliance_info = account.get_alliance_info(2752)
    players += alliance_info[1]["Data"]["Player"]
    alliance_info = account.get_alliance_info(2108)
    players += alliance_info[1]["Data"]["Player"]
    alliance_info = account.get_alliance_info(2070)
    players += alliance_info[1]["Data"]["Player"]
    alliance_info = account.get_alliance_info(2110)
    players += alliance_info[1]["Data"]["Player"]
    alliance_info = account.get_alliance_info(2317)
    players += alliance_info[1]["Data"]["Player"]
    alliance_info = account.get_alliance_info(2204)
    players += alliance_info[1]["Data"]["Player"]
    alliance_info = account.get_alliance_info(2111)
    players += alliance_info[1]["Data"]["Player"]
    alliance_info = account.get_alliance_info(2130)
    players += alliance_info[1]["Data"]["Player"]
    alliance_info = account.get_alliance_info(2996)
    players += alliance_info[1]["Data"]["Player"]
    alliance_info = account.get_alliance_info(2606)
    players += alliance_info[1]["Data"]["Player"]
    alliance_info = account.get_alliance_info(2216)
    players += alliance_info[1]["Data"]["Player"]
    alliance_info = account.get_alliance_info(3170)
    players += alliance_info[1]["Data"]["Player"]
    alliance_info = account.get_alliance_info(2112)
    players += alliance_info[1]["Data"]["Player"]
    alliance_info = account.get_alliance_info(1987)
    players += alliance_info[1]["Data"]["Player"]
    alliance_info = account.get_alliance_info(2116)
    players += alliance_info[1]["Data"]["Player"]
    alliance_info = account.get_alliance_info(2847)
    players += alliance_info[1]["Data"]["Player"]
    alliance_info = account.get_alliance_info(2129)
    players += alliance_info[1]["Data"]["Player"]
    alliance_info = account.get_alliance_info(2913)
    players += alliance_info[1]["Data"]["Player"]
    alliance_info = account.get_alliance_info(2133)
    players += alliance_info[1]["Data"]["Player"]
    alliance_info = account.get_alliance_info(1891)
    players += alliance_info[1]["Data"]["Player"]
    alliance_info = account.get_alliance_info(3013)
    players += alliance_info[1]["Data"]["Player"]
    alliance_info = account.get_alliance_info(2454)
    players += alliance_info[1]["Data"]["Player"]
    alliance_info = account.get_alliance_info(2117)
    players += alliance_info[1]["Data"]["Player"]
    alliance_info = account.get_alliance_info(2465)
    players += alliance_info[1]["Data"]["Player"]
    alliance_info = account.get_alliance_info(2999)
    players += alliance_info[1]["Data"]["Player"]
    alliance_info = account.get_alliance_info(3015)
    players += alliance_info[1]["Data"]["Player"]
    alliance_info = account.get_alliance_info(3005)
    players += alliance_info[1]["Data"]["Player"]
    alliance_info = account.get_alliance_info(3195)
    players += alliance_info[1]["Data"]["Player"]
    alliance_info = account.get_alliance_info(2490)
    players += alliance_info[1]["Data"]["Player"]

    players.append({"id": "3405"})
    players.append({"id": "3944"})
    players.append({"id": "3406"})
    players.append({"id": "6326"})
    players.append({"id": "3391"})
    players.append({"id": "3399"})
    players.append({"id": "3395"})
    players.append({"id": "9577"})
    players.append({"id": "5180"})
    players.append({"id": "8167"})
    players.append({"id": "8166"})
    players.append({"id": "6467"})
    players.append({"id": "4587"})
    players.append({"id": "3035"})
    players.append({"id": "3541"})


    for player in players:
        done = False
        while not done:
            player_info_result = account.get_player_info(player["id"])
            if player_info_result[0]:
                if player_info_result[1]["Data"]["Player"][0]["isOnVacation"] == "false":
                    habitat_ids = player_info_result[1]["Data"]["Player"][0]["habitatArray"]
                    alliance_habitat_id_array += habitat_ids
                    #alliance_habitat_id_array += random.sample(habitat_ids, len(habitat_ids)//5)
                    print(str(player["id"]) + " - player habitats added to list")
                else:
                    print(str(player["id"]) + " - vacations")
                done = True
            else:
                pass
                #time.sleep(0.5)
            #-----------alliance_habitat_id_array
    random.shuffle(alliance_habitat_id_array)  # перемешивает массив игроков для эффектности 😈
    counter = 0
    total_amount = len(alliance_habitat_id_array)
    print(total_amount)
    for habitat_id in alliance_habitat_id_array:
        counter += 1
        #trans_result = account.send_spy(habitat_id)
        trans_result = account.rand_attack(habitat_id, unit_dic, habitat_id_to_use)
        # trans_result = account.send_spy(habitat_id, habitat_id_to_use)
        # send_spy
        #if counter < 1000:
        #    trans_result = account.rand_attack(habitat_id, "{102=1;}")
        #else:
        #    trans_result = account.rand_attack(habitat_id, "{2=1;}")  # unitDictionary: {1=коп;2=меч;101=лук;102=арб;}
        print(trans_result)
        print(str(counter) + "/" + str(total_amount))
        print("estimating time left: " + str(int((total_amount - counter) * (2 + 3) / 2)))
        print()
        time_to_wait = random.randint(2, 3)
        if trans_result[0]:
            print("sleeping {} seconds".format(time_to_wait))
            time.sleep(time_to_wait)
        else:
            time.sleep(1)


def funct5():
    alliance_habitat_id_array = []
    account = Class.Player("syjw@list.ru", "130206")
    players = []
    enter_account_result = account.gui_enter_account()
    # СП
    alliance_info = account.get_alliance_info(433)
    players += alliance_info[1]["Data"]["Player"]

    player_info_result = account.get_player_info(537)
    for key in player_info_result[1]["Data"]["Habitat"]:
        print(key)


def funct6():
    account = Class.Player("talt01@gmail.com", "passz")
    account.smart_enter()
    alliances_to_tripwire = []
    this_player_id = account.header_info['playerID']
    for player in account.login_result["Data"]["Player"]:
        if player["id"] == this_player_id:
            if "alliance" in player:
                alliances_to_tripwire.append(player["alliance"])
    for element in account.login_result["Data"]["Diplomacy"]:
        print(element)

#funct2()
#funct5()
#funct4("{1=1;}")
#funct4("{2=1;}")
#funct4("{101=1;}")
#funct6()

#unitDictionary: {1=1;102=2;201=3;} 1spear, 2crossbowmen, 3ahs


funct6()
