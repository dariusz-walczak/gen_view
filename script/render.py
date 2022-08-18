import jinja2


def init_jinja_env(data_path):
    return jinja2.Environment(
        optimized  = False,
        loader     = jinja2.FileSystemLoader(data_path),
        autoescape = False)
