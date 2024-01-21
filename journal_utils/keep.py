import uuid
from datetime import datetime

import gkeepapi
import requests

from journal_utils import note


def get_keep_instance(cfg):
    keep = gkeepapi.Keep()
    keep.resume(cfg["keep"]["username"], cfg["keep"]["token"])
    return keep


def get_journal_entries(keep):
    journal_label = keep.findLabel("journal")
    if not journal_label:
        print("Error: no 'journal' label found in Google Keep.")
        print("Please create a 'journal' label in Google Keep.")
        return None, None

    journal_entries = keep.find(query="", labels=[journal_label])
    return journal_label, journal_entries


def download(args, cfg):
    """
    Download all entries from Keep in the 'journal' label and add them
    as local entries in the journal.
    """
    keep = get_keep_instance(cfg)
    _, journal_entries = get_journal_entries(keep)

    if not journal_entries:
        return

    for entry in journal_entries:
        date = datetime.strptime(entry.title, "%m/%d")
        cur_year_date = date.replace(year=datetime.today().year)
        prev_year_date = date.replace(year=datetime.today().year - 1)
        today = datetime.today()
        if abs(today - cur_year_date) < abs(prev_year_date - today):
            date = cur_year_date
        else:
            date = prev_year_date

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


def archive(args, cfg):
    keep = get_keep_instance(cfg)
    journal_label, journal_entries = get_journal_entries(keep)
    archive_label = keep.findLabel("journal_archive")
    if not archive_label:
        archive_label = keep.createLabel("journal_archive")
    for entry in journal_entries:
        entry.labels.remove(journal_label)
        entry.labels.add(archive_label)
        entry.archived = True

    keep.sync()
