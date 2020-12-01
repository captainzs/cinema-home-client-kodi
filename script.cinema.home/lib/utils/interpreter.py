def duration_2_readable(seconds):
    hours = seconds // 3600
    minutes = seconds % 3600 // 60
    seconds = seconds % 60
    return "{}h {}m".format(hours, minutes)


def bytes_2_readable(number_of_bytes):
    if number_of_bytes < 0:
        return 'null'
    step_to_greater_unit = 1024.
    number_of_bytes = float(number_of_bytes)
    unit = 'bytes'
    if (number_of_bytes / step_to_greater_unit) >= 1:
        number_of_bytes /= step_to_greater_unit
        unit = 'KB'
    if (number_of_bytes / step_to_greater_unit) >= 1:
        number_of_bytes /= step_to_greater_unit
        unit = 'MB'
    if (number_of_bytes / step_to_greater_unit) >= 1:
        number_of_bytes /= step_to_greater_unit
        unit = 'GB'
    if (number_of_bytes / step_to_greater_unit) >= 1:
        number_of_bytes /= step_to_greater_unit
        unit = 'TB'
    precision = 1
    number_of_bytes = round(number_of_bytes, precision)
    return str(number_of_bytes) + ' ' + unit


def resolution_2_readable(resolution):
    if resolution == "x480":
        return "SD"
    elif resolution == "x720":
        return "HD-Ready"
    elif resolution == "x1080":
        return "Full-HD"
    elif resolution == "x1440":
        return "2K Quad-HD"
    elif resolution == "x2160":
        return "4K Ultra-HD"
    elif resolution == "x2880":
        return "5K Ultra-HD"
    elif resolution == "x4320":
        return "8K Ultra-HD"
    return resolution


def language_2_readable(source_id):
    switcher = {
        0: "Hungarian",
        1: "English",
        2: "Italian",
        3: "German",
        4: "Russian",
        5: "Danish",
        6: "Portugal",
        7: "French",
        8: "Hindi"
    }
    return switcher.get(source_id, "Unknown")


def source_2_readable(source_id):
    switcher = {
        0: "Camera",
        1: "HD Camera",
        2: "Telesync",
        3: "HD Telesync",
        4: "Workprint",
        5: "VHS Casettte",
        6: "HD VHS Casettte",
        7: "Pay-Per-View Service",
        8: "Screener",
        9: "HD Screener",
        10: "DVD Rip",
        11: "HD DVD Rip",
        12: "DVD",
        13: "HD DVD",
        14: "TV",
        15: "HD TV",
        16: "Web",
        17: "Streaming Service",
        18: "BluRay",
        19: "HD BluRay",
        20: "UHD BluRay"
    }
    return switcher.get(source_id, "Unknown")


def video_codec_2_readable(codec_id):
    switcher = {
        0: "DivX",
        1: "XviD",
        2: "MPEG-2",
        3: "MPEG-4",
        4: "x264",
        5: "MVC",
        6: "x265",
        7: "VC-1",
        8: "VP-9"
    }
    return switcher.get(codec_id, "Unknown")


def audio_codec_2_readable(codec_id):
    switcher = {
        0: "MP2",
        1: "MP3",
        2: "AAC",
        3: "Dolby Digital",
        4: "Dolby Digital+",
        5: "DTS",
        6: "DTS-ES",
        7: "FLAC",
        8: "Dolby Atmos TrueHD",
        9: "DTS-HD",
        10: "DTS:X",
        11: "PCM"
    }
    return switcher.get(codec_id, "Unknown")


def color_codec_2_readable(codec_id):
    switcher = {
        0: "PAL",
        1: "NTSC",
        2: "SECAM"
    }
    return switcher.get(codec_id, "Unknown")


def flag_2_img(flag_id):
    switcher = {
        0: "hun.png",
        1: "eng.png",
        2: "ita.png",
        3: "ger.png",
        4: "rus.png",
        5: "dnk.png",
        6: "por.png",
        7: "fra.png",
        8: "ind.png"
    }
    return switcher.get(flag_id, "usa.png")


def show_status_2_readable(status_id):
    switcher = {
        0: "Returning",
        1: "Planned",
        2: "In Production",
        3: "Ended",
        4: "Cancelled",
        5: "Pilot"
    }
    return switcher.get(status_id, "Unknown Status")
