import contextlib
import io
import json
import unittest

from country_list.__main__ import main

try:
    from click.testing import CliRunner

    click_installed = True
except ImportError:
    click_installed = False
else:
    from country_list.__main__ import cli


@unittest.skipUnless(click_installed, "click not installed")
class TestCli(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def test_list(self):
        result = self.runner.invoke(cli, ["list"])
        self.assertEqual(result.exit_code, 0, result)
        languages = [language for language in result.output.split("\n") if language]
        self.assertEqual(len(languages), 628)

    def test_list_simple(self):
        result = self.runner.invoke(cli, ["list", "--simple"])
        self.assertEqual(result.exit_code, 0, result)
        languages = [language for language in result.output.split("\n") if language]
        self.assertEqual(len(languages), 132)

    def test_show_all(self):
        result = self.runner.invoke(cli, ["show", "en"])
        self.assertEqual(result.exit_code, 0, result)
        countries = [country for country in result.output.split("\n") if country]
        self.assertEqual(len(countries), 249)

    def test_show_specific(self):
        result = self.runner.invoke(cli, ["show", "en", "se", "be"])
        self.assertEqual(result.exit_code, 0, result)
        self.assertEqual(result.output, "BE - Belgium\nSE - Sweden\n")

    def test_export(self):
        result = self.runner.invoke(cli, ["export", "en", "sv", "nl"])
        self.assertEqual(result.exit_code, 0, result)
        data = json.loads(result.output)
        self.assertEqual(set(data.keys()), {"en", "sv", "nl"})

    def test_export_small(self):
        result = self.runner.invoke(cli, ["export", "en", "sv", "nl", "--small"])
        self.assertEqual(result.exit_code, 0, result)
        data = json.loads(result.output)
        self.assertEqual(set(data.keys()), {"en", "sv", "nl"})


@unittest.skipIf(click_installed, "click installed")
class TestCliNoClick(unittest.TestCase):
    def test_cli_message(self):
        stdout = io.StringIO()
        with self.assertRaises(SystemExit):
            with contextlib.redirect_stdout(stdout):
                main()
        self.assertTrue(stdout.getvalue().startswith("ERROR"))
