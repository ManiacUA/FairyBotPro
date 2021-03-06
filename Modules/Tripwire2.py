import Logger
import WorldAccount
import Data
import Tool
import Telegram
from Entities.Report import Report
from Entities.Alliance import Alliance
from Entities.Player import Player


class TripwireError(Exception):
    pass


class Reporter:
    def __init__(self, account):
        self.logger = Logger.Logger("Tripwire2.Reporter", account)
        self.account = account
        self.telegram = Telegram.Telegram()
        self.logger.log_finished(account, "init")

    def run(self, account):
        self.logger.log_started(account, 'run')
        reports = self._load_reports()
        reports = [report for report in reports if report.is_defensive]
        insufficient_losses_reports = [report for report in reports if not report.losses_enough_to_alert]
        sufficient_losses_reports = [report for report in reports if report.losses_enough_to_alert]
        self._delete_reports( insufficient_losses_reports)
        self._public_reports(sufficient_losses_reports)
        reports_lists = self._split_reports(reports)
        self._message_reports(reports_lists)
        self.logger.log_finished(account, 'run')

    def _load_reports(self):
        success, response_dict = self.account.fetch_reports()
        if not success:
            raise TripwireError
        server_id = Tool.server_id_from_response_dict(response_dict)
        reports = []
        for report_dict in response_dict:
            reports.append(Report(report_dict, server_id))
        return reports

    def _delete_reports(self, reports_list):
        self.logger.log(2, "delete_reports", "started")
        for report in reports_list:
            success, _ = self.account.delete_report(report)
            if not success:
                self.logger.log(2, "delete_reports", "{} report wasn't deleted".format(report.id))
        self.logger.log(2, "delete_reports", "finished")

    def _public_reports(self, reports_list):
        self.logger.log(2, "public_reports", "started")
        for report in reports_list:
            success, _ = self.account.public_report(report)
            if not success:
                self.logger.log(2, "public_reports", "{} report wasn't published".format(report.id))
        self.logger.log(2, "public_reports", "finished")

    def _message_reports(self, reports_lists):
        self.logger.log(2, "message_reports", "started")
        list_index = 0
        for reports_list in reports_lists:
            self._message_reports_list(reports_list, list_index)
            list_index += 1
        self.logger.log(2, "message_reports", "finished")

    def _message_reports_list(self, reports_list, list_index):
        message = ""
        report_index = 1
        for report in reports_list:
            message += "{})\n{}\n".format(report_index+list_index*Data.tripwire_data["reports_in_message"], str(report))
            report_index += 1
        self.telegram.send_message(message)
        success, _ = self.account.send_message(message, discussion_id=Data.tripwire_data["discussion_id"])
        if not success:
            self.logger.log(3, "message_reports_list", "reports list(size {}) wasn't sent".format(len(reports_list)))

    def _split_reports(self, reports):
        pointbreak = Data.tripwire_data["reports_in_message"]
        reports_lists = []
        pointbreak -= 1
        while len(reports) >= pointbreak:
            reports_lists.append(reports[0:pointbreak])
            reports = reports[pointbreak:]
        if reports:
            reports_lists += [reports]
        self.logger.log(2, "split_reports", "reports splitted in {} lists".format(len(reports_lists)))
        return reports_lists


class Replacer:
    def __init__(self, account):
        self.account = account
        self.logger = Logger.Logger("Tripwire2.Replacer", account)

    def run(self):
        alliances_to_tripwire = self._get_alliance_ids()
        force_include_players = Data.tripwire_data["player_ids_include_list"]
        force_exclude_players = Data.tripwire_data["player_ids_exclude_list"]
        players_to_tripwire = self.alliance_id_to_player_ids(alliances_to_tripwire)

    def _get_alliance_ids(self):
        player_id = self.account.header_info['playerID']

        for player in self.account.login_result["Data"]["Player"]:
            if player["id"] == player_id:
                player_dict = player
                break
            else:
                self.logger.warning(self.account, "get_alliance_ids", "Player is not in the info with players, consider loading by request")
                return []

        player = Player(player_dict, "202")
        if not player.alliance:
            self.logger.warning(self.account, "get_alliance_ids", "Player has not alliance")
            return []

        for alliance in self.account.login_result["Data"]["Alliance"]:
            if alliance["id"] == player.alliance:
                this_player_alliance = Alliance(alliance, "202")
                break

        this_player_alliance.extract_diplomacy(self.account.login_result["Data"]["Diplomacy"])
        return this_player_alliance.get_diplomacy_by_color("orange") + [this_player_alliance.id]

    def alliance_id_to_player_ids(self, alliance_ids):
        player_ids = []
        for alliance_id in alliance_ids:
            result = self.account.alliance_info(alliance_id)
            pass


def main():
    account = WorldAccount.WorldAccount(Data.tripwire_data["email"], Data.tripwire_data["password"], 1)
    account.smart_enter()
    # reporter = Reporter(account)
    replacer = Replacer(account)
    replacer.run()

main()