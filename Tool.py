import re
import requests
import datetime
import Data


def validate(text):
    try:
        parser_result = parse(text)
    except SyntaxError:
        raise ValueError("Incorrect syntax: " + text)
    if "error" in parser_result:
        raise ValueError("Response contains error saying: " + parser_result["error"])


def parse(text):
    temp_namespace = {}
    temp_dictionary_name = "temp_name"
    text = text.replace("=", ":")
    text = text.replace("(", "[")
    text = text.replace(")", "]")
    text = text.replace(";", ",")
    text = re.sub(r'\\U', "\\u", text)
    text = surrogate_decoding(text)
    exec(temp_dictionary_name + "=" + text, temp_namespace)
    return temp_namespace[temp_dictionary_name]


def server_id_from_response_dict(response_dict):
    if "serverVersion" not in response_dict:
        raise ValueError("there is no serverVersion in response dictionary, can not figure out server id")
    string = response_dict["serverVersion"]
    string_data = {}
    string_data["game"], string_data["server"], string_data["ids"] = string.split("_")
    (string_data["ids"]["server_id"],
     string_data["ids"]["who_knows_what1"],
     string_data["ids"]["who_knows_what1"]
     ) = string_data["ids"].split("-")
    return string_data["ids"]["server_id"]



def current_time_in_msc(time_string):
    report_datetime = datetime.datetime.strptime(time_string, "%Y-%m-%d %H:%M:%S Etc/GMT")
    report_datetime += datetime.timedelta(hours=3)
    new_time_string = "{:02d}/{:02d}/{:04d} {:02d}:{:02d}:{:02d}".format(report_datetime.day, report_datetime.month, report_datetime.year, report_datetime.hour, report_datetime.minute, report_datetime.second)
    return new_time_string


def surrogate_decoding(text):
    return str(text).encode('utf-16', 'surrogatepass').decode('utf-16')


def create_header(cookie_data_dictionary=None):
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


def make_request(url, params, cookie_dict, parse_response=True, return_cookies=False):
    try:
        to_check, to_use = send_request(url, params, cookie_dict, return_cookies)
        validate(to_check)
        if parse_response:
            return [True, parse(to_use)]
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


def send_request(url, params, cookie_dict, return_cookies):
    headers = create_header(cookie_dict)
    response = requests.get(url, params=params, headers=headers, timeout=Data.request_timeout)
    if return_cookies:
        cookie_data_list = response.cookies.items()
        cookie_data_dict = {}
        for element in cookie_data_list:
            cookie_data_dict[element[0]] = element[1]
        return [response.text, cookie_data_dict]
    else:
        return [response.text, response.text]


def Sprint(text):
    text = surrogate_decoding(text)
    print(text)
