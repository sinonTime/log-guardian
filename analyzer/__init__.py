from .rule_engine import check_by_rules
from .anomaly_detector import SlidingWindowZScore

class Analyzer:
    def __init__(self):
        self.error_count_detector = SlidingWindowZScore(window_size=10, threshold=3)
        self.minute_error_count = 0
        self.last_minute = None

    def analyze(self, log_line: str) -> dict:
        if check_by_rules(log_line):
            return {"alert": True, "engine": "rule", "line": log_line}
        return {"alert": False, "engine": None, "line": log_line}