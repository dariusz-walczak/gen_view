#!/usr/bin/env python3

import argparse
import copy
import datetime
import json
import logging
import sys


logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(messages)",
    stream=sys.stderr)

_LOG = logging.getLogger()


def parse_options(args):
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "input", action="store", metavar="INPUT_FILE",
        help="Person list INPUT FILE path in JSON format")

    return parser.parse_args(args)


def extract_year_from_iso_date(ctx, field_name):
    person_id = ctx.get("id", "P?????")

    try:
        iso_birth_date = ctx[field_name]
    except KeyError as e:
        _LOG.debug(
            "Failed to extract the '%s' field from the person ('%s') context:\n    %s",
            field_name, person_id, str(e))
        return None

    try:
        parsed_date = datetime.date.fromisoformat(iso_birth_date)
    except (TypeError, ValueError) as e:
        _LOG.debug(
            "Failed to convert the value (%s) of the '%s' field of the person ('%s') context:\n"
            "    %s", iso_birth_date, field_name, person_id, str(e))
        return None

    return parsed_date.year


def adapt_person_details(person_ctx: dict) -> dict:
    """Adapt the input person context to include all useful, derived data.

    Args:
        person_ctx: The person context to be adapted

    Returns:
        dict: An adapted copy of the input person context
    """
    # Consider removing the following deep copy when there is a need to optimize:
    person_ctx = copy.deepcopy(person_ctx)

    birth_year = extract_year_from_iso_date(person_ctx, "birth_date")
    if birth_year is not None:
        person_ctx["birth_year"] = birth_year

    death_year = extract_year_from_iso_date(person_ctx, "death_date")
    if death_year is not None:
        person_ctx["death_year"] = death_year

    return person_ctx


def adapt_each_person(context: list[dict]) -> list[dict]:
    """Adapt each person context in the input list to include all useful, derived data.
    """
    return [adapt_person_details(p) for p in context]


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
            adapt_person_list(
                adapt_each_person(context)),
            indent=4))

    return 0


if __name__ == '__main__':
    sys.exit(main(parse_options(sys.argv[1:])))
