"""
Модуль для генерации отчётов по логам.

Содержит функции:
- aggregate_logs: агрегирует статистику по URL.
- generate_average_report: формирует отчёт со средним временем ответа.
- generate_count_report: формирует отчёт с количеством запросов.
"""

from collections import defaultdict


def aggregate_logs(logs: list[dict], date: str | None = None):
    stats = defaultdict(lambda: {"count": 0, "total_time": 0})
    for entry in logs:
        if date and not entry.get("@timestamp", "").startswith(date):
            continue

        url = entry.get("url")
        response_time = entry.get("response_time", 0)

        if url is None or response_time is None:
            continue

        stats[url]["count"] += 1
        stats[url]["total_time"] += response_time

    return stats


def generate_average_report(logs: list[dict], date: str | None = None):
    stats = aggregate_logs(logs, date)
    result = []
    for url, data in stats.items():
        avg_time = data["total_time"] / data["count"] if data["count"] else 0
        result.append({
            "url": url,
            "count": data["count"],
            "avg_time": avg_time
        })
    return result


def generate_count_report(logs: list[dict], date: str | None = None):
    stats = aggregate_logs(logs, date)
    result = [
        {"url": url, "count": data["count"]}
        for url, data in stats.items()
    ]
    return result
