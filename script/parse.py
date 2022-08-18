import datetime
import re
import simplejson


def parse_source(sio):
    separator_pattern = re.compile("^====*$")

    raw_part_1 = ""
    raw_part_2 = None

    for line in sio:
        if separator_pattern.match(line) is None:
            raw_part_1 += line
        else:
            raw_part_2 = ""
            break

    for line in sio:
        raw_part_2 += line

    if raw_part_2 is None:
        return ({}, raw_part_1)

    return (simplejson.loads(raw_part_1), raw_part_2)


def parse_date(s, default=None):
    try:
        return datetime.datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        return default


def parse_time(s):
    time_pattern = re.compile(r"^(?P<hour>(?:[01][0-9]|2[0-3])):(?P<mins>[0-5][0-9])$")
    time_match = time_pattern.match(s)
    if time_match is not None:
        return datetime.time(
            hour=int(time_match.group("hour")),
            minute=int(time_match.group("mins")))

    return None


def parse_doc_index(file_name):
    m = re.match(r"^(?P<idx>\d+)_.*", file_name)

    if m is not None:
        return int(m.group("idx"))

    return None


def capitalize_word_list(word_list):
    articles = ('a', 'an', 'the')
    # Coordinating conjunctions:
    cconj = ('and', 'but', 'for', 'nor', 'or', 'so', 'yet')
    # Prepositions:
    prepos = (
        'ago', 'at', 'by', 'for', 'from', 'in', 'into', 'of', 'off', 'on', 'onto', 'over', 'past',
        'since', 'till', 'to')
    exceptions = articles + cconj + prepos

    word_cnt = len(word_list)

    if word_cnt == 0:
        return []

    if word_cnt == 1:
        return [word_list[0].capitalize()]

    res_list = [word_list[0].capitalize()]

    for word in word_list[1:-1]:
        if word.lower() in exceptions:
            res_list.append(word.lower())
        else:
            res_list.append(word.capitalize())

    res_list.append(word_list[-1].capitalize())

    return res_list


def parse_doc_name(file_name):
    m = re.match(r"^(?:\d+_)?(?P<title>.*)\.\w+$", file_name)

    if m is not None:
        return m.group("title")

    return None
