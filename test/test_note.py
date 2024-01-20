import argparse
from pathlib import Path
from unittest.mock import mock_open, patch

from journal_utils.note import new


@patch("geocoder.ip")
@patch("builtins.open", new_callable=mock_open)
@patch("builtins.print")
def test_new_existing_file(mock_print, mock_file_open, mock_geocoder, tmp_path: Path):
    args = argparse.Namespace(date="2022/01/01", force=False)
    cfg = {"journal_path": tmp_path, "location_type": "ip"}

    mock_geocoder.return_value.address = "Location"
    path = Path(cfg["journal_path"]) / "2022/01/01.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch()

    new(args, cfg)

    mock_print.assert_called_with(f"File {path} already exists.")
    mock_file_open.assert_not_called()


@patch("geocoder.ip")
@patch("builtins.open", new_callable=mock_open)
@patch("builtins.print")
def test_new_valid_date(mock_print, mock_file_open, mock_geocoder, tmp_path: Path):
    args = argparse.Namespace(date="2022/01/01", force=False)
    cfg = {"journal_path": tmp_path, "location_type": "ip"}

    mock_geocoder.return_value.address = "Location"
    path = Path(cfg["journal_path"]) / "2022/01/01.md"

    new(args, cfg)

    mock_print.assert_called_with(f"Created {path}")
    mock_file_open.assert_called_with(path, "w")
    handle = mock_file_open()
    handle.write.assert_called_with("<small>Written in: Location</small>\n")


@patch("builtins.open", new_callable=mock_open)
@patch("builtins.print")
def test_new_invalid_date(mock_print, mock_file_open, tmp_path: Path):
    args = argparse.Namespace(date="2022/01/32", force=False)
    cfg = {"journal_path": tmp_path, "location_type": "ip"}

    new(args, cfg)

    mock_print.assert_called_with(
        "Invalid date format: 2022/01/32. Expected YYYY/MM/DD."
    )
    mock_file_open.assert_not_called()


@patch("geocoder.ip")
@patch("builtins.open", new_callable=mock_open)
@patch("builtins.print")
def test_new_force_option(mock_print, mock_file_open, mock_geocoder, tmp_path: Path):
    args = argparse.Namespace(date="2022/01/01", force=True)
    cfg = {"journal_path": tmp_path, "location_type": "ip"}

    mock_geocoder.return_value.address = "Location"
    path = Path(cfg["journal_path"]) / "2022/01/01.md"

    new(args, cfg)

    mock_print.assert_called_with(f"Created {path}")
    mock_file_open.assert_called_with(path, "w")
    handle = mock_file_open()
    handle.write.assert_called_with("<small>Written in: Location</small>\n")
