class Player:
    name = None
    world_id = None
    id = None
    link = None
    alliance = None

    def __init__(self, player_dict, world_id, ):
        self.world_id = str(world_id)

        if "id" in player_dict:
            self.id = player_dict["id"]

        if "name" in player_dict:
            self.id = player_dict["name"]

        if "alliance" in player_dict:
            self.alliance = player_dict["alliance"]

        self._calc_link()

    def _calc_link(self):
        self.link = "l+k://player?{}&{}".format(self.id, self.world_id)

    def __str__(self):
        return "{} {}".format(self.name, self.link)
