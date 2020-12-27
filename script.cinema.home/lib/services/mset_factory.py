import random

from lib.models.types.genres import Genre
from lib.models.types.media_sets import Recommended, Popular, Categorized, Newest, Best, Streamed
from lib.models.types.networks import Network

main_genres = [Genre.ACTION, Genre.ANIMATION, Genre.COMEDY, Genre.CRIME, Genre.DOCUMENTARY, Genre.DRAMA,
               Genre.ROMANCE, Genre.SCI_FI, Genre.THRILLER, Genre.HORROR, Genre.WAR]


def movie_sets():
    random.shuffle(main_genres)
    return [Popular.movies(),
            Categorized.movies_by_genre(main_genres[0]),
            Recommended.movies_by_staff(),
            Categorized.movies_by_genre(main_genres[1]),
            Newest.movies(),
            Categorized.movies_by_genre(main_genres[2]),
            Streamed.movies_of(Network.NETFLIX),
            Categorized.movies_by_genre(main_genres[3]),
            Best.movies(),
            Categorized.movies_by_genre(main_genres[4]),
            Categorized.movies_by_genre(main_genres[5]),
            Categorized.movies_by_genre(main_genres[6]),
            Categorized.movies_by_genre(main_genres[7]),
            Categorized.movies_by_genre(main_genres[8]),
            Categorized.movies_by_genre(main_genres[9]),
            Categorized.movies_by_genre(main_genres[10])]


def show_sets():
    random.shuffle(main_genres)
    return [Popular.shows(),
            Categorized.shows_by_genre(main_genres[0]),
            Recommended.shows_by_staff(),
            Categorized.shows_by_genre(main_genres[1]),
            Newest.shows(),
            Categorized.shows_by_genre(main_genres[2]),
            Streamed.shows_of(Network.NETFLIX),
            Categorized.shows_by_genre(main_genres[3]),
            Best.shows(),
            Categorized.shows_by_genre(main_genres[4]),
            Categorized.shows_by_genre(main_genres[5]),
            Categorized.shows_by_genre(main_genres[6]),
            Categorized.shows_by_genre(main_genres[7]),
            Categorized.shows_by_genre(main_genres[8]),
            Categorized.shows_by_genre(main_genres[9]),
            Categorized.shows_by_genre(main_genres[10])]
