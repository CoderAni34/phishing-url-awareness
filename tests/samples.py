"""Exact Section 08 sample strings and independently specified expectations."""

SAMPLES = (
    ("https://www.example.com/login",
     ["No listed warning signs found. This does NOT prove safety."]),
    ("http://192.0.2.10/account",
     ["Uses an IP address instead of a familiar domain.",
      "Uses HTTP. HTTPS alone does not prove trust."]),
    ("http://example.com@sample.invalid/login",
     ["Contains an @ symbol; inspect carefully.",
      "Uses HTTP. HTTPS alone does not prove trust."]),
    ("https://a.b.c.d.e.example.invalid/path",
     ["Contains many hostname segments/subdomains."]),
    ("https://xn--example.invalid/",
     ["Contains a punycode-style hostname."]),
)
