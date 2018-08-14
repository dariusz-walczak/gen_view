import jinja2


def init_jinja_env(data_path):
    return jinja2.Environment(
        optimized  = False,
        loader     = jinja2.FileSystemLoader(data_path),
        autoescape = False)


def adapt_str_req(value):
    if isinstance(value, str):
        return value
    elif isinstance(value, unicode):
        return value.encode("utf-8", "replace")
    else:
        return str(value)


def adapt_unicode_opt(value):
    if value is not None:
        return adapt_unicode_req(value)
    else:
        return u""


def adapt_unicode_req(value):
    assert value is not None

    if isinstance(value, str):
        return unicode(value, "utf8")
    elif isinstance(value, unicode):
        return value
    else:
        return unicode(value)
