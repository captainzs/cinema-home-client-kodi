from collections import namedtuple

NetworkDef = namedtuple('Network', 'id name file')


class Network:
    ABC = NetworkDef(0, 'ABC', 'abc.png')
    APPLE = NetworkDef(1, 'AppleTV', 'apple.png')
    AMAZON = NetworkDef(2, 'Amazon', 'amazon.png')
    BBC = NetworkDef(3, 'BBC', 'bbc.png')
    CBS = NetworkDef(4, 'CBS', 'cbs.png')
    CRITERION = NetworkDef(5, 'Criterion Channel', 'criterion.png')
    CW = NetworkDef(6, 'The CW', 'cw.png')
    DCU = NetworkDef(7, 'DC Universe', 'dcu.png')
    DISNEY = NetworkDef(8, 'Disney', 'disney.png')
    HBO = NetworkDef(9, 'HBO', 'hbo.png')
    HULU = NetworkDef(10, 'HULU', 'hulu.png')
    ITUNES = NetworkDef(11, 'iTunes', 'itunes.png')
    MTV = NetworkDef(12, 'MTV', 'mtv.png')
    MTVA = NetworkDef(13, 'MTVA', 'mtva.png')
    NBC = NetworkDef(14, 'NBC', 'nbc.png')
    NICKELODEON = NetworkDef(15, 'Nickelodeon', 'nickelodeon.png')
    NETFLIX = NetworkDef(16, 'Netflix', 'netflix.png')
    STARZ = NetworkDef(17, 'STARZ', 'starz.png')

    _NETWORK_2_ID = {
        0: ABC,
        1: APPLE,
        2: AMAZON,
        3: BBC,
        4: CBS,
        5: CRITERION,
        6: CW,
        7: DCU,
        8: DISNEY,
        9: HBO,
        10: HULU,
        11: ITUNES,
        12: MTV,
        13: MTVA,
        14: NBC,
        15: NICKELODEON,
        16: NETFLIX,
        17: STARZ
    }

    @classmethod
    def of(cls, network_id):
        network = Network._NETWORK_2_ID.get(network_id, None)
        if network is None:
            raise RuntimeError("Network is not configured for id: {}".format(network_id))
        elif network.id != network_id:
            raise RuntimeError("Network with id: {} is incorrectly configured!".format(network_id))
        return network
