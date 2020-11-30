class DynamicData:
    def __init__(self, json):
        self._json = json
        return

    def is_favored(self):
        return self._json["isFavored"]
