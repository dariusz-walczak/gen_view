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
    else:
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
    else:
        return None


def parse_future_task_list(sio):
    task_pattern = re.compile(
        r"^\* TASK/"
        r"(?P<date>\d{4}-\d{2}-\d{2})/"
        r"(?P<time>..:..)/"
        r"(?P<desc>.+)$", re.IGNORECASE)

    tasks = []

    for line in sio:
        task_match = task_pattern.match(line)

        if task_match is not None:
            task = {
                "date": parse_date(task_match.group("date")),
                "time": parse_time(task_match.group("time")),
                "desc": unicode(task_match.group("desc"), "utf8")
            }
            tasks.append(task)

    return tasks


def parse_monthly_task_list(sio):
    task_pattern = re.compile(
        r"^\* TASK/"
        r"(?P<day>[1-9]|0[1-9]|[12][0-9]|3[01])/"
        r"(?P<time>..:..)/"
        r"(?P<desc>.+)$", re.IGNORECASE)

    tasks = []

    for line in sio:
        task_match = task_pattern.match(line)

        if task_match is not None:
            task = {
                "day_of_month": int(task_match.group("day")),
                "time": parse_time(task_match.group("time")),
                "desc": unicode(task_match.group("desc"), "utf8")
            }
            tasks.append(task)

    return tasks


def parse_weekly_task_list(sio):
    task_pattern = re.compile(
        r"^\* TASK/"
        r"(?P<dow>MON|TUE|WED|THU|FRI|SAT|SUN)/"
        r"(?P<time>..:..)/"
        r"(?P<desc>.+)$", re.IGNORECASE)

    tasks = []

    for line in sio:
        task_match = task_pattern.match(line)
        if task_match is not None:
            task = {
                "day_of_week": task_match.group("dow").upper(),
                "time": parse_time(task_match.group("time")),
                "desc": unicode(task_match.group("desc"), "utf8")
            }
            tasks.append(task)

    return tasks


def parse_doc_index(file_name):
    m = re.match(r"^(?P<idx>\d+)_.*", file_name)

    if m is not None:
        return int(m.group("idx"))
    else:
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
    elif word_cnt == 1:
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
    else:
        return None
