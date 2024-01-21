from datetime import datetime
from pathlib import Path

import geocoder

# import geopy


def get_path_from_date(date: datetime, cfg):
    date_str = date.strftime("%Y/%m/%d")
    return Path(cfg["journal_path"]) / f"{date_str}.md"


def _new(date: datetime, force: bool, cfg, verbose: bool = False):
    path = get_path_from_date(date, cfg)
    if path.exists() and not force:
        if verbose:
            print(f"File {path} already exists.")
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        if cfg["location_type"] == "ip":
            location = geocoder.ip("me").address
        else:
            pass
        f.write(f"<small>Written in: {location}</small>\n")

    if verbose:
        print(f"Created {path}")


def new(args, cfg):
    if args.date:
        try:
            date = datetime.strptime(args.date, "%Y/%m/%d")
        except ValueError:
            print(f"Invalid date format: {args.date}. Expected YYYY/MM/DD.")
            return
    else:
        date = datetime.today()
    _new(date, args.force, cfg, verbose=True)
