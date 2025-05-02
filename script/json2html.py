#!/usr/bin/env python3

import argparse
import json
import sys

from render import init_jinja_env

def parse_options(args):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--data-path", action="store", metavar="PATH", dest="data_path",
        help="PATH to the directory containing jinja templates")
    parser.add_argument(
        "-v", "--doc-version", action="store", metavar="NUM", dest="doc_version",
        help="The document version NUMber")
    parser.add_argument(
        "context", action="store", metavar="CONTEXT_FILE",
        help="jinja2 CONTEXT input FILE in json format")
    parser.add_argument(
        "template", action="store", metavar="TEMPLATE_NAME", help="jinja2 TEMPLATE NAME")

    return parser.parse_args(args)


def main(options):
    with open(options.context, 'r', encoding="utf-8") as f:
        context = json.load(f)

    env = init_jinja_env(options.data_path)
    template = env.get_template(options.template)
    print(template.render(context))

    return 0


if __name__ == '__main__':
    sys.exit(main(parse_options(sys.argv[1:])))
