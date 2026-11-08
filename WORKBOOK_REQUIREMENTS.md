# Requirements extracted from the EWB workbook

Source: `EWB_Phishing_URL_Checker_Workbook.pdf`, 22 pages, supplied locally.
The embedded text was decoded locally from PDF ASCII85/Flate content streams.
No requirements below were inferred from an unavailable document.

## Required behavior (Sections 01, 05, 06 and 07; pages 4, 7-12)

Python 3.10+, command-line input, standard library only. Strip outer whitespace;
return `No URL entered.` for empty text. If `://` is absent, prepend `http://`
for parsing (so omitted schemes trigger HTTP). Parse using `urllib.parse.urlparse`,
lowercase the hostname, and return `Could not identify a hostname.` if absent.
Print every detected indicator, in this order, with a cautious reminder:

| # | Exact starter condition | Exact warning message |
|---|---|---|
| 1 | `@` anywhere in candidate text | Contains an @ symbol; inspect carefully. |
| 2 | Trimmed original length strictly greater than 100 | Unusually long URL (over 100 characters). |
| 3 | Host matches `(?:\d{1,3}\.){3}\d{1,3}` in full | Uses an IP address instead of a familiar domain. |
| 4 | At least 5 nonempty dot-separated hostname parts | Contains many hostname segments/subdomains. |
| 5 | Lowercase hostname contains `xn--` | Contains a punycode-style hostname. |
| 6 | Lowercase parsed scheme equals `http` | Uses HTTP. HTTPS alone does not prove trust. |

If none match: `No listed warning signs found. This does NOT prove safety.`
Final starter reminder: `Never enter passwords from unexpected links.`
The IPv4-shaped regex does not validate octet ranges or cover IPv6. The punycode
check is a substring check. Retain these starter semantics and explain their limits.

No opening links, HTTP requests, DNS lookups, scanning, crawling, probing, malware
checks or reputation services. Never claim a definitive safe/malicious verdict.

## Exact five required inputs (Section 08; page 13)

| # | Sample input (type exactly) | Expected observation |
|---|---|---|
| 1 | `https://www.example.com/login` | May show no listed warning signs; not a safety guarantee. |
| 2 | `http://192.0.2.10/account` | Flags IP-address hostname and HTTP. |
| 3 | `http://example.com@sample.invalid/login` | Flags @ symbol and HTTP. |
| 4 | `https://a.b.c.d.e.example.invalid/path` | Flags many hostname segments. |
| 5 | `https://xn--example.invalid/` | Flags punycode-style hostname. |

## Testing and evidence (Sections 08-10; pages 13-16)

- Run all five examples, record input, expected, actual and PASS/FAIL in
  `tests/test_samples.md`, with Python version, OS, date and 2-3 lines of notes.
- Warning wording must match the starter. Record real output; fix failures and rerun.
- Rerun all five after improvements. At least two improvements are required, with
  what, why and verification explained in the README.
- Optional examples: empty input; `www.example.com` (HTTP warning);
  `https://secure-login.example.invalid` (no listed signs); `http://[bad`
  (starter crashes; suggested improvement C catches the parse error).
- Suggested improvements: A repeat/quit loop, B review summary, C malformed-input
  handling, D simple explanations, E clearer output formatting.
- `screenshots/sample_run.png`: actual terminal command, prompt, sample and output.
- `screenshots/test_results.png`: evidence of all five runs, or filled sample table
  open in VS Code. Show terminal path/command, readable text, no private information.
  Screenshots must be real PNG captures from the student's computer.

## Documentation and delivery (Sections 04, 11-13, 18)

Required names: `phishing_checker.py`, `README.md`, `requirements.txt` (comment
saying no dependencies), `tests/test_samples.md`, and both screenshot PNGs.
Workbook folder/repository name: `phishing-url-awareness`. This implementation
uses the user's existing `EWB-Cybersecurity` working folder; it can be renamed or
uploaded to a repository with the workbook's name later.

README sections: overview, features, requirements, how to run, example output,
testing, screenshots, improvements, limitations, ethical use and author details.
Screenshots must eventually render in the README using the exact relative paths.
Use your own words and be ready to explain the work (Sections 15-16).

Publish a public GitHub repo unless the coordinator instructs otherwise, inspect
the files/images, and verify access in a private browser window. Submit the
accessible repository URL through the internship team's designated method.
The workbook does not supply an EWB form URL. A screenshot alone is insufficient;
certificate issuance depends on successful submission and verification.

## Evaluation rubric (Section 14; page 19)

| Criterion | Marks | Full-mark expectations |
|---|---:|---|
| Working program | 25 | Runs without errors from a terminal, accepts input, handles empty input. |
| Detection logic | 20 | All six checks work; student explains each in simple words. |
| Testing and evidence | 20 | Five honest completed test rows and two clear screenshots. |
| README and documentation | 20 | Clear setup, usage, limitations, ethics; every section complete and written by student. |
| GitHub quality and explanation | 15 | Accessible public repo, neat structure, confident Section 15 answers. |
| Total | 100 | Completeness and understanding. |

## Submission checklist (Section 13; page 19)

- Program runs without errors from a terminal and accepts input.
- All six detection checks work and student can explain them.
- Five sample tests include input, expected, actual and pass/fail.
- At least two improvements are implemented and explained.
- README includes overview, features, requirements, usage, testing, screenshots,
  limitations, ethical use and improvements.
- Real readable screenshots show program/results and no private information.
- Public GitHub repo has visible files and opens in a private window.
- No passwords, API keys, private data, unrelated files or `__pycache__` folders.
- Student can explain behavior and limitations (Section 15).

Current completion status is tracked separately in `SUBMISSION_CHECKLIST.md`.
