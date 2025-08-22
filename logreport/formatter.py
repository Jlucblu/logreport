"""
Модуль для форматирования отчёта для вывода в консоль.

Функции:
- format_report: форматирует данные отчёта в таблицу.
"""

from tabulate import tabulate


def format_report(report_data: list[dict]):
    if not report_data:
        return "No data for report."

    headers = report_data[0].keys()
    rows = [item.values() for item in report_data]
    return tabulate(rows, headers=headers, tablefmt="tablegrid")
