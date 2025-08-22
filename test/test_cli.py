"""
Тесты для парсинга аргументов командной строки (logreport.cli).

Проверяются сценарии:
- Корректная обработка одного файла (test_single_file)
- Корректная обработка нескольких файлов (
    test_multiple_files_separate_flags,
    test_multiple_files_comma_with_space
)
- Передача даты и каталога логов (test_with_date_and_dir)
- Ошибки при некорректных или отсутствующих аргументах (
    test_invalid_argument_name,
    test_unknown_argument,
    test_missing_required_file,
    test_missing_required_report
)
"""

import os
import pytest
from logreport.cli import get_args


CWD = os.getcwd()


# Valid cases
def test_single_file(monkeypatch):
    monkeypatch.setattr(
        "sys.argv",
        [
            "prog",
            "--file", "example1.log",
            "--report", "average"
        ]
    )
    args = get_args()
    assert args.file == ["example1.log"]
    assert args.report == "average"
    assert args.date is None
    assert args.log_dir == CWD


def test_multiple_files_separate_flags(monkeypatch):
    monkeypatch.setattr(
        "sys.argv",
        [
            "prog",
            "--file", "a.log",
            "--file", "b.log",
            "--report", "average"
        ]
    )
    args = get_args()
    assert args.file == ["a.log", "b.log"]
    assert args.report == "average"


def test_multiple_files_comma_with_space(monkeypatch):
    monkeypatch.setattr(
        "sys.argv",
        [
            "prog",
            "--file", "a.log, b.log",
            "--report", "average"
        ]
    )
    args = get_args()
    assert args.file == ["a.log", "b.log"]


def test_with_date_and_dir(monkeypatch):
    monkeypatch.setattr(
        "sys.argv",
        [
            "prog",
            "--file", "a.log",
            "--report", "count",
            "--date", "2025-06-22",
            "--log_dir", "/tmp/logs"
        ]
    )
    args = get_args()
    assert args.file == ["a.log"]
    assert args.report == "count"
    assert args.date == "2025-06-22"
    assert args.log_dir == "/tmp/logs"


# Invalid cases
def test_invalid_argument_name(monkeypatch):
    monkeypatch.setattr(
        "sys.argv",
        [
            "prog",
            "--file", "a.log",
            "--repos", "average"
        ]
    )
    with pytest.raises(SystemExit):
        get_args()


def test_unknown_argument(monkeypatch):
    monkeypatch.setattr(
        "sys.argv",
        [
            "prog",
            "--file", "a.log",
            "--report", "average",
            "--unknown", "123"
        ]
    )
    with pytest.raises(SystemExit):
        get_args()


def test_missing_required_file(monkeypatch):
    monkeypatch.setattr(
        "sys.argv",
        [
            "prog",
            "--report", "average"
        ]
    )
    with pytest.raises(SystemExit):
        get_args()


def test_missing_required_report(monkeypatch):
    monkeypatch.setattr(
        "sys.argv",
        [
            "prog",
            "--file", "a.log"
        ]
    )
    with pytest.raises(SystemExit):
        get_args()
