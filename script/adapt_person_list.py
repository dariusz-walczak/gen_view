#!/usr/bin/env python3

import argparse
import json
import os.path
import sys

def parse_options(args):
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "input", action="store", metavar="INPUT_FILE",
        help="Person list INPUT FILE path in JSON format")

    return parser.parse_args(args)


def adapt_person_list(context):
    family_name_missing = [
        person for person in context if person.get("name", {}).get("last") is None]

    def __group_by_known_family_names(context):
        person_map = {}

        for person in context:
            family_name = person.get("name", {}).get("last")

            if family_name is not None:
                person_map.setdefault(family_name, []).append(person)

        return person_map
    
    family_name_map = __group_by_known_family_names(context)

    family_name_grouped = []

    for family_name in sorted(family_name_map.keys()):
        persons = sorted(
            family_name_map[family_name], key=lambda person: person.get("name", {}).get("full"))

        entry = {
            "family_name": family_name,
            "persons": persons
        }
        family_name_grouped.append(entry)

    return {
        "by_last_name": {
            "unknown": family_name_missing,
            "grouped": family_name_grouped
        }
    }


def main(options):
    with open(options.input, 'r', encoding="utf-8") as f:
        context = json.load(f)

    print(
        json.dumps(
            adapt_person_list(context),
            indent=4))

    return 0


if __name__ == '__main__':
    sys.exit(main(parse_options(sys.argv[1:])))
