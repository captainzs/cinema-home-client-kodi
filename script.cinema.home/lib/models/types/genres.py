from collections import namedtuple

GenreDef = namedtuple('Genre', 'id name file')


class Genre:
    def __init__(self):
        pass

    ACTION = GenreDef(0, 'Action', 'abc.png')
    ADVENTURE = GenreDef(1, 'Adventure', 'apple.png')
    ANIMATION = GenreDef(2, 'Animation', 'amazon.png')
    BIOGRAPHY = GenreDef(3, 'Biography', 'bbc.png')
    COMEDY = GenreDef(4, 'Comedy', 'cbs.png')
    CRIME = GenreDef(5, 'Crime', 'criterion.png')
    DOCUMENTARY = GenreDef(6, 'Documentary', 'cw.png')
    DRAMA = GenreDef(7, 'Drama', 'dcu.png')
    EDUCATIONAL = GenreDef(8, 'Educational', 'disney.png')
    FAMILY = GenreDef(9, 'Family', 'hbo.png')
    FANTASY = GenreDef(10, 'Fantasy', 'hulu.png')
    HISTORY = GenreDef(11, 'History', 'itunes.png')
    HORROR = GenreDef(12, 'Horror', 'mtv.png')
    MUSIC = GenreDef(13, 'Music', 'mtva.png')
    MYSTERY = GenreDef(14, 'Mystery', 'nbc.png')
    REALITY = GenreDef(15, 'Reality', 'nickelodeon.png')
    ROMANCE = GenreDef(16, 'Romance', 'netflix.png')
    SCI_FI = GenreDef(17, 'Science Fiction', 'starz.png')
    SHORT = GenreDef(18, 'Short', 'starz.png')
    SPORT = GenreDef(19, 'Sport', 'starz.png')
    TALK_SHOW = GenreDef(20, 'Talk-Show', 'starz.png')
    THRILLER = GenreDef(21, 'Thriller', 'starz.png')
    WAR = GenreDef(22, 'War', 'starz.png')
    WESTERN = GenreDef(23, 'Western', 'starz.png')

    _GENRE_2_ID = {
        0: ACTION,
        1: ADVENTURE,
        2: ANIMATION,
        3: BIOGRAPHY,
        4: COMEDY,
        5: CRIME,
        6: DOCUMENTARY,
        7: DRAMA,
        8: EDUCATIONAL,
        9: FAMILY,
        10: FANTASY,
        11: HISTORY,
        12: HORROR,
        13: MUSIC,
        14: MYSTERY,
        15: REALITY,
        16: ROMANCE,
        17: SCI_FI,
        18: SHORT,
        19: SPORT,
        20: TALK_SHOW,
        21: THRILLER,
        22: WAR,
        23: WESTERN
    }

    @classmethod
    def of(cls, genre_id):
        genre = Genre._GENRE_2_ID.get(genre_id, None)
        if genre is None:
            raise RuntimeError("Genre is not configured for id: {}".format(genre_id))
        elif genre.id != genre_id:
            raise RuntimeError("Genre with id: {} is incorrectly configured!".format(genre_id))
        return genre
