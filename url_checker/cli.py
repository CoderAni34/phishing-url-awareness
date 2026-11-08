"""Readable, repeatable terminal interface with safe exit handling."""

from url_checker.rules import analyze_url

CAUTION = "Awareness only: these clues do NOT prove a URL safe or malicious."


def main() -> None:
    print("EWB Phishing URL Awareness Checker")
    print("Text checks only - this program does not open URLs.")
    print(CAUTION)
    while True:
        try:
            raw = input("\nEnter a sample URL (or type q to quit): ")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye! Stay alert online.")
            return
        if raw.strip().lower() in ("q", "quit", "exit"):
            print("Goodbye! Stay alert online.")
            return
        result = analyze_url(raw)
        print("\nResult:")
        for message in result.messages:
            print("- " + message)
        for index, sign in enumerate(result.warnings, 1):
            print(f"  Why {index}: {sign.explanation}")
        if result.assumed_http:
            print("Note: assumed http:// for parsing because no scheme separator was supplied.")
        if result.warnings:
            print(f"REVIEW CAREFULLY: {len(result.warnings)} warning sign(s) found.")
        print(CAUTION)
        print("Never enter passwords from unexpected links.")
