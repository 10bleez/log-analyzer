import argparse
import datetime
import sys
from parser import read_log_file, parse_line
from filters import LogFilter
from aggregator import Aggregator
from output import print_summary, save_to_json, save_to_csv

def parse_date(date_str):
    if not date_str:
        return None
    try:
        return datetime.datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    except ValueError:
        raise argparse.ArgumentTypeError(f"Неверный формат даты: {date_str}")

def main():
    parser = argparse.ArgumentParser(description="CLI-анализатор журналов событий")
    parser.add_argument("--input", required=True, help="Путь к файлу журнала")
    parser.add_argument("--from", dest="from_ts", type=parse_date, help="Начало интервала (ISO 8601)")
    parser.add_argument("--to", dest="to_ts", type=parse_date, help="Конец интервала (ISO 8601, не включая)")
    parser.add_argument("--level", choices=["TRACE", "DEBUG", "INFO", "WARN", "ERROR"], help="Фильтр по уровню")
    parser.add_argument("--source", help="Фильтр по источнику")
    parser.add_argument("--top", type=int, default=5, help="Количество топ-ошибок (по умолчанию 5)")
    parser.add_argument("--format", choices=["json", "csv"], help="Формат сохранения")
    parser.add_argument("--output", help="Путь для сохранения файла")

    args = parser.parse_args()

    log_filter = LogFilter(args.from_ts, args.to_ts, args.level, args.source)
    aggregator = Aggregator()

    try:
        for line, line_num in read_log_file(args.input):
            entry, error = parse_line(line, line_num)
            if error:
                print(error, file=sys.stderr)
                aggregator.process_line(None, False)
                continue
            
            matched = log_filter.matches(entry)
            aggregator.process_line(entry, matched)

        print_summary(aggregator, args.top)

        if args.format and args.output:
            if args.format == "json":
                save_to_json(aggregator, args.top, args.output)
            elif args.format == "csv":
                save_to_csv(aggregator, args.top, args.output)

    except FileNotFoundError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
