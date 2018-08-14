#!/usr/bin/env python

import argparse
import markdown
import os.path
import sys
import re

from parse import capitalize_word_list, parse_doc_index, parse_doc_name, parse_source
from render import adapt_str_req, adapt_unicode_opt, init_jinja_env

def parse_options(args):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--data-path", action="store", metavar="PATH", dest="data_path",
        help="PATH to the directory containing source documents")
    parser.add_argument(
        "-v", "--doc-version", action="store", metavar="NUM", dest="doc_version",
        help="The document version NUMber")
    parser.add_argument("input", action="store", metavar="INPUT", help="INPUT file to be parsed")

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
    ## @note Simplejson codes strings as unicode, so the context variable content doesn't need any
    #      conversion to unicode for jinja2 rendering purposes. The template variable is a simple
    #      str, so its conversion to unicode is required and is performed on jinja2 template
    #      construction stage.
    context, template = parse_source(open(options.input))
    context["inc_version"] = options.doc_version if options.doc_version is not None else 0

    auto_props = determine_auto_props(options.input)
    context.setdefault("index", auto_props["index"])
    context.setdefault("title", auto_props["title"])
    context["ititle"] = u"[{0:04d}] {1:s}".format(context["index"], context["title"])

    env = init_jinja_env(options.data_path)
    md_rendered = env.from_string(adapt_unicode_opt(template)).render(context)

    # For markdown extensions description see:
    # https://pythonhosted.org/Markdown/extensions/index.html

    context["content"] = markdown.markdown(
        md_rendered,
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.sane_lists',
            'markdown.extensions.smarty',
        ])

    ## @note Conversion to utf-8 stored in 8-bit string is required for the script to work with
    #      both, terminal printing as well as file redirection.
    #  @see https://stackoverflow.com/questions/4545661/unicodedecodeerror-when-redirecting-to-file
    print adapt_str_req(env.get_template("html/base.html").render(context))

    return 0


if __name__ == '__main__':
    sys.exit(main(parse_options(sys.argv[1:])))
