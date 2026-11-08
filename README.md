# Phishing URL Awareness Checker

My final mini-project for the EWB AI Powered Cyber Security Internship.

## Web demo

[Open the live URL checker](https://coderani34.github.io/phishing-url-awareness/)

The browser version lives in [`docs/`](docs/). It checks URL text locally using
JavaScript; entered URLs are never fetched, uploaded or saved. The Python CLI
below remains the original internship implementation. The web parser is a small
adaptation, not a full equivalent of Python's URL parser or a URL validator.

Run the optional browser-rule checks with `node tests/test_web.cjs` (Node.js is
only needed to run these extra web tests, not to use the website or Python CLI).
All 25 browser-rule checks pass, including the five exact workbook samples.
GitHub Pages reports a successful public build. Visual browser QA could not be
completed in the development session because browser access was unavailable.

Phishing links try to trick people into sharing passwords or other sensitive information. This project is a small Python command-line tool that checks URL text for six warning signs from the EWB workbook. It does not open the link or connect to any website.

## Requirements

- Python 3.10 or later
- No extra packages, API keys or internet connection needed to run the checker

`requirements.txt` contains only a comment because the project uses Python's standard library.

## How to run

Download or clone this repository, open a terminal in the project folder, and run:

```powershell
python -B phishing_checker.py
```

On macOS or Linux, use `python3` instead of `python`.

On my Windows PC, the Python alias did not work, so I used:

```powershell
& "$env:LOCALAPPDATA\Python\bin\python.exe" -B phishing_checker.py
```

Enter a sample URL when prompted. You can check more than one URL in the same session. Type `q`, `quit` or `exit` to close the program. Ctrl+C also exits cleanly.

## What it checks

| Warning sign | Rule used |
|---|---|
| @ symbol | Flags `@` anywhere in the URL text. |
| Long URL | Flags more than 100 characters after removing spaces at the ends. |
| IP-style hostname | Flags a hostname matching four groups of 1 to 3 digits separated by dots. |
| Many hostname segments | Flags five or more nonempty parts separated by dots. |
| Punycode marker | Flags `xn--` anywhere in the hostname, ignoring case. |
| HTTP | Flags the HTTP scheme. HTTPS alone does not prove a site is trustworthy. |

These rules follow the workbook's starter behavior. If a scheme is missing, the checker assumes `http://` for parsing and explains this in the output. Empty input and missing hostnames get a clear message.

The checks are deliberately simple. For example, the IP-style rule does not validate the numbers or detect IPv6. The @ rule also flags the symbol in a path or query. Long URLs, international domain names and hosts with many parts can all be legitimate.

## Improvements over the starter

- **Repeat checks without restarting:** a loop lets you enter another URL or quit. Tests cover repeated inputs, quit commands and Ctrl+C/end-of-input.
- **Handle malformed input:** inputs such as `http://[bad` show a format message instead of crashing. Tests also cover empty input, missing hosts and Unicode parsing errors.
- **Explain warnings:** each detected sign includes a short explanation of why it matters and where the rule can be misleading.
- **Show a review summary:** the output counts warning signs and says `REVIEW CAREFULLY`. Input errors are not counted as warnings.

The five workbook samples still pass after these changes.

## Example output

For `http://192.0.2.10/account`, the warning lines are:

```text
Result:
- Uses an IP address instead of a familiar domain.
- Uses HTTP. HTTPS alone does not prove trust.
```

The program then explains both warnings and prints:

```text
REVIEW CAREFULLY: 2 warning sign(s) found.
Awareness only: these clues do NOT prove a URL safe or malicious.
Never enter passwords from unexpected links.
```

## Testing

The recorded local run used Python 3.15.2 on Windows 11:

```text
Ran 26 tests in 0.003s
OK
```

All five workbook examples passed:

| Sample input | Expected result | Actual result |
|---|---|---|
| `https://www.example.com/login` | No listed warning signs; not a safety guarantee | Matches - PASS |
| `http://192.0.2.10/account` | IP-style hostname and HTTP | Matches - PASS |
| `http://example.com@sample.invalid/login` | @ symbol and HTTP | Matches - PASS |
| `https://a.b.c.d.e.example.invalid/path` | Many hostname segments | Matches - PASS |
| `https://xn--example.invalid/` | Punycode-style hostname | Matches - PASS |

The full expected and actual messages are in [tests/test_samples.md](tests/test_samples.md). The [test log](tests/test_run.txt) and [CLI transcripts](tests/cli_runs.txt) contain the recorded results.

To run the checks yourself:

```powershell
python -B -m unittest discover -s tests -v
python -B -m tests.run_samples
```

To regenerate the sample-results table:

```powershell
python -B -m tests.run_samples --write
```

The automated tests also cover the 100/101-character boundary, four/five hostname parts, upper-case schemes, malformed inputs and the CLI loop. All test inputs are local strings; none are visited.

## Screenshots

I captured these from PowerShell on my PC.

**Sample run**

![Sample run](screenshots/sample_run.png?v=89208a1)

**Five sample checks**

![Test results](screenshots/test_results.png)

The last URL in the second screenshot omits the trailing `/`. It gives the same warning. The exact workbook input, including the slash, is covered in the automated results.

To take new screenshots, run the CLI or `python -B -m tests.run_samples`, then use Win+Shift+S. Keep the command and results readable and save the images in `screenshots/`.

## Limitations

No warning signs does **not** mean a URL is safe. A phishing URL can avoid all six checks, and a legitimate URL can trigger several of them.

The tool only reads text. It makes no network requests or DNS lookups, visits no websites, and does no crawling or scanning. It cannot inspect page content, redirects, certificates, malware, ownership or reputation. Parsing a string successfully does not make it a valid or trustworthy URL.

It also misses things such as encoded @ symbols, Unicode look-alikes without an `xn--` marker and alternative numeric host formats. It does not save a history of entered URLs.

## Ethical use

This project is for defensive learning with workbook samples and synthetic strings. Do not use it to send phishing messages, collect credentials or probe websites. Do not put passwords, tokens or private URLs in screenshots or the repository.

## Project structure

```text
phishing_checker.py          Entry point
url_checker/
  __init__.py
  rules.py                   Six checks and results
  cli.py                     Interactive terminal interface
tests/
  __init__.py
  samples.py                 Workbook samples and expectations
  test_checker.py            Automated tests
  run_samples.py             Sample runner
  test_samples.md            Expected and actual results
  test_run.txt               Test log
  cli_runs.txt               CLI transcripts
screenshots/
  README.md
  sample_run.png
  test_results.png
docs/                        Browser-only web demo (GitHub Pages)
README.md
WORKBOOK_REQUIREMENTS.md
SUBMISSION_CHECKLIST.md
requirements.txt
.gitignore
```

[WORKBOOK_REQUIREMENTS.md](WORKBOOK_REQUIREMENTS.md) records the workbook requirements and rubric. [SUBMISSION_CHECKLIST.md](SUBMISSION_CHECKLIST.md) tracks the remaining submission steps. The original workbook and raw extraction are kept locally and excluded from Git. The `-B` option avoids creating Python cache folders.

## Author

**Aniket**  
AI Powered Cyber Security Internship  
EWB EDUTECH PRIVATE LIMITED

Role: Cyber Security Intern. Programme start date: 28 September 2026. Duration: 4 weeks.

## AI assistance

I used OpenAI Codex to extract the workbook requirements, generate the code, tests and documentation, and run local checks. I reviewed the project and took the screenshots myself. Codex also helped revise this README. This project involved substantial AI assistance; it was not written entirely without AI.

Codex also generated the browser demo and its JavaScript tests.
