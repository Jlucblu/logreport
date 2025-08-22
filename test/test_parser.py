"""
Тесты для парсера лог-файлов (logreport.parser).

Проверяются сценарии:
- Некорректный каталог логов (test_invalid_directory)
- Чтение одного файла (test_single_file)
- Чтение нескольких файлов (test_multiple_files)
- Не существующий файл (test_nonexistent_file)
- Пустой файл (test_empty_file)
- Некорректный JSON в файле (test_broken_json)
- Корректный лог в построчном формате (test_valid_log_line_by_line)
- Корректный лог в формате JSON массива (test_valid_json_array)
- Логи в разных форматах (test_logs_in_different_formats)
"""

import os
import pytest
import json
from logreport.parser import parse_logs, parse_log

DATA_DIR = os.path.join(os.path.dirname(__file__), "examples")


def test_invalid_directory():
    logs = parse_logs([], log_dir="/invalid/path/to/logs")
    assert logs == []


def test_single_file():
    file_path = os.path.join(DATA_DIR, "example1.log")
    logs = parse_log(file_path)
    assert isinstance(logs, list)
    assert len(logs) > 0


def test_multiple_files():
    file1 = os.path.join(DATA_DIR, "example1.log")
    file2 = os.path.join(DATA_DIR, "example2.log")
    logs = parse_logs([file1, file2], log_dir=None)
    assert isinstance(logs, list)
    assert len(logs) > 0


def test_nonexistent_file():
    file_path = os.path.join(DATA_DIR, "no_such_file.log")
    logs = parse_log(file_path)
    assert logs == []


def test_empty_file():
    file_path = os.path.join(DATA_DIR, "empty.log")
    logs = parse_log(file_path)
    assert logs == []


def test_broken_json():
    file_path = os.path.join(DATA_DIR, "test1.txt")
    with pytest.raises(json.JSONDecodeError):
        parse_logs([file_path], log_dir=None)


def test_valid_log_line_by_line():
    """Старый формат: построчный JSON"""
    file_path = os.path.join(DATA_DIR, "example1.log")
    logs = parse_logs([file_path], log_dir=None)
    assert all(
        all(k in log for k in ("url", "status", "response_time"))
        for log in logs
    )


def test_valid_json_array():
    file_path = os.path.join(DATA_DIR, "test2.json")
    logs = parse_logs([file_path], log_dir=None)
    assert all(
        all(k in log for k in ("url", "status", "response_time"))
        for log in logs
    )


def test_logs_in_different_format():
    file1 = os.path.join(DATA_DIR, "example1.log")
    file2 = os.path.join(DATA_DIR, "test2.json")
    logs = parse_logs([file1, file2], log_dir=None)
    logs1 = parse_logs([file1], log_dir=None)
    logs2 = parse_logs([file2], log_dir=None)
    assert len(logs) == len(logs1) + len(logs2)
