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
note_subparsers.add_parser("add")


def load_yaml(path: str):
    with open(path) as f:
        return yaml.safe_load(f)


def main():
    args = parser.parse_args()
    cfg = load_yaml(args.cfg)
    if args.command == "search":
        search(args, cfg)
    elif args.command == "note":
        if args.note_command == "add":
            note.add(args, cfg)
        else:
            print("Wrong/No command provided.")
            sys.exit(1)
    else:
        print("Wrong/No command provided.")
        sys.exit(1)


if __name__ == "__main__":
    main()
