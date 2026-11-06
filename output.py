import json
import csv
import sys

def print_summary(aggregator, top_n):
    """Выводит сводку в консоль."""
    print("=" * 40)
    print("СВОДКА ПО ЖУРНАЛУ")
    print("=" * 40)
    print(f"Всего корректных строк: {aggregator.total_lines}")
    print(f"Поврежденных строк: {aggregator.malformed_lines}")
    print(f"Событий после фильтрации: {aggregator.filtered_events}")
    print("-" * 40)
    print("По уровням:")
    for level, count in aggregator.level_counts.items():
        print(f"  {level}: {count}")
    print("По источникам:")
    for source, count in aggregator.source_counts.items():
        print(f"  {source}: {count}")
    print(f"Top-{top_n} кодов ошибок:")
    for code, count in aggregator.get_top_errors(top_n):
        print(f"  {code}: {count}")
    print("=" * 40)

def save_to_json(aggregator, top_n, filepath):
    """Сохраняет сводку в JSON."""
    data = {
        "total_lines": aggregator.total_lines,
        "malformed_lines": aggregator.malformed_lines,
        "filtered_events": aggregator.filtered_events,
        "level_counts": dict(aggregator.level_counts),
        "source_counts": dict(aggregator.source_counts),
        "top_errors": dict(aggregator.get_top_errors(top_n))
    }
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Сводка сохранена в JSON: {filepath}")

def save_to_csv(aggregator, top_n, filepath):
    """Сохраняет сводку в CSV."""
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Метрика", "Значение"])
        writer.writerow(["Всего корректных строк", aggregator.total_lines])
        writer.writerow(["Поврежденных строк", aggregator.malformed_lines])
        writer.writerow(["Событий после фильтрации", aggregator.filtered_events])
        for level, count in aggregator.level_counts.items():
            writer.writerow([f"Уровень {level}", count])
        for source, count in aggregator.source_counts.items():
            writer.writerow([f"Источник {source}", count])
        for code, count in aggregator.get_top_errors(top_n):
            writer.writerow([f"Код ошибки {code}", count])
    print(f"Сводка сохранена в CSV: {filepath}")
