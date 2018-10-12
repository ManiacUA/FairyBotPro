from Entities.Player import Player
from Entities.Alliance import Alliance
from Entities.Habitat import Habitat


class Data:
    world_id = None
    def __init__(self, gen_dict):
        self.gen_dict = gen_dict
        self.parse_useful()
        self.data = {"player": {},
                     "alliance": {},
                     "habitat": {}}

    def parse_players(self):
        try:
            dict_list = self.gen_dict["Data"]["Player"]
            for dict_item in dict_list:
                new_object = Player(dict_item, world_id=self.world_id)
                self.data["player"][new_object.id] = new_object
        except KeyError:
            pass

    def parse_alliances(self):
        try:
            dict_list = self.gen_dict["Data"]["Alliance"]
            for dict_item in dict_list:
                new_object = Alliance(dict_item, world_id=self.world_id)
                self.data["alliance"][new_object.id] = new_object
        except KeyError:
            pass

    def parse_habitats(self):
        try:
            dict_list = self.gen_dict["Data"]["Habitat"]
            for dict_item in dict_list:
                new_object = Habitat(dict_item, world_id=self.world_id)
                self.data["habitat"][new_object.id] = new_object
        except KeyError:
            pass

    def parse_diplomacy(self):
        pass

    def find_own(self):
        pass

    def parse_useful(self):
        self.calc_server_id()

    def calc_server_id(self):
        if "serverVersion" not in self.gen_dict:
            raise ValueError("there is no serverVersion in response dictionary, can not figure out server id")
        string = self.gen_dict["serverVersion"]
        string_data = {}
        string_data["game"], string_data["server"], string_data["ids"] = string.split("_")
        (string_data["ids"]["server_id"],
         string_data["ids"]["who_knows_what1"],
         string_data["ids"]["who_knows_what2"]
         ) = string_data["ids"].split("-")
        self.world_id = string_data["ids"]["server_id"]

    def get(self, instance, ids=None):
        # if ids is None all will be returned otherwise a list of instances for those ids will be
        # if value is not found it will be queried
        pass

# testing env

import WorldAccount


account = WorldAccount.WorldAccount("talt01@gmail.com", "3259")
account.smart_enter()
