class Alliance:
    name = None
    world_id = None
    id = None
    link = None
    diplomacy = None

    def __init__(self, alliance_dict, world_id, diplomacy_dict=None):
        self.world_id = str(world_id)

        if "id" in alliance_dict:
            self.id = alliance_dict["id"]

        if "name" in alliance_dict:
            self.name = alliance_dict["name"]

        self._calc_link()

        if diplomacy_dict is not None:
            self.extract_diplomacy(diplomacy_dict)

    def _calc_link(self):
        self.link = "l+k://alliance?{}&{}".format(self.id, self.world_id)

    def __str__(self):
        return "{} {}".format(self.name, self.link)

    def extract_diplomacy(self, diplomacy_dict):
        relationship_num_to_word = {"-1": "red", "1": "blue", "2": "green", "3": "orange"}
        self.diplomacy = {}
        for diplomacy_rel in diplomacy_dict:
            self_alliance, target_alliance = diplomacy_rel['id'].split('-')
            self.diplomacy[target_alliance] = relationship_num_to_word[diplomacy_rel["relationship"]]

    def get_diplomacy_by_color(self, color):
        ids = []
        for alliance_id in self.diplomacy:
            alliance_rel = self.diplomacy[alliance_id]
            if alliance_rel == color:
                ids.append(alliance_id)
        return ids