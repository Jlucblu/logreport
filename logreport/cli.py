"""
Модуль для парсинга аргументов командной строки.

Функции:
- get_args: парсит и возвращает аргументы CLI.
"""

import argparse
import os


def get_args():
    parser = argparse.ArgumentParser(description="Log")
    parser.add_argument("--file", "-f",
                        action="append",
                        required=True,
                        help="Path(s) to log file(s)")
    parser.add_argument("--report", "-r",
                        required=True,
                        choices=["average", "count"],
                        help="Report type")
    parser.add_argument("--date", "-d",
                        help="Optional date filter (YYYY-MM-DD)")
    parser.add_argument("--log_dir", "-l",
                        default=os.getcwd(),
                        help="Directory containing log files")
    args = parser.parse_args()

    file_list = []
    for part in args.file:
        parts = [f.strip() for f in part.split(",") if f.strip()]
        file_list.extend(parts)
    args.file = file_list

    return args
