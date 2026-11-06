import pytest
import datetime
from parser import parse_line, read_log_file, LogEntry
from filters import LogFilter
from aggregator import Aggregator
from output import save_to_json, save_to_csv, print_summary

# --- Тесты парсера ---
def test_parse_valid_line():
    line = "2023-10-25T10:00:00Z | INFO | Server1 | 100 | Started"
    entry, err = parse_line(line, 1)
    assert err is None
    assert entry.level == "INFO"
    assert entry.source == "Server1"

def test_parse_malformed_line():
    line = "Битая строка"
    entry, err = parse_line(line, 3)
    assert entry is None
    assert "неверное количество полей" in err

def test_parse_invalid_date():
    line = "2023-13-45T10:00:00Z | INFO | Server1 | 100 | Started"
    entry, err = parse_line(line, 1)
    assert entry is None
    assert "неверный формат даты" in err

def test_parse_invalid_level():
    line = "2023-10-25T10:00:00Z | UNKNOWN | Server1 | 100 | Started"
    entry, err = parse_line(line, 1)
    assert entry is None
    assert "неверный уровень" in err

# --- Тесты фильтров ---
@pytest.fixture
def sample_entry():
    ts = datetime.datetime.fromisoformat("2023-10-25T10:00:00+00:00")
    return LogEntry(ts, "ERROR", "Server1", "500", "Crash")

def test_filter_by_level(sample_entry):
    assert LogFilter(level="ERROR").matches(sample_entry) is True
    assert LogFilter(level="INFO").matches(sample_entry) is False

def test_filter_by_source(sample_entry):
    assert LogFilter(source="Server1").matches(sample_entry) is True
    assert LogFilter(source="Server2").matches(sample_entry) is False

def test_filter_by_date_bounds(sample_entry):
    f1 = LogFilter(from_ts=datetime.datetime.fromisoformat("2023-10-25T10:00:00+00:00"))
    assert f1.matches(sample_entry) is True
    f2 = LogFilter(to_ts=datetime.datetime.fromisoformat("2023-10-25T10:00:00+00:00"))
    assert f2.matches(sample_entry) is False

# --- Тесты агрегатора ---
def test_aggregator_counts(sample_entry):
    agg = Aggregator()
    agg.process_line(sample_entry, True)
    agg.process_line(None, False)
    assert agg.total_lines == 1
    assert agg.malformed_lines == 1
    assert agg.filtered_events == 1
    assert agg.get_top_errors(1)[0] == ("500", 1)

# --- Тесты вывода ---
def test_print_summary(capsys, sample_entry):
    agg = Aggregator()
    agg.process_line(sample_entry, True)
    print_summary(agg, 5)
    captured = capsys.readouterr()
    assert "СВОДКА ПО ЖУРНАЛУ" in captured.out
    assert "ERROR: 1" in captured.out

def test_output_json_csv(sample_entry, tmp_path):
    agg = Aggregator()
    agg.process_line(sample_entry, True)
    json_path = tmp_path / "out.json"
    save_to_json(agg, 5, str(json_path))
    assert json_path.exists()
    csv_path = tmp_path / "out.csv"
    save_to_csv(agg, 5, str(csv_path))
    assert csv_path.exists()

# --- Тесты файлов ---
def test_missing_file():
    with pytest.raises(FileNotFoundError):
        list(read_log_file("no_such_file.log"))

def test_empty_file(tmp_path):
    empty_file = tmp_path / "empty.log"
    empty_file.write_text("")
    assert list(read_log_file(str(empty_file))) == []
