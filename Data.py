# server_url = "https://backend3.lordsandknights.com/XYRALITY/WebObjects/LKWorldServer-BattleWorld-World-5.woa/wa/"
server_url = "https://backend2.lordsandknights.com/XYRALITY/WebObjects/LKWorldServer-RU-17.woa/wa/"
check_valid_login_browser_url = "https://login.lordsandknights.com/XYRALITY/WebObjects/BKLoginServer.woa/wa/LoginAction/checkValidLoginBrowser"
worlds_url = "https://login.lordsandknights.com/XYRALITY/WebObjects/BKLoginServer.woa/wa/worlds"

request_timeout = 5
relogin_timeout = 10
alliance_ids_to_tripwire = [611, 824, 835, 1867, 2649]  # replace with orange diplo of Tale
telegram_token = "560145098:AAGoLcHjsnj59TOGcPoZ2WkcVh_M4WtKmsU"

tripwire_data = {
    "telegram_chat_id": "-305164648",
    "telegram_debug_chat_id": "-201794441",
    "reports_in_message": 8,
    "minutes_between_check": 7,
    "tripwire_size": 5,
    "trips_source": 21597,  # choose it by habitat link
    "discussion_id": 23502,
    "email": "m2222222@bk.ru",
    "password": "22222",
    "alert_coefficient": 0.21  # 1/5 will not trigger while 1/4- and 2+/5 will
}