import Data
import hashlib
import Tool
import urllib
import time
import Logger
import requests
import re


class WorldAccount:

    def __init__(self, email, password):
        self.email = email
        # Exceptional situation. If I place logger first here it will attempt to get email which is not assigned yet.
        self.logger = Logger.Logger("Class/Player", self)
        self.password = password

        self.header_info = {}
        self.gen_dict = {}
        self.logger.log_func_finish()

    def make_request(self, url, params, cookie_dict, parse_response=True, return_cookies=False):
        try:
            to_check, to_use = self.send_request(url, params, cookie_dict, return_cookies)
            self.validate(to_check)
            if parse_response:
                return [True, self.parse(to_use)]
            else:
                return [True, to_use]
        except requests.exceptions.ReadTimeout:
            return [False, "Read timeout"]
        except requests.exceptions.ConnectTimeout:
            return [False, "Connect timeout"]
        except ValueError as error:
            return [False, str(error)]
        except:
            return [False, "Unknown error"]

    def send_request(self, url, params, cookie_dict, return_cookies):
        headers = self.create_header(cookie_dict)
        response = requests.get(url, params=params, headers=headers, timeout=Data.request_timeout)
        if return_cookies:
            cookie_data_list = response.cookies.items()
            cookie_data_dict = {}
            for element in cookie_data_list:
                cookie_data_dict[element[0]] = element[1]
            return [response.text, cookie_data_dict]
        else:
            return [response.text, response.text]

    def create_header(self, cookie_data_dictionary=None):
        cookie_data_string = ""
        if cookie_data_dictionary is None:
            cookie_data_dictionary = {}
        cookie_data_dictionary.update({"G_ENABLED_IDPS": "google"})
        for element in cookie_data_dictionary:
            cookie_data_string += element + "=" + cookie_data_dictionary[element] + ";"
        login_headers = \
            {
                "XYClient-Capabilities": "base,fortress,city,partialTransits,starterpack,requestInformation,partialUpdate",
                "Cookie": cookie_data_string,
                "XYClient-Platform": "browser"
            }
        return login_headers

    def validate(self, text):
        try:
            parser_result = self.parse(text)
        except SyntaxError:
            raise ValueError("Incorrect syntax: " + text)
        if "error" in parser_result:
            raise ValueError("Response contains error saying: " + parser_result["error"])

    def parse(self, text):
        temp_namespace = {}
        temp_dictionary_name = "temp_name"
        text = text.replace("=", ":")
        text = text.replace("(", "[")
        text = text.replace(")", "]")
        text = text.replace(";", ",")
        text = re.sub(r'\\U', "\\u", text)
        text = Tool.surrogate_decoding(text)
        exec(temp_dictionary_name + "=" + text, temp_namespace)
        return temp_namespace[temp_dictionary_name]

    def repeated_request(self, url, params, short_url=True, parse_response=True, return_cookies=False, times=3):
        self.logger.log_func_start("repeated_request")
        if short_url:
            url += Data.server_url + url
        ini_times = times
        done = False
        result = [False, "Request was not attempted.(times <= 0 ?)"]

        while (not done) and times > 0:
            result = self.make_request(url, params, self.header_info,
                                       parse_response=parse_response,
                                       return_cookies=return_cookies)
            done = result[0]
            times -= 1
            if not done:  # if session expired only then re login
                self.smart_enter()

        if not done:
            self.logger.warning("After {} attempt(s) request {} did not succeed with error {}.".format(
                ini_times-times, url, result[1]))
        self.logger.log("After {} attempt(s) request {} succeeded.".format( ini_times-times, url))

        self.logger.log_func_finish()
        return result

    def enter(self):
        self.logger.log_func_start("enter")

        def reset():
            self.gen_dict = None
            self.header_info = None

        token_result = self.token()
        if not token_result[0]:
            reset()
            return token_result
        self.header_info = token_result[1]

        login_result = self.login()
        if not login_result[0]:
            reset()
        else:
            self.gen_dict = login_result[1]
        self.logger.log_func_finish()
        return login_result

    def smart_enter(self):
        self.logger.log_func_start("smart_enter")
        done = False
        while not done:
            result = self.enter()
            done = result[0]
            if not done:
                self.logger.log("Could not enter account: {}".format(result[1]))
                time.sleep(Data.relogin_timeout)
            if done:
                self.logger.log("Account entered")
        self.logger.log_func_finish()
        return result

    def token(self):
        url = "LoginAction/token"
        params = {
            "login": self.email,
            "password": hashlib.sha256(self.password.encode("utf-8")).hexdigest(),
            "deviceType": "Email",
        }
        return self.repeated_request(url, params,
                                     parse_response=False,
                                     return_cookies=True,
                                     times=1)

    def login(self):
        url = "LoginAction/login"
        params = {}
        return self.repeated_request(url, params, times=1)

    def request_help(self):
        url = "AllianceAction/helpAllMembersForFree"
        params = {}
        return self.repeated_request(url, params, times=3)

    def habitat_info(self, habitat_id):
        url = "HabitatAction/habitatInformation"
        params = {
            "id": habitat_id
        }
        return self.repeated_request(url, params, times=3)

    def alliance_info(self, alliance_id):
        url = "AllianceAction/allianceInformation"
        params = {
            "id": alliance_id
        }
        return self.repeated_request(url, params, times=3)

    def player_info(self, player_id):
        url = "ProfileAction/playerInformation"
        params = {
            "id": player_id
        }
        return self.repeated_request(url, params, times=3)

    def send_message(self, content, discussion_id):
        url = "DiscussionAction/addDiscussionEntry"
        params = {
            "discussionId": str(discussion_id),
            "content": urllib.parse.quote_plus(str(content))
        }
        return self.repeated_request(url, params, times=3)

    def public_report(self, report_id):
        url = "ReportAction/setReportPublished"
        params = {
            "id": str(report_id),
            "published": "true"
        }
        return self.repeated_request(url, params, times=3)

    def fetch_reports(self):
        url = "ReportAction/habitatReportArray"
        params = {}
        return self.repeated_request(url, params)

    def send_support(self, destination_id, unit_dictionary, source_id):
        url = "TransitAction/startTransit"
        params = {
            "transitType": str(0),
            "unitDictionary": str(unit_dictionary),
            "sourceHabitatID": str(source_id),
            "resourceDictionary": "{}",
            "destinationHabitatID": str(destination_id)

        }
        return self.repeated_request(url, params)

    def send_resources(self, destination_id, unit_dictionary, resource_dictionary, source_id):
        url = "TransitAction/startTransit"
        params = {
            "transitType": str(4),
            "resourceDictionary": str(resource_dictionary),
            "unitDictionary": str(unit_dictionary),
            "sourceHabitatID": str(source_id),
            "destinationHabitatID": str(destination_id)
        }
        return self.repeated_request(url, params)

    def delete_report(self, report):
        url = "ReportAction/deleteHabitatReport"
        params = {
            "id": str(report.id)
        }
        return self.repeated_request(url, params)

    def recall_support(self, source_id, unit_dictionary, destination_id):
        url = "TransitAction/startTransit"
        params = {
            "destinationHabitatID": str(destination_id),
            "sourceHabitatID": str(source_id),
            "unitDictionary": str(unit_dictionary),
            "transitType": str(1)
        }
        return self.repeated_request(url, params)

    def load_alliance_rating(self):
        url = "QueryAction/allianceRanks"
        params = {
            "offset": str(0),
            "limit": str(50)
        }
        return self.repeated_request(url, params)

    def create_message(self, subject, player_id, content):
        url = "DiscussionAction/createDiscussion"
        params = {
            "content": urllib.parse.quote_plus(str(content)),
            "subject": urllib.parse.quote_plus(str(subject)),
            "receivingPlayerArray": str(player_id)
        }
        return self.repeated_request(url, params)

    def check_valid_login_browser(self):
        url = Data.check_valid_login_browser_url
        params = {
            "login": self.email,
            "password": hashlib.sha256(self.password.encode("utf-8")).hexdigest(),
            "deviceType": "Email",
        }
        return self.repeated_request(url, params, short_url=False)

    def load_worlds(self):
        url = Data.worlds_url
        params = {
            "login": self.email,
            "password": hashlib.sha256(self.password.encode("utf-8")).hexdigest(),
            "deviceType": "Email",
        }
        return self.repeated_request(url, params, short_url=False)

    def send_attack(self, destination_id, unit_dictionary, source_id):
        url = "TransitAction/startTransit"
        params = {
            "unitDictionary": str(unit_dictionary),
            "sourceHabitatID": str(source_id),
            "destinationHabitatID": str(destination_id)
        }
        return self.repeated_request(url, params)

    def set_diplo(self, alliance_id, alliance_rel):
        url = "AllianceAction/setDiplomaticRelation"
        params = {
            "id": str(alliance_id),
            "diplomaticValue": str(alliance_rel)
        }
        return self.repeated_request(url, params)

    def send_spy(self, destination_id, source_id, amount=1):
        url = "SpyAction/startSpyingTransit"
        params = {
            "copperAmount": str(amount),
            "sourceHabitatID": str(source_id),
            "destinationHabitatID": str(destination_id)
        }
        return self.repeated_request(url, params)
