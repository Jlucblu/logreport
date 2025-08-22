"""
Модуль для чтения и парсинга лог-файлов.

Функции:
- parse_log: читает и парсит один лог-файл.
- parse_logs: читает и парсит список лог-файлов.
"""

import json
import os


def parse_log(file_path: str):
    if not os.path.isfile(file_path):
        print(f"Warning: Log file not found: {file_path}")
        return []
    with open(file_path, "r", encoding="utf-8") as f:
        first_char = f.read(1)
        f.seek(0)
        if first_char == "[":
            return json.load(f)
        else:
            return [json.loads(line) for line in f]


def parse_logs(file_paths: list[str], log_dir: str | None = None):
    if log_dir and not os.path.isdir(log_dir):
        print(f"Warning: Log directory not found: {log_dir}")
        return []
    logs = []
    for path in file_paths:
        full_path = os.path.join(log_dir, path) if log_dir else path
        logs.extend(parse_log(full_path))
    return logs
