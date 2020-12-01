class Collection:
    @classmethod
    def of(cls, json):
        return Collection(json)

    def __init__(self, json):
        self._json = json
        return

    def get_id(self):
        return self._json.get("id")

    def get_name(self):
        return self._json.get("name")
