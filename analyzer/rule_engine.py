import re

def check_by_rules(log_line: str) -> bool:
    if re.search(r'\b(ERROR|FATAL)\b', log_line, re.IGNORECASE):
        return True
    if re.search(r'\b5\d{2}\b', log_line):
        return True
    if re.search(r'\b(timeout|connection refused|exception)\b', log_line, re.IGNORECASE):
        return True

    return False