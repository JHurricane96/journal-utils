import argparse
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock, mock_open, patch

from journal_utils import keep


class FakeDate(datetime):
    "A fake replacement for datetime that can be mocked for testing."

    def __new__(cls, *args, **kwargs):
        return datetime.__new__(datetime, *args, **kwargs)


@patch("journal_utils.keep.datetime", FakeDate)
@patch("gkeepapi.Keep")
@patch("builtins.open", new_callable=mock_open)
@patch("journal_utils.keep.note._new")
def test_download(mock_new_note, mock_file_open, mock_keep):
    args = argparse.Namespace(overwrite=False)

    # Mocking Keep and datetime.today
    mock_keep_instance = mock_keep.return_value
    FakeDate.today = classmethod(lambda cls: datetime(2021, 1, 1))

    # Mocking the cfg dictionary
    cfg = {"keep": {"username": "test", "token": "test"}, "journal_path": "test"}

    # Mocking the journal label
    mock_label = Mock()
    mock_keep_instance.findLabel.return_value = mock_label

    # Mocking the journal entries
    mock_entry = Mock()
    mock_entry.title = "12/31"
    mock_entry.text = "Test entry"
    mock_entry.images = []
    mock_keep_instance.find.return_value = [mock_entry]

    # Call the function
    keep.download(args, cfg)

    # Assert that the functions were called with the correct arguments
    mock_keep_instance.findLabel.assert_called_once_with("journal")
    mock_keep_instance.find.assert_called_once_with(query="", labels=[mock_label])
    mock_new_note.assert_called_once()
    mock_file_open.assert_called_once_with(Path("test/2020/12/31.md"), "a")
    mock_file_open().write.assert_called_once_with("\nTest entry\n")


@patch("builtins.print")
@patch("gkeepapi.Keep")
def test_download_no_journal_label(mock_keep, mock_print):
    # Mocking the Keep object
    mock_keep_instance = mock_keep.return_value

    # Mocking the cfg dictionary
    cfg = {"keep": {"username": "test", "token": "test"}}

    # Mocking the journal label
    mock_keep_instance.findLabel.return_value = None

    # Call the function
    keep.download(None, cfg)

    # Assert that the error message was printed
    mock_print.assert_any_call("Error: no 'journal' label found in Google Keep.")
    mock_print.assert_any_call("Please create a 'journal' label in Google Keep.")
