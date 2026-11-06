import datetime

class LogEntry:
    def __init__(self, timestamp, level, source, event_code, message):
        self.timestamp = timestamp
        self.level = level
        self.source = source
        self.event_code = event_code
        self.message = message

def parse_line(line, line_number):
    """Парсит одну строку. Возвращает (LogEntry, None) или (None, error_msg)."""
    line = line.strip()
    if not line:
        return None, f"Строка {line_number}: пустая строка"

    parts = line.split('|')
    if len(parts) != 5:
        return None, f"Строка {line_number}: неверное количество полей (ожидалось 5, получено {len(parts)})"

    timestamp_str, level, source, event_code, message = [p.strip() for p in parts]

    # Валидация уровня
    if level not in ["TRACE", "DEBUG", "INFO", "WARN", "ERROR"]:
        return None, f"Строка {line_number}: неверный уровень '{level}'"

    # Валидация даты (ISO 8601 UTC)
    try:
        # Заменяем Z на +00:00 для корректного парсинга в Python
        ts_str = timestamp_str.replace('Z', '+00:00')
        timestamp = datetime.datetime.fromisoformat(ts_str)
    except ValueError:
        return None, f"Строка {line_number}: неверный формат даты '{timestamp_str}'"

    return LogEntry(timestamp, level, source, event_code, message), None

def read_log_file(filepath):
    """Генератор, который читает файл построчно (без загрузки в память)."""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, start=1):
                yield line, line_num
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл не найден: {filepath}")
