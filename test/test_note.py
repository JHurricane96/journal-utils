import argparse
from pathlib import Path
from unittest.mock import mock_open, patch

from journal_utils.note import new


def test_new_existing_file(tmp_path: Path):
    args = argparse.Namespace(date="2022/01/01", force=False)
    cfg = {"journal_path": tmp_path, "location_type": "ip"}

    with (
        patch("builtins.print") as mock_print,
        patch("builtins.open", mock_open()) as mock_file_open,
        patch("geocoder.ip") as mock_geocoder,
    ):
        mock_geocoder.return_value.address = "Location"
        path = Path(cfg["journal_path"]) / "2022/01/01.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch()

        new(args, cfg)

        mock_print.assert_called_with(f"File {path} already exists.")
        mock_file_open.assert_not_called()


def test_new_valid_date(tmp_path: Path):
    args = argparse.Namespace(date="2022/01/01", force=False)
    cfg = {"journal_path": tmp_path, "location_type": "ip"}

    with (
        patch("builtins.print") as mock_print,
        patch("builtins.open", mock_open()) as mock_file_open,
        patch("geocoder.ip") as mock_geocoder,
    ):
        mock_geocoder.return_value.address = "Location"
        path = Path(cfg["journal_path"]) / "2022/01/01.md"

        new(args, cfg)

        mock_print.assert_called_with(f"Created {path}")
        mock_file_open.assert_called_with(path, "w")
        handle = mock_file_open()
        handle.write.assert_called_with("<small>Written in: Location</small>\n")


def test_new_invalid_date(tmp_path: Path):
    args = argparse.Namespace(date="2022/01/32", force=False)
    cfg = {"journal_path": tmp_path, "location_type": "ip"}

    with (
        patch("builtins.print") as mock_print,
        patch("builtins.open", mock_open()) as mock_file_open,
    ):
        new(args, cfg)

        mock_print.assert_called_with(
            "Invalid date format: 2022/01/32. Expected YYYY/MM/DD."
        )
        mock_file_open.assert_not_called()


def test_new_force_option(tmp_path: Path):
    args = argparse.Namespace(date="2022/01/01", force=True)
    cfg = {"journal_path": tmp_path, "location_type": "ip"}

    with (
        patch("builtins.print") as mock_print,
        patch("builtins.open", mock_open()) as mock_file_open,
        patch("geocoder.ip") as mock_geocoder,
    ):
        mock_geocoder.return_value.address = "Location"
        path = Path(cfg["journal_path"]) / "2022/01/01.md"

        new(args, cfg)

        mock_print.assert_called_with(f"Created {path}")
        mock_file_open.assert_called_with(path, "w")
        handle = mock_file_open()
        handle.write.assert_called_with("<small>Written in: Location</small>\n")
