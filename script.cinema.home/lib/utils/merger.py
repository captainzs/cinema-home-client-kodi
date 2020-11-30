from lib.utils.logger import Logger

__logger = Logger.get_instance(__name__)


def merge(json1, json2):
    merged = json2.copy()
    for key, value in json1.items():
        if key not in merged:
            merged[key] = value
        elif type(value) is list:
            for v in value:
                if v not in merged[key]:
                    merged[key].append(v)
        elif type(value) is dict:
            merged[key] = merge(value, merged[key])
        elif key not in ["rating", "releaseYear", "runtime"] and value != merged[key]:
            __logger.warning(
                "Seems to be an incorrect value on json merge {}: {} != {}".format(key, value, merged[key]))
    return merged
