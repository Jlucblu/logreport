"""
Точка входа для генерации отчёта по логам.
Использование:
    python main.py --file log1.txt --report average --date 2025-06-22 --log_dir ./logs
    py main.py -f "log1.json, log2.txt" -r average -d 2025-06-22 -l ./logs
    py main.py -f log1.json -f log2.txt -r average -d 2025-06-22 -l ./logs

Аргументы:
    --file/-f     Список лог-файлов, формат json (через запятую или несколько флагов)
    --report/-r   Тип отчёта: average или count
    --date/-d     Фильтр по дате (формат YYYY-MM-DD)
    --log_dir/-l  Каталог с логами (по умолчанию — текущий)
"""

from logreport.cli import get_args
from logreport.parser import parse_logs
from logreport.reports import generate_average_report, generate_count_report
from logreport.formatter import format_report


def main():
    args = get_args()
    logs = parse_logs(args.file, log_dir=args.log_dir)

    if args.report == "average":
        report_data: list = generate_average_report(logs, date=args.date)
    elif args.report == "count":
        report_data: list = generate_count_report(logs, date=args.date)
    else:
        raise ValueError(f"Unknown report: {args.report}")

    print(format_report(report_data))


if __name__ == "__main__":
    main()
