from Class import Player
import time
# DipSyncPixar3259@gmail.com
# DipSyncTale3259@gmail.com

def sync_diplo(diplo_from, id_from, id_to, account_to, diplo_to):
    if id_from == "":
        return
    print("syncing diplo from {} to {}".format(id_from, id_to))
    common_rel = ""
    if id_to != "":
        for element in diplo_from:
            if element["targetAlliance"] == id_to:
                common_rel = element["relationship"]
                result = account_to.set_diplo(id_from, common_rel)
                print("setting common rel result: {}".format(result[0]))
                del element
    for element in diplo_from:
        if element["targetAlliance"] == id_to:
            print("skipped common rel from 'from' to 'to'...")
            continue
        already_done = False
        for subelement in diplo_to:
            if subelement["targetAlliance"] == element["targetAlliance"] and subelement["relationship"] == element["relationship"]:
                already_done = True
        if not already_done:
            result = account_to.set_diplo(element["targetAlliance"], element["relationship"])[0]
            print(str(result) + " result for setting " + element["targetAlliance"])
            #time.sleep(1)
        else:
            print(element["targetAlliance"] + " - already done")


def read_diplo(email, password):
    account = Player(email, password, 0)
    while not account.smart_enter()[0]:
        print("oooops, relogining for email {} in 5 secs...".format(email))
        time.sleep(5)
    login_data = account.smart_enter()[1]
    diplomacy = []
    if "Diplomacy" in login_data["Data"]:
        diplomacy = login_data["Data"]["Diplomacy"]

    id = ""
    if len(diplomacy) > 0:
        id = diplomacy[0]["id"].split("-")[0]

    return diplomacy, id, account


def zero_to_diplo(account, diplo):
    for element in diplo:
        result = account.set_diplo(element["targetAlliance"], "0")
        print(str(result[0]) + " zeroing diplo for {}".format(element["targetAlliance"]))
# -1 - Enemy
# 0 - None
# 1 - NaP
# 2 - Ally
# 3 - Vassal



clone_from_diplo, clone_from_id, clone_from_account = read_diplo("elza_battle5_3259@gmail.com", "3259")
clone_to_diplo, clone_to_id, clone_to_account = read_diplo("crush_battle5_3259@gmail.com", "3259")
zero_to_diplo(clone_to_account, clone_to_diplo)
clone_from_diplo, clone_from_id, clone_from_account = read_diplo("elza_battle5_3259@gmail.com", "3259")
clone_to_diplo, clone_to_id, clone_to_account = read_diplo("crush_battle5_3259@gmail.com", "3259")

sync_diplo(clone_from_diplo, clone_from_id, clone_to_id, clone_to_account, clone_to_diplo)

clone_from_diplo, clone_from_id, clone_from_account = read_diplo("elza_battle5_3259@gmail.com", "3259")
clone_to_diplo, clone_to_id, clone_to_account = read_diplo("crush_battle5_3259@gmail.com", "3259")

sync_diplo(clone_from_diplo, clone_from_id, clone_to_id, clone_to_account, clone_to_diplo)
# crush


clone_from_diplo, clone_from_id, clone_from_account = read_diplo("elza_battle5_3259@gmail.com", "3259")
clone_to_diplo, clone_to_id, clone_to_account = read_diplo("heimlich_battle5_3259@gmail.com", "3259")
zero_to_diplo(clone_to_account, clone_to_diplo)
clone_from_diplo, clone_from_id, clone_from_account = read_diplo("elza_battle5_3259@gmail.com", "3259")
clone_to_diplo, clone_to_id, clone_to_account = read_diplo("heimlich_battle5_3259@gmail.com", "3259")

sync_diplo(clone_from_diplo, clone_from_id, clone_to_id, clone_to_account, clone_to_diplo)

clone_from_diplo, clone_from_id, clone_from_account = read_diplo("elza_battle5_3259@gmail.com", "3259")
clone_to_diplo, clone_to_id, clone_to_account = read_diplo("heimlich_battle5_3259@gmail.com", "3259")

sync_diplo(clone_from_diplo, clone_from_id, clone_to_id, clone_to_account, clone_to_diplo)


clone_from_diplo, clone_from_id, clone_from_account = read_diplo("elza_battle5_3259@gmail.com", "3259")
clone_to_diplo, clone_to_id, clone_to_account = read_diplo("bloat_battle5_3259@gmail.com", "3259")
zero_to_diplo(clone_to_account, clone_to_diplo)
clone_from_diplo, clone_from_id, clone_from_account = read_diplo("elza_battle5_3259@gmail.com", "3259")
clone_to_diplo, clone_to_id, clone_to_account = read_diplo("bloat_battle5_3259@gmail.com", "3259")

sync_diplo(clone_from_diplo, clone_from_id, clone_to_id, clone_to_account, clone_to_diplo)

clone_from_diplo, clone_from_id, clone_from_account = read_diplo("elza_battle5_3259@gmail.com", "3259")
clone_to_diplo, clone_to_id, clone_to_account = read_diplo("bloat_battle5_3259@gmail.com", "3259")

sync_diplo(clone_from_diplo, clone_from_id, clone_to_id, clone_to_account, clone_to_diplo)
# crush