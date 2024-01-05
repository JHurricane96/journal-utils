from datetime import datetime
from pathlib import Path

import geocoder
# import geopy

def new(args, cfg):
    if args.date:
        try:
            date = datetime.strptime(args.date, "%Y/%m/%d")
        except ValueError:
            print(f"Invalid date format: {args.date}. Expected YYYY/MM/DD.")
            return
    else:
        date = datetime.today()
    date_str = date.strftime("%Y/%m/%d")
    filename = f"{date_str}.md"
    path = Path(cfg["journal_path"]) / filename
    if path.exists() and not args.force:
        print(f"File {path} already exists.")
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        if cfg["location_type"] == "ip":
            location = geocoder.ip("me").address
        else:
            pass
        f.write(f"<small>Written in: {location}</small>\n")

    print(f"Created {path}")
