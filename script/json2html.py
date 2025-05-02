#!/usr/bin/env python3

import argparse
import json
import os.path
import re
import sys

import markdown

from parse import capitalize_word_list, parse_doc_index, parse_doc_name, parse_source
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
        "context", action="store", metavar="CONTEXT_FILE", help="jinja2 CONTEXT input FILE in json format")
    parser.add_argument(
        "template", action="store", metavar="TEMPLATE_NAME", help="jinja2 TEMPLATE NAME")

    return parser.parse_args(args)


def determine_auto_props(file_name):
    file_name = os.path.basename(file_name)
    index = parse_doc_index(file_name)
    full_title_raw = parse_doc_name(file_name)

    # Split the full title into subtitles
    subtitle_raw_list = re.split('_+', full_title_raw)
    subtitle_list = []

    for subtitle_raw in subtitle_raw_list:
        word_list = re.split('-+', subtitle_raw)
        subtitle_list.append(' '.join(capitalize_word_list(word_list)))

    return {
        "index": index,
        "title": ': '.join(subtitle_list)
    }


def main(options):
    with open(options.context, 'r', encoding="utf-8") as f:
        context = json.load(f)

    env = init_jinja_env(options.data_path)
    template = env.get_template(options.template)
    print(template.render(context))

    return 0


if __name__ == '__main__':
    sys.exit(main(parse_options(sys.argv[1:])))
