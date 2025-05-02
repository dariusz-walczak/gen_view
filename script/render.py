import datetime
import sys

import jinja2


# Return the year extracted from the input date string.
def _extract_year_filter(raw_date):
    try:
        return datetime.date.fromisoformat(raw_date).year
    except ValueError:
        pass

    try:
        return datetime.datetime.strptime(raw_date, "%Y-%m").date().year
    except ValueError:
        pass

    try:
        return datetime.datetime.strptime(raw_date, "%Y").date().year
    except ValueError:
        pass

    sys.stderr.write(f"_extract_year: Failed to parse the '{raw_date}' date string\n")

    return None


def init_jinja_env(data_path):
    env = jinja2.Environment(
        optimized  = False,
        loader     = jinja2.FileSystemLoader(data_path),
        autoescape = False)
    env.filters["year"] = _extract_year_filter
    return env
