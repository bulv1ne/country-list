import argparse
import json

from . import available_languages, countries_for_language

parser = argparse.ArgumentParser(
    "country_list", description="List available countries and country codes",
)
parser.set_defaults(func=None)

subparsers = parser.add_subparsers(title="available commands")

list_parser = subparsers.add_parser("list", help="List all available languages.")
list_parser.set_defaults(func="list")
list_parser.add_argument("--simple", action="store_true")

country_for_language_parser = subparsers.add_parser(
    "show",
    help=(
        "Show countries for a specific language."
        " Add country code to only show that country."
    ),
)
country_for_language_parser.set_defaults(func="show")
country_for_language_parser.add_argument("lang")
country_for_language_parser.add_argument("country", nargs="*", type=str.upper)


export_parser = subparsers.add_parser("export", help="Export countries to json")
export_parser.set_defaults(func="export")
export_parser.add_argument("lang", nargs="+")


if __name__ == "__main__":
    args = parser.parse_args()
    if args.func == "list":
        for lang in available_languages():
            if not args.simple or "_" not in lang:
                print(lang)
    elif args.func == "show":
        for country_code, country_name in countries_for_language(args.lang):
            if not args.country or country_code in args.country:
                print("{} - {}".format(country_code, country_name))
    elif args.func == "export":
        export_data = {}
        for lang in args.lang:
            export_data[lang] = dict(countries_for_language(lang))

        print(json.dumps(export_data, indent=2, sort_keys=True))
