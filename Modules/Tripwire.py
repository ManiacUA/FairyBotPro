import WorldAccount
import Tool
import Data
import time
from Telegram import Telegram
telegram = Telegram()
import Logger
logger = Logger.Logger("Tripwire")
from Entities.Report import Report

def main(email, password):
    account = WorldAccount.WorldAccount(email, password, 1)
    login_result = account.smart_enter()
    counter = 2  # times to replace tripwires
    while True:
        reports_to_public_list, reports_to_delete_list = get_new_reports(account)
        delete_reports(account, reports_to_delete_list)
        reports_to_message_list = public_reports(account, reports_to_public_list)
        message_reports(account, reports_to_message_list, Data.tripwire_data["discussion_id"])

        print("\t" * 1 + "counter: {}".format(counter))
        if counter == 0:
            counter = int(8 * 60 / Data.tripwire_data["minutes_between_check"])
            print("\t" * 1 + "tripwires refresh needed")
            refresh_tripwires(account)
        else:
            print("\t" * 1 + "tripwires refresh not needed")
            counter -= 1

        print("\t" * 0 + "sleeping")
        time.sleep(60 * Data.tripwire_data["minutes_between_check"])


def get_this_player_habitats(account, login_result):
    for player in login_result[1]["Data"]["Player"]:
        if "habitatArray" in player and "id" in player:
            if account.header_info["playerID"] == player["id"]:
                return player["habitatArray"]
    return []

def alliance_ids_to_tripwire(login_result):
    pass
    #load id of your alliance
    # select diplo with orange colour


def player_to_habitat(account, player_ids):
    habitat_id_array = []
    counter = 1
    for player in player_ids:
        print("\t" * 4 + "player {}/{}".format(counter, len(player_ids)))
        counter += 1
        done = False
        while not done:
            player_info_result = account.get_player_info(player["id"])
            done = player_info_result[0]
            if done:
                habitat_id_array += player_info_result[1]["Data"]["Player"][0]["habitatArray"]
            else:
                account.smart_enter()
    print("\t" * 4 + "habitats amount: {}".format(len(habitat_id_array)))
    return habitat_id_array


def alliance_to_player(account, alliance_ids=Data.alliance_ids_to_tripwire):
    all_players = []
    print("\t" * 4 + "alliances: {}".format(alliance_ids))
    for alliance_id in alliance_ids:
        done = False
        while not done:
            result = account.get_alliance_info(alliance_id)
            done = result[0]
            if done:
                all_players += result[1]["Data"]["Player"]
            else:
                account.smart_enter()
    return all_players


def get_info_tripwires(account, login_result):
    print("\t" * 3 + "converting alliance ids to player ids")
    player_id_array = alliance_to_player(account)
    print("\t" * 3 + "alliance ids to player ids converted")
    print("\t" * 3 + "converting player ids to habitat ids")
    habitat_id_array = player_to_habitat(account, player_id_array)
    print("\t" * 3 + "player ids to habitat ids converted")

    change_troops_dict = {}
    this_player_habitats_id_list = get_this_player_habitats(account, login_result)

    print("\t" * 3 + "this players habitats: {}".format(this_player_habitats_id_list))

    #for player in login_result[1]["Data"]["Player"]:
    #    if player["id"] == account.header_info["playerID"]:
    #        Data.trips_source = player["habitatArray"][0]
    #        break
    print("\t" * 3 + "selected source habitat: {}".format(Data.tripwire_data["trips_source"]))

    for habitat_id in habitat_id_array:
        if habitat_id in this_player_habitats_id_list:
            continue
        change_troops_dict[habitat_id] = Data.tripwire_data["default_tripwire_size"]

    for habitat_unit in login_result[1]["Data"]["HabitatUnit"]:
        if habitat_unit["battleType"] != "1":
            continue

        if habitat_unit["habitat"] in change_troops_dict:
            change_troops_dict[habitat_unit["habitat"]] -= int(habitat_unit["amount"])
            if change_troops_dict[habitat_unit["habitat"]] == 0:
                del change_troops_dict[habitat_unit["habitat"]]

    try:
        transits = login_result[1]["Data"]["Transit"]
    except KeyError:
        print("no transits found")
        transits = []

    for transit in transits:
        if transit["transitType"] == "0" and "1" in transit["unitDictionary"]:  # sent defence
            if transit["destinationHabitat"] in change_troops_dict:
                sum_troops_sent = int(transit["unitDictionary"]["1"])
                change_troops_dict[transit["destinationHabitat"]] -= sum_troops_sent
                if change_troops_dict[transit["destinationHabitat"]] == 0:
                    del change_troops_dict[transit["destinationHabitat"]]
    print("\t" * 3 + "amount of changes to make: {}".format(len(change_troops_dict)))
    return change_troops_dict


def refresh_tripwires(account):
    print("\t" * 2 + "relogging for new info")
    login_result = account.smart_enter()
    print("\t" * 2 + "relogged for new info")
    print("\t" * 2 + "getting tripwires info")
    habitat_trips = get_info_tripwires(account, login_result)
    print("\t" * 2 + "tripwires info gotten")
    trip_counter = 0
    for habitat_trip in habitat_trips:
        #time.sleep(3)
        trip_counter += 1
        print("\t" * 2 + "{}/{}: ".format(trip_counter, len(habitat_trips)), end="")
        if habitat_trips[habitat_trip] > 0:
            unit_dictionary = "{1=" + str(habitat_trips[habitat_trip]) + ";}"
            counter = 1
            while counter > 0:
                result = account.support(habitat_trip, unit_dictionary, Data.tripwire_data["trips_source"])
                if result[0]:
                    counter = 0
                    print("\t" * 2 + "support to {} of amount {} sent".format(habitat_trip, habitat_trips[habitat_trip]))
                else:
                    account.smart_enter()
                    counter -= 1
                    print(result[1])
                    print("\t" * 2 + "support to {} of amount {} was not send".format(habitat_trip, habitat_trips[habitat_trip]))
        else:
            unit_dictionary = "{1=" + str(- habitat_trips[habitat_trip]) + ";}"
            counter = 2
            while counter > 0:
                result = account.recall_units(habitat_trip, unit_dictionary, Data.tripwire_data["trips_source"])
                if result[0]:
                    counter = 0
                    print("\t" * 2 + "units from {} in amount {} recalled".format(habitat_trip, habitat_trips[habitat_trip]))
                else:
                    account.smart_enter()
                    counter -= 1
                    print(result[1])
                    print("\t" * 2 + "units from {} in amount {} was not recalled".format(habitat_trip, habitat_trips[habitat_trip]))


def get_new_reports(account):
    fetch_reports_result = account.fetch_reports()
    reports_to_public = []
    reports_to_delete = []
    for report in fetch_reports_result[1]["Data"]["Report"]:
        reportt = Report(report, "173")
        continue
        if Tool.is_report_defensive(report):
            if Tool.are_losses_enough(report):
                if not Tool.is_report_published(report):
                    reports_to_public.append(report)
            else:
                reports_to_delete.append(report)
    logger.log(1, "get_new_reports", "Reports to delete: {}, reports to public: {}".format(len(reports_to_delete,), len(reports_to_public)))
    return reports_to_public, reports_to_delete


def delete_reports(account, reports_to_delete_list):
    for report in reports_to_delete_list:
        account.delete_report(report["id"])


def public_reports(account, reports_to_public_list):
    reports_to_message_list = []
    for report in reports_to_public_list:
        result = account.delete_report(report["id"])
        if result[0]:
            reports_to_message_list.append(report)
    return reports_to_message_list


def message_reports(account, reports_to_message_list, discussion_id):
    # reports to message:
    print("\t" * 2 + "separating reports")
    tens_messages_list = list_to_list_of_list(reports_to_message_list)
    print("\t" * 2 + "reports separated")
    print("\t" * 2 + "messages amount: {}".format(len(tens_messages_list)))
    ten_index = 0
    for ten_messages in tens_messages_list:
        time.sleep(3)
        counter = 5
        while counter > 0:
            send_message_result = send_message(account, ten_messages, discussion_id, ten_index)
            result = send_message_result[0]
            if result:
                counter = 0
                print("\t" * 2 + "message sent")
            else:
                print("\t" * 2 + send_message_result[1])
                print("\t" * 2 + "message not sent, relogging")
                account.smart_enter()
                print("\t" * 2 + "relogged")
                result -= 1
        ten_index += 1


def send_message(account, reports_list, discussion_id, list_index):
    message = ""
    counter = 0
    for report in reports_list:
        index = list_index * Data.tripwire_data["reports_in_message"] + counter + 1
        counter += 1
        report_link = "l+k://report?" + str(report["id"]) + "&" + str(report["habitat"]) + "&193"
        try:
            habitat_name = Tool.surrogate_decoding(report["content"]["destinationHabitat"]["name"])
        except:
            habitat_name = "(/)название(/)"
        try:
            player_name = Tool.surrogate_decoding(report["content"]["destinationHabitat"]["nick"])
        except:
            player_name = "(/)имя(/)"

        message += "{}. {}\n{}\n{}\n{}\n\n".format(index, Tool.current_time_in_msc(report["date"]), player_name, habitat_name, report_link)
    telegram.send_message(message)
    print(message)
    result = account.send_message(message, discussion_id)
    print(result)
    return result


def list_to_list_of_list(llist, pointbreak=Data.tripwire_data["reports_in_message"]):
    list_of_lists = []
    sublist = []
    count = pointbreak
    while llist:
        sublist.append(llist.pop())
        count -= 1

        if count == 0:
            count = pointbreak
            list_of_lists.append(sublist)
            sublist = []
    if sublist:
        list_of_lists.append(sublist)
    return list_of_lists


main("m2222222@bk.ru", "22222")
