"""
Тесты для генерации отчётов (logreport.reports).

Проверяются сценарии:
- Агрегация логов (test_aggregate_logs)
- Генерация отчёта со средним временем ответа (test_generate_average_report)
- Пустые входные данные (test_reports_with_empty_logs)
"""

import os
import pytest
from logreport.reports import (
    aggregate_logs,
    generate_average_report,
    generate_count_report
)
from logreport.parser import parse_log


DATA_DIR = os.path.join(os.path.dirname(__file__), "examples")
FILE_PATH = os.path.join(DATA_DIR, "test2.json")


def test_aggregate_logs():
    logs = parse_log(FILE_PATH)
    stats = aggregate_logs(logs)
    total_context_count = 3
    total_hw_count = 7
    assert stats["/api/context/..."]["count"] == total_context_count
    assert stats["/api/homeworks/..."]["count"] == total_hw_count

    total_context_time = 0.024 + 0.02 + 0.024
    total_hw_time = 0.06 + 0.032 + 0.06 + 0.06 + 0.06 + 0.064 + 0.1
    assert stats["/api/context/..."]["total_time"] == pytest.approx(
        total_context_time
    )
    assert stats["/api/homeworks/..."]["total_time"] == pytest.approx(
        total_hw_time
    )


def test_generate_average_report():
    logs = parse_log(FILE_PATH)
    report = generate_average_report(logs)
    for r in report:
        if r["url"] == "/api/context/...":
            avr_context = (0.024 + 0.02 + 0.024)/3
            assert r["avg_time"] == pytest.approx(avr_context)
        if r["url"] == "/api/homeworks/...":
            avg_hw = (0.06 + 0.032 + 0.06 + 0.06 + 0.06 + 0.064 + 0.1)/7
            assert r["avg_time"] == pytest.approx(avg_hw)


def test_generate_average_report_with_date():
    logs = parse_log(FILE_PATH)
    date = "2025-06-22"
    report = generate_average_report(logs, date=date)
    assert len(report) == 2
    for r in report:
        if r["url"] == "/api/context/...":
            count_context = 3
            assert r["count"] == count_context
            avr_context = (0.024 + 0.02 + 0.024)/3
            assert r["avg_time"] == pytest.approx(avr_context)
        if r["url"] == "/api/homeworks/...":
            count_hw = 2
            assert r["count"] == count_hw
            avg_hw = (0.06 + 0.032)/2
            assert r["avg_time"] == pytest.approx(avg_hw)


def test_reports_with_empty_logs():
    assert aggregate_logs([]) == {}
    assert generate_average_report([]) == []
    assert generate_count_report([]) == []
