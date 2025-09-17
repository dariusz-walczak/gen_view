#!/usr/bin/env python3

import argparse
import json
import os.path
import sys

import jinja2

from render import init_jinja_env

def parse_options(args):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-b", "--base-dir", action="store", metavar="PATH", dest="base_path", default=".",
        help="The output document tree base PATH")
    parser.add_argument(
        "--res-dir", action="store", metavar="PATH", dest="res_dir_path",
        help=(
            "The resources output tree base PATH if different than the output document tree base"
            " path (see: --base-path)"))
    parser.add_argument(
        "-d", "--data-dir", action="store", metavar="PATH", dest="data_path",
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

    context.setdefault("config", {}).setdefault("path", {})["base"] = options.base_path

    if options.res_dir_path is not None:
        context["config"]["path"]["res"] = options.res_dir_path
    else:
        context["config"]["path"]["res"] = options.base_path

    html_template_path = os.path.join(options.data_path, "html")

    env = init_jinja_env(html_template_path)
    try:
        template = env.get_template(options.template)
    except jinja2.exceptions.TemplateNotFound as e:
        print(
            f"ERROR: The '{options.template}' template not found under the '{html_template_path}'"
            " path", file=sys.stderr)
        return 1;

    print(template.render(context))

    return 0


if __name__ == '__main__':
    sys.exit(main(parse_options(sys.argv[1:])))
