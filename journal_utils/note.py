from datetime import datetime
from pathlib import Path


def add(args, cfg):
    today = datetime.today().strftime("%Y/%m/%d")
    filename = f"{today}.md"
    path = Path(cfg["journal_path"]) / filename
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch()
        print(f"Created {path}")
    else:
        print(f"File {path} already exists.")
