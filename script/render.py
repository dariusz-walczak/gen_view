import datetime
import gettext
import sys

import jinja2

import notes

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


def init_jinja_env(data_path, locale_path=None):
    extensions = [] if locale_path is None else ["jinja2.ext.i18n"]

    env = jinja2.Environment(
        optimized  = False,
        loader     = jinja2.FileSystemLoader(data_path),
        extensions = extensions,
        autoescape = False)
    env.filters["year"] = _extract_year_filter
    env.globals["render_note"] = notes.render_note

    if locale_path is not None:
        translations = gettext.translation(
            domain = "messages",
            localedir = locale_path,
            languages = ["en"])
        # make the `_` function and the `{% trans %}` block available in templates rendered using
        #  this jinja2 environment:
        env.install_gettext_translations(translations, newstyle=True) # pylint: disable=no-member
        translations.install() # make the `_` global function available in python code

    return env
