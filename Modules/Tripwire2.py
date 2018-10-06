import Logger
import Class
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

    def run(self, account):
        self.logger.log(1, "run", "started.")
        reports = self._load_reports()
        self.logger.log(1, "load_reports", "{} reports loaded at all".format(len(reports)))
        reports = [report for report in reports if report.is_defensive]
        self.logger.log(1, "load_reports", "{} defensive reports".format(len(reports)))
        insufficient_losses_reports = [report for report in reports if not report.losses_enough_to_alert]
        self.logger.log(1, "load_reports", "{} deletion pending reports".format(len(insufficient_losses_reports)))
        sufficient_losses_reports = [report for report in reports if report.losses_enough_to_alert]
        self.logger.log(1, "load_reports", "{} publishing and sending pending reports".format(len(sufficient_losses_reports)))
        self._delete_reports( insufficient_losses_reports)
        self._public_reports(sufficient_losses_reports)
        reports_lists = self._split_reports(reports)
        self._message_reports(reports_lists)
        self.logger.log(1, "run", "finished.")

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
        self.logger = Logger.Logger("Tripwire2.Replacer")

    def run(self):
        pass

    def _get_alliance_ids(self):
        alliances_to_tripwire = []

        player_id = self.account.header_info['playerID']

        for player in self.account.login_result["Data"]["Player"]:
            if player["id"] == player_id:
                player_dict = player
            else:
                self.logger.warning(1, "get_alliance_ids", "Player is not in the info with players, consider loading by request")
                return []

        player = Player(player_dict)
        if not player.alliance:
            self.logger.warning(1, "get_alliance_ids", "Player has not alliance")
            return []

        for alliance in self.account.login_result["Data"]["Alliance"]:
            if alliance["id"] == this_player_alliance_id:
                this_player_alliance = Alliance(alliance, "202")

            this_player_alliance.extract_diplomacy(self.account.login_result["Data"]["Diplomacy"])
            for alliance_id in this_player_alliance.diplomacy:
                alliance__rel = this_player_alliance.diplomacy[alliance_id]
        return alliances_to_tripwire


def main():
    account = Class.Player(Data.tripwire_data["email"], Data.tripwire_data["password"], 1)
    account.smart_enter()
    reporter = Reporter(account)
    replacer = Replacer(account)

main()