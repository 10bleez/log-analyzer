from collections import Counter

class Aggregator:
    def __init__(self):
        self.total_lines = 0
        self.malformed_lines = 0
        self.filtered_events = 0
        self.level_counts = Counter()
        self.source_counts = Counter()
        self.error_codes = Counter()

    def process_line(self, entry, matched):
        """Обновляет статистику на основе одной строки."""
        if entry is None:
            self.malformed_lines += 1
            return

        self.total_lines += 1
        
        if matched:
            self.filtered_events += 1
            self.level_counts[entry.level] += 1
            self.source_counts[entry.source] += 1
            if entry.level == "ERROR":
                self.error_codes[entry.event_code] += 1

    def get_top_errors(self, n=5):
        """Возвращает Top-N кодов ошибок."""
        return self.error_codes.most_common(n)
