"""Workbook-compatible heuristics, kept separate from terminal interaction."""

from dataclasses import dataclass
import re
from urllib.parse import urlparse


@dataclass(frozen=True)
class WarningSign:
    code: str
    message: str
    explanation: str


SIGNS = (
    WarningSign("at", "Contains an @ symbol; inspect carefully.",
                "In the authority, text before @ is user information, not the destination. "
                "This broad rule also flags @ in paths or queries."),
    WarningSign("long", "Unusually long URL (over 100 characters).",
                "Long text can make a destination harder to read. Honest links can also be long."),
    WarningSign("ip", "Uses an IP address instead of a familiar domain.",
                "A numeric hostname can obscure identity. Internal tools may use one legitimately. "
                "This workbook rule matches IPv4-style text, not validated IP addresses."),
    WarningSign("segments", "Contains many hostname segments/subdomains.",
                "Five or more nonempty dot-separated parts can make the host confusing. "
                "Legitimate services can also have many parts."),
    WarningSign("punycode", "Contains a punycode-style hostname.",
                "The xn-- marker can represent international names, including look-alike letters. "
                "International names are also used legitimately."),
    WarningSign("http", "Uses HTTP. HTTPS alone does not prove trust.",
                "HTTP does not encrypt traffic. HTTPS encryption alone does not establish honesty."),
)
NO_SIGNS = "No listed warning signs found. This does NOT prove safety."


@dataclass(frozen=True)
class Inspection:
    warnings: tuple[WarningSign, ...] = ()
    notice: str = ""
    assumed_http: bool = False

    @property
    def messages(self) -> list[str]:
        return [sign.message for sign in self.warnings] or [self.notice or NO_SIGNS]


def analyze_url(raw_url: str) -> Inspection:
    """Inspect text using the six Section 06 rules, in workbook order.

    Deliberately retain the workbook's IPv4-shaped regex and substring
    punycode rule. This is not a URL validator or a browser URL parser.
    """
    url = raw_url.strip()
    if not url:
        return Inspection(notice="No URL entered.")
    assumed = "://" not in url
    candidate = "http://" + url if assumed else url
    # urlparse can reject malformed brackets and invalid Unicode authorities.
    try:
        parsed = urlparse(candidate)
        host = (parsed.hostname or "").lower()
    except ValueError:
        return Inspection(notice="This text is not a valid URL format.", assumed_http=assumed)
    if not host:
        return Inspection(notice="Could not identify a hostname.", assumed_http=assumed)
    matched = (
        "@" in candidate,
        len(url) > 100,
        re.fullmatch(r"(?:\d{1,3}\.){3}\d{1,3}", host) is not None,
        len([part for part in host.split(".") if part]) >= 5,
        "xn--" in host,
        parsed.scheme.lower() == "http",
    )
    return Inspection(tuple(sign for sign, found in zip(SIGNS, matched) if found),
                      assumed_http=assumed)


def inspect_url(raw_url: str) -> list[str]:
    """Return the same warning lines as the workbook's public function."""
    return analyze_url(raw_url).messages
