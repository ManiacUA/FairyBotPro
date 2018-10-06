import Data
import hashlib
import Tool
import urllib
import time
import Logger


class Player:
    available = True
    login_result = None

    def smart_create_message(self):
        self.logger.warning(1, "smart_create_message", "this function is not finished.")
        # TODO: if message doesnt fit - split it and send 1 by 1

    def smart_send_message(self):
        self.logger.warning(1, "smart_send_message", "this function is not finished.")
        # TODO: if message doesnt fit - split it and send 1 by 1

    def __init__(self, email, password, additional_indent=0, world_id="no_data", header_info=None):
        if header_info is None:
            self.header_info = {}
        self.email = email
        self.password = password
        self.world_id = world_id
        self.logger = Logger.Logger("Class/Player", additional_indent)
        # TODO: get server url by requesting it from server

    def repeated_request(self, url, params, parse_response=True, return_cookies=False, relogin_on_failure=True, times=1):
        ini_times = times
        done = False
        result = [False, "Request was not attempted.(times <= 0 ?)"]
        while (not done) and times > 0:
            result = Tool.make_request(url, params, self.header_info, parse_response=parse_response,
                                       return_cookies=return_cookies)
            done = result[0]
            times -= 1
            if (not done) and relogin_on_failure:
                self.enter()
                # TODO: in the future think about that: if dur to 802 I can not reenter account - I should wait before retry
                # TODO: add waiting time(custom for login!!!)
        if not done:
            self.logger.warning(1, "repeated_request", "{}: After {} attempt(s) request {} didnt succeed with error {}.".format(self.email, ini_times-times, url, result[1]))
        if done:
            self.logger.log(1, "repeated_request", "{}: After {} attempt(s) request {} succeeded.".format(self.email, ini_times-times, url))
        return result

    def enter(self):
        # This function can not use common repeat since it has a certain constrains on how often it may be used(due to login big return value) so it has to be done somewhere outside
        token_result = self.token()
        if not token_result[0]:
            self.header_info = None
            self.login_result = None
            return token_result
        login_result = self.login()
        if not login_result[0]:
            self.header_info = None
            self.login_result = None
        self.login_result = login_result[1]
        return login_result

    def smart_enter(self):
        done = False
        while not done:
            result = self.enter()
            done = result[0]
            if not done:
                self.logger.log(1, "smart_enter", "Counldt enter account: {}".format(result[1]))
                time.sleep(Data.relogin_timeout)
            if done:
                self.logger.log(1, "smart_enter", "Account entered.")
        return result

    def token(self):
        url = Data.server_url + "LoginAction/token"
        params = {
            "login": self.email,
            "password": hashlib.sha256(self.password.encode("utf-8")).hexdigest(),
            "deviceType": "Email",
        }
        result = self.repeated_request(url, params, False, True, False)
        if result[0]:
            self.header_info = result[1]
        return result

    def login(self):
        url = Data.server_url + "LoginAction/login"
        params = {}
        return self.repeated_request(url, params, relogin_on_failure=False)

    def request_help(self):
        url = Data.server_url + "AllianceAction/helpAllMembersForFree"
        params = {}
        return self.repeated_request(url, params, times=3)

    def habitat_info(self, habitat_id):
        url = Data.server_url + "HabitatAction/habitatInformation"
        params = {
            "id": habitat_id
        }
        return self.repeated_request(url, params, times=3)

    def alliance_info(self, alliance_id):
        url = Data.server_url + "AllianceAction/allianceInformation"
        params = {
            "id": alliance_id
        }
        return self.repeated_request(url, params, times=3)

    def player_info(self, player_id):
        url = Data.server_url + "ProfileAction/playerInformation"
        params = {
            "id": player_id
        }
        return self.repeated_request(url, params, times=3)

    def send_message(self, content, discussion_id):
        url = Data.server_url + "DiscussionAction/addDiscussionEntry"
        params = {
            "discussionId": str(discussion_id),
            "content": urllib.parse.quote_plus(str(content))
        }
        return self.repeated_request(url, params, times=3)

    def public_report(self, report_id):
        url = Data.server_url + "ReportAction/setReportPublished"
        params = {
            "id": str(report_id),
            "published": "true"
        }
        return self.repeated_request(url, params, times=3)

    def fetch_reports(self):
        url = Data.server_url + "ReportAction/habitatReportArray"
        params = {}
        return self.repeated_request(url, params, times=3)

    def send_support(self, destination_id, unit_dictionary, source_id):
        url = Data.server_url + "TransitAction/startTransit"
        # TODO: are all of params really necessary !??!?
        params = {
            "transitType": str(0),
            "unitDictionary": str(unit_dictionary),
            "sourceHabitatID": str(source_id),
            "resourceDictionary": "{}",
            "worldId": str(193),
            "logoutUrl": "http://lordsandknights.com/",
            "destinationHabitatID": str(destination_id)

        }
        return self.repeated_request(url, params, times=3)

    def send_resources(self, destination_id, unit_dictionary, resource_dictionary, source_id):
        url = Data.server_url + "TransitAction/startTransit"
        params = {
            "transitType": str(4),
            "resourceDictionary": str(resource_dictionary),
            "unitDictionary": str(unit_dictionary),
            "sourceHabitatID": str(source_id),
            "destinationHabitatID": str(destination_id)
        }
        return self.repeated_request(url, params, times=3)

    def delete_report(self, report):
        url = Data.server_url + "ReportAction/deleteHabitatReport"
        params = {
            "id": str(report.id)
        }
        return self.repeated_request(url, params, times=3)

    def recall_support(self, source_id, unit_dictionary, destination_id):
        url = Data.server_url + "TransitAction/startTransit"
        params = {
            "destinationHabitatID": str(destination_id),
            "sourceHabitatID": str(source_id),
            "unitDictionary": str(unit_dictionary),
            "transitType": str(1)
        }
        return self.repeated_request(url, params, times=3)

    def load_alliance_rating(self, offset=0, limit=50):
        url = Data.server_url + "QueryAction/allianceRanks"
        params = {
            "offset": str(offset),
            "limit": str(limit)
        }
        return self.repeated_request(url, params, times=3)

    def create_message(self, subject, player_id, content):
        url = Data.server_url + "DiscussionAction/createDiscussion"
        params = {
            "content": urllib.parse.quote_plus(str(content)),
            "subject": urllib.parse.quote_plus(str(subject)),
            "receivingPlayerArray": str(player_id)  # TODO: make it work with few players at a time
        }
        return self.repeated_request(url, params, times=3)

    def check_valid_login_browser(self):
        url = Data.check_valid_login_browser_url
        params = {
            "login": self.email,
            "password": hashlib.sha256(self.password.encode("utf-8")).hexdigest(),
            "deviceType": "Email",
        }
        return self.repeated_request(url, params, times=2)

    def load_worlds(self):
        url = Data.worlds_url
        params = {
            "login": self.email,
            "password": hashlib.sha256(self.password.encode("utf-8")).hexdigest(),
            "deviceType": "Email",
        }
        return self.repeated_request(url, params, times=2)

    def send_attack(self, destination_id, unit_dictionary, source_id):
        url = Data.server_url + "TransitAction/startTransit"
        params = {
            "unitDictionary": str(unit_dictionary),
            "sourceHabitatID": str(source_id),
            "destinationHabitatID": str(destination_id)
        }
        return self.repeated_request(url, params, times=3)

    def set_diplo(self, alliance_id, alliance_rel):
        url = Data.server_url + "AllianceAction/setDiplomaticRelation"
        params = {
            "id": str(alliance_id),
            "diplomaticValue": str(alliance_rel)
        }
        return self.repeated_request(url, params, times=3)

    def send_spy(self, destination_id, source_id, amount=1):
        url = Data.server_url + "SpyAction/startSpyingTransit"
        params = {
            "copperAmount": str(amount),
            "sourceHabitatID": str(source_id),
            "destinationHabitatID": str(destination_id)
        }
        return self.repeated_request(url, params, times=3)
