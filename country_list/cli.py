import json

import click

from . import available_languages, countries_for_language

name = "country_list"


@click.group()
def cli():
    pass


@cli.command("list")
@click.option(
    "--simple", is_flag=True, help="Output only languages without country combination."
)
def list_(simple=False):
    for lang in available_languages():
        if not simple or "_" not in lang:
            click.echo(lang)


@cli.command()
@click.argument("lang", nargs=1)
@click.argument("country", nargs=-1, required=False, type=str.upper)
def show(lang, country):
    for country_code, country_name in countries_for_language(lang):
        if not country or country_code in country:
            click.echo("{} - {}".format(country_code, country_name))


@cli.command()
@click.argument("lang", nargs=-1, required=True)
@click.option("--small", is_flag=True, help="Output the json as small as possible.")
def export(lang, small):
    export_data = {}
    for language_name in lang:
        export_data[language_name] = dict(countries_for_language(language_name))

    json_dump_kwargs = {"sort_keys": True, "indent": 2}
    if small:
        json_dump_kwargs = {"sort_keys": True, "separators": (",", ":")}

    click.echo(json.dumps(export_data, **json_dump_kwargs))
