import uuid
from datetime import datetime

import gkeepapi
import requests

from journal_utils import note

JOURNAL_LABEL = "journal"
ARCHIVE_LABEL = "journal_archive"


def get_keep_instance(cfg):
    keep = gkeepapi.Keep()
    keep.resume(cfg["keep"]["username"], cfg["keep"]["token"])
    return keep


def get_journal_entries(keep):
    journal_label = keep.findLabel(JOURNAL_LABEL)
    if not journal_label:
        print(f"Error: no '{JOURNAL_LABEL}' label found in Google Keep.")
        print(f"Please create a '{JOURNAL_LABEL}' label in Google Keep.")
        return None, None

    journal_entries = keep.find(query="", labels=[journal_label])
    return journal_label, journal_entries


def _get_date_from_title(title: str):
    date = datetime.strptime(title, "%m/%d")
    cur_year_date = date.replace(year=datetime.today().year)
    prev_year_date = date.replace(year=datetime.today().year - 1)
    today = datetime.today()
    if abs(today - cur_year_date) < abs(prev_year_date - today):
        date = cur_year_date
    else:
        date = prev_year_date
    return date


def download(args, cfg):
    """
    Download all entries from Keep in the journal label and add them
    as local entries in the journal.
    """
    keep = get_keep_instance(cfg)
    journal_label, journal_entries = get_journal_entries(keep)

    if not journal_entries:
        return

    journal_entries = list(journal_entries)
    for entry in journal_entries:
        date = _get_date_from_title(entry.title)

        note._new(date, args.overwrite, cfg, verbose=False)
        note_path = note.get_path_from_date(date, cfg)

        img_dir = note_path.parent / "img"
        img_dir.mkdir(exist_ok=True, parents=True)
        imgs = []
        for image in entry.images:
            url = keep.getMediaLink(image)

            # Get the file extension from the Content-Disposition header of the response
            response = requests.get(url)
            content_disposition = response.headers["Content-Disposition"].split(";")
            if len(content_disposition) > 1 and content_disposition[0] == "attachment":
                file_ext = (
                    content_disposition[1].split("=")[1].strip('"').split(".")[-1]
                )
            else:
                file_ext = "jpg"

            file_name = f"{uuid.uuid4()}.{file_ext}"
            with open(img_dir / file_name, "wb") as f:
                f.write(response.content)
            imgs.append(f"![{file_name}](img/{file_name})")

        with open(note_path, "a") as f:
            for img in imgs:
                f.write(f"\n{img}\n")
            f.write(f"\n{entry.text}\n")

    if args.archive:
        _archive(keep, journal_label, journal_entries)


def _archive(keep, journal_label, journal_entries):
    archive_label = keep.findLabel(ARCHIVE_LABEL)
    if not archive_label:
        archive_label = keep.createLabel(ARCHIVE_LABEL)
    for entry in journal_entries:
        entry.labels.remove(journal_label)
        entry.labels.add(archive_label)
        entry.archived = True

    keep.sync()


def archive(args, cfg):
    """
    Archive all entries from Keep in the journal label.
    """
    keep = get_keep_instance(cfg)
    journal_label, journal_entries = get_journal_entries(keep)
    _archive(keep, journal_label, journal_entries)
    print(f"All entries in the '{JOURNAL_LABEL}' label have been archived.")


def peek(args, cfg):
    keep = get_keep_instance(cfg)
    journal_label, journal_entries = get_journal_entries(keep)
    if journal_label and not journal_entries:
        print(f"No entries found in the '{JOURNAL_LABEL}' label.")
        return

    num_entries = 0
    num_new_entries = 0
    num_edited_entries = 0
    for entry in journal_entries:
        num_entries += 1
        date = _get_date_from_title(entry.title)
        note_path = note.get_path_from_date(date, cfg)
        if not note_path.exists():
            num_new_entries += 1
        elif entry.timestamps.edited > datetime.fromtimestamp(
            note_path.stat().st_mtime
        ):
            num_edited_entries += 1

    print(f"{num_entries} entry/entries found in the '{JOURNAL_LABEL}' label.")
    print(f"{num_new_entries} entry/entries new.")
    print(f"{num_edited_entries} entry/entries edited.")
