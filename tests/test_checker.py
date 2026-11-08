import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from phishing_checker import inspect_url
from url_checker.rules import analyze_url
from url_checker.cli import main
from tests.samples import SAMPLES


class WorkbookSamples(unittest.TestCase):
    def test_five_exact_samples(self):
        for url, expected in SAMPLES:
            with self.subTest(url=url):
                self.assertEqual(inspect_url(url), expected)


class RuleBoundaries(unittest.TestCase):
    def codes(self, url):
        return [w.code for w in analyze_url(url).warnings]

    def test_length_100_is_not_long(self):
        self.assertNotIn("long", self.codes("https://example.com/".ljust(100, "a")))

    def test_length_101_is_long(self):
        self.assertIn("long", self.codes("https://example.com/".ljust(101, "a")))

    def test_outer_whitespace_not_counted(self):
        self.assertNotIn("long", self.codes("  " + "https://example.com/".ljust(100, "a") + "  "))

    def test_four_segments(self):
        self.assertNotIn("segments", self.codes("https://a.b.example.invalid"))

    def test_five_segments(self):
        self.assertIn("segments", self.codes("https://a.b.c.example.invalid"))

    def test_empty_segments_not_counted(self):
        self.assertNotIn("segments", self.codes("https://a..b.example.invalid."))

    def test_at_in_path_still_matches_workbook(self):
        self.assertEqual(self.codes("https://example.com/a@b"), ["at"])

    def test_ip_in_path_not_host(self):
        self.assertNotIn("ip", self.codes("https://example.com/192.0.2.10"))

    def test_ipv4_shape_is_not_validation(self):
        self.assertIn("ip", self.codes("https://999.999.999.999/"))

    def test_ipv6_not_part_of_workbook_rule(self):
        self.assertNotIn("ip", self.codes("https://[2001:db8::1]/"))

    def test_punycode_only_in_host(self):
        self.assertNotIn("punycode", self.codes("https://example.com/xn--example"))

    def test_punycode_substring_matches_workbook(self):
        self.assertIn("punycode", self.codes("https://prefix-xn--example.invalid/"))

    def test_case_insensitive_host_and_scheme(self):
        self.assertEqual(self.codes("HTTP://XN--example.invalid/"), ["punycode", "http"])

    def test_missing_scheme_assumes_http(self):
        self.assertEqual(self.codes("www.example.com"), ["http"])
        self.assertTrue(analyze_url("www.example.com").assumed_http)

    def test_all_rules_accumulate_in_order(self):
        self.assertEqual(self.codes("http://example.com@1.2.3.4.5.xn--example.invalid/" + "a" * 101),
                         ["at", "long", "segments", "punycode", "http"])

    def test_ip_and_http_accumulate(self):
        self.assertEqual(self.codes("http://192.0.2.10/"), ["ip", "http"])

    def test_empty_input(self):
        self.assertEqual(inspect_url(" \t\n"), ["No URL entered."])

    def test_missing_hostname(self):
        self.assertEqual(inspect_url("https:///login"), ["Could not identify a hostname."])

    def test_malformed_brackets(self):
        self.assertEqual(inspect_url("http://[bad"), ["This text is not a valid URL format."])

    def test_unicode_authority_parse_error(self):
        self.assertEqual(inspect_url("http://example.com\uff0fpath"),
                         ["This text is not a valid URL format."])


class CliTests(unittest.TestCase):
    def run_cli(self, inputs):
        output = io.StringIO()
        with patch("builtins.input", side_effect=inputs), redirect_stdout(output):
            main()
        return output.getvalue()

    def test_loop_explanations_and_summary(self):
        out = self.run_cli([SAMPLES[1][0], SAMPLES[0][0], "q"])
        self.assertEqual(out.count("Result:"), 2)
        self.assertIn("Why 1:", out)
        self.assertIn("REVIEW CAREFULLY: 2 warning sign(s) found.", out)
        self.assertEqual(out.count("REVIEW CAREFULLY:"), 1)
        self.assertIn("This does NOT prove safety.", out)

    def test_invalid_and_empty_are_not_warning_counts(self):
        out = self.run_cli(["", "http://[bad", "exit"])
        self.assertNotIn("REVIEW CAREFULLY:", out)
        self.assertIn("No URL entered.", out)
        self.assertIn("not a valid URL format", out)

    def test_quit_aliases(self):
        for command in ("q", " QUIT ", "Exit"):
            with self.subTest(command=command):
                self.assertIn("Goodbye!", self.run_cli([command]))

    def test_eof_and_interrupt(self):
        for exception in (EOFError, KeyboardInterrupt):
            with self.subTest(exception=exception):
                self.assertIn("Goodbye!", self.run_cli([exception]))

    def test_assumption_disclosed(self):
        self.assertIn("assumed http://", self.run_cli(["www.example.com", "q"]))


if __name__ == "__main__":
    unittest.main()
