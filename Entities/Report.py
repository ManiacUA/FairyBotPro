import Tool
import Data


class Report:
    is_defensive = None
    losses_enough_to_alert = None
    world_id = None
    published = None
    id = None

    def __init__(self, report_dict, world_id):
        self.world_id = str(world_id)

        if "published" in report_dict:
            self.published = report_dict["published"] == "true"

        if "id" in report_dict:
            self.id = report_dict["id"]

        self._calc_is_defensive_(report_dict)
        self._calc_losses_enough_to_alert(report_dict)

    def _calc_is_defensive_(self, report_dict):
        correct_type = "type" in report_dict and report_dict["type"] == "8"
        not_offensive = "content" in report_dict and "ownOffenderUnitDictionary" not in report_dict["content"]
        self.is_defensive = correct_type and not_offensive

    def _calc_losses_enough_to_alert(self, report_dict):
        if "content" in report_dict and "unitDictionary" in report_dict["content"]:
            unit_dictionary = report_dict["content"]["unitDictionary"]
        else:
            unit_dictionary = {}
        left_sum = 0
        if "content" in report_dict and "lossDictionary" in report_dict["content"]:
            losses_dictionary = report_dict["content"]["lossDictionary"]
        else:
            losses_dictionary = {}
        losses_sum = 0

        for unit_kind in unit_dictionary:
            left_sum += int(unit_dictionary[unit_kind])
        for unit_kind in losses_dictionary:
            losses_sum += int(losses_dictionary[unit_kind])

        total_sum = losses_sum + left_sum
        if total_sum == 0:
            self.losses_enough_to_alert = False

        self.losses_enough_to_alert = losses_sum / total_sum > Data.tripwire_data["alert_coefficient"]

    def __str__(self):
        alive = 0
        dead = 0
        destruction_perc = 0
        player_name = ""
        habitat_name = ""
        habitat_type = ""
        habitat_type_to_emoji = {"cast": "🏡", "fort": "🏰", "city": "🌃"}
        link = ""
        strings = []
        strings[0] = "{} 😇{}/💀{}/{}%".format(habitat_type_to_emoji[habitat_type], alive, dead, destruction_perc)
        strings[1] = str(Tool.current_time_in_msc())
        strings[2] = "👤{}".format(player_name)
        strings[3] = "🏰{}".format(habitat_name)
        strings[4] = "{}".format(link)
        return "\n".join(strings)

