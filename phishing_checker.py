"""Interactive entry point for the offline EWB awareness checker."""

from url_checker.cli import main
from url_checker.rules import inspect_url

__all__ = ["inspect_url", "main"]

if __name__ == "__main__":
    main()
