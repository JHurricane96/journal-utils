import argparse
import sys

import yaml

from journal_utils import keep, note, search

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
new_note_subparser.add_argument(
    "--date", "-d", help="Date of the note in YYYY/MM/DD format", default=None
)

keep_parser = subparsers.add_parser("keep")
keep_subparsers = keep_parser.add_subparsers(dest="keep_command")
download_subparser = keep_subparsers.add_parser("dl")
download_subparser.add_argument("--overwrite", "-o", action="store_true")
download_subparser.add_argument("-a", "--archive", action="store_true")
archive_subparser = keep_subparsers.add_parser("archive")
peek_subparser = keep_subparsers.add_parser("peek")


def load_yaml(path: str):
    with open(path) as f:
        return yaml.safe_load(f)


def error_and_exit():
    parser.print_help()
    print("Error: wrong/no command provided.")
    sys.exit(1)


def main():
    args = parser.parse_args()
    cfg = load_yaml(args.cfg)
    if args.command == "search":
        search(args, cfg)
    elif args.command == "note":
        if args.note_command == "new":
            note.new(args, cfg)
        else:
            error_and_exit()
    elif args.command == "keep":
        if args.keep_command == "dl":
            keep.download(args, cfg)
        elif args.keep_command == "archive":
            keep.archive(args, cfg)
        elif args.keep_command == "peek":
            keep.peek(args, cfg)
        else:
            error_and_exit()
    else:
        error_and_exit()


if __name__ == "__main__":
    main()
