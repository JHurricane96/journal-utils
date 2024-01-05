import argparse
import sys

import yaml

from journal_utils import note, search

parser = argparse.ArgumentParser()

parser.add_argument("--cfg", default="config.yaml")

subparsers = parser.add_subparsers(dest="command")

search_parser = subparsers.add_parser("search")
search_parser.add_argument("--type", "-t", choices=["tag", "body"])
search_parser.add_argument("query")

note_parser = subparsers.add_parser("note")
note_subparsers = note_parser.add_subparsers(dest="note_command")
new_note_subparser = note_subparsers.add_parser("new")
new_note_subparser.add_argument("--force", "-f", action="store_true")
new_note_subparser.add_argument("--date", "-d", help="Date of the note in YYYY/MM/DD format", default=None)


def load_yaml(path: str):
    with open(path) as f:
        return yaml.safe_load(f)


def main():
    args = parser.parse_args()
    cfg = load_yaml(args.cfg)
    if args.command == "search":
        search(args, cfg)
    elif args.command == "note":
        if args.note_command == "new":
            note.new(args, cfg)
        else:
            parser.print_help()
            print("Error: wrong/no command provided.")
            sys.exit(1)
    else:
        parser.print_help()
        print("Error: wrong/no command provided.")
        sys.exit(1)


if __name__ == "__main__":
    main()
