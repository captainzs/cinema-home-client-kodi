import xbmcgui
from lib.utils import interpreter
from lib.utils.logger import Logger


class TorrentListItem(xbmcgui.ListItem):
    _logger = Logger.get_instance(__name__)

    @classmethod
    def of(cls, torrent):
        item = TorrentListItem()
        item.init(torrent)
        return item

    def __init__(self):
        xbmcgui.ListItem.__init__(self)
        return

    def init(self, torrent):
        self.setLabel(torrent.get_title())
        self.setProperty("FlagFile", interpreter.flag_2_img(torrent.get_unique_language()))
        self.setProperty("Languages",
                         ", ".join([interpreter.language_2_readable(lang) for lang in torrent.get_languages()]))
        full_size = torrent.get_size()
        self.setProperty("Size", interpreter.bytes_2_readable(full_size))
        resolution = torrent.get_res()
        if resolution:
            self.setProperty("Resolution", interpreter.resolution_2_readable(resolution))
        else:
            self.setProperty("Resolution", torrent.get_res_def())
        sources = torrent.get_sources()
        if sources:
            self.setProperty("Sources", ", ".join([interpreter.source_2_readable(s) for s in sources]))
        codecs_strings = []
        video_codec = torrent.get_video_codec()
        if video_codec:
            codecs_strings.append(interpreter.video_codec_2_readable(video_codec))
        audio_codecs = torrent.get_audio_codecs()
        if audio_codecs:
            codecs_strings.extend([interpreter.audio_codec_2_readable(c) for c in audio_codecs])
        color_codec = torrent.get_color_codec()
        if color_codec:
            codecs_strings.append(interpreter.color_codec_2_readable(color_codec))
        is_hdr = torrent.is_hdr()
        if is_hdr is True:
            codecs_strings.append("HDR")
        if len(codecs_strings) > 0:
            self.setProperty("Codecs", ", ".join(codecs_strings))
        channels = torrent.get_audio_channels()
        if channels:
            self.setProperty("Channels", ", ".join(channels))
        warnings = []
        if torrent.is_3d():
            warnings.append("3D")
        if torrent.is_widescreen():
            warnings.append("Widescreen")
        if torrent.is_hardcoded():
            warnings.append("Hardcoded")
        if torrent.is_black_white():
            warnings.append("Black&White")
        if len(warnings) > 0:
            self.setProperty("Warnings", ", ".join(warnings))
        if torrent.get_seeds() < 10:
            self.setProperty("SeedsError", str(True))
        return
