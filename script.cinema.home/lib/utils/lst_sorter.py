from lib.utils.logger import Logger

__logger = Logger.get_instance(__name__)


def sort_arts(art_lst, iso639_order):
    if art_lst is None:
        return None

    def priority(img):
        iso639 = img.get_iso639()
        if iso639 in iso639_order:
            return iso639_order.index(iso639)
        return len(iso639_order)

    return sorted(art_lst, key=priority)


def sort_videos(video_lst, iso639_order):
    if video_lst is None:
        return None

    def priority(video):
        return 0 if video.get_type() == "Teaser" else 1

    teasers_in_front = sorted(video_lst, key=priority)
    return sort_arts(teasers_in_front, iso639_order)


def sort_locale_texts(locale_text_lst, iso639_order):
    if locale_text_lst is None:
        return None

    def priority(text):
        iso639 = text.get("iso639Id", None)
        if iso639 in iso639_order:
            return iso639_order.index(iso639)
        return len(iso639_order)

    return sorted(locale_text_lst, key=priority)


def sort_seasons(season_lst):
    if season_lst is None:
        return None
    return sorted(season_lst, key=lambda s: s.get_season_no())


def sort_episodes(episode_lst):
    if episode_lst is None:
        return None
    return sorted(episode_lst, key=lambda e: e.get_episode_number())


def sort_torrents(torrent_lst):
    if torrent_lst is None:
        return None
    return sorted(torrent_lst, key=lambda t: t.get_peers(), reverse=True)
