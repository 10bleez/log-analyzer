import datetime

class LogFilter:
    def __init__(self, from_ts=None, to_ts=None, level=None, source=None):
        self.from_ts = from_ts
        self.to_ts = to_ts
        self.level = level
        self.source = source

    def matches(self, entry):
        """Проверяет, удовлетворяет ли событие всем фильтрам."""
        if self.from_ts and entry.timestamp < self.from_ts:
            return False
        if self.to_ts and entry.timestamp >= self.to_ts: # Конец исключительно!
            return False
        if self.level and entry.level != self.level:
            return False
        if self.source and entry.source != self.source:
            return False
        return True
