import re
import sys
from typing import Counter


def main():
    if len(sys.argv) <= 1:
        print("Usage: python app.py <path-to-log> [level]")
        return
   
    get_logs_info(sys.argv[1:])


def get_logs_info(args):
    path = args[0] if len(args) > 0 else None
    level = args[1] if len(args) > 1 else None

    if not path:
        print("Log file path not specified.")
        return
    
    logs = load_logs(path)
    
    if logs is None:
        print("We couldn't find your file")
        return

    if not logs:
        print("Your file is empty or data format is not correct")
        return
    
    counts = count_logs_by_level(logs)
    if counts:
        display_log_counts(counts)

    if level:
        filtered = filter_logs_by_level(logs, level)
        display_logs_details(filtered, level)

     
def load_logs(file_path: str) -> list:
    try:
        with open(file_path, "r", encoding="utf-8") as fh:
            lines = [el.strip() for el in fh.readlines()]
            parsed = [parse_log_line(line) for line in lines]
            return [p for p in parsed if p]
    except FileNotFoundError:
       return


def parse_log_line(line: str) -> dict:
    log_pattern = re.compile(
        r"^(\d{4}-\d{2}-\d{2})\s+"
        r"(\d{2}:\d{2}:\d{2})\s+"
        r"(?:(INFO|DEBUG|ERROR|WARNING|CRITICAL)\s+)?"
        r"(.*)$"
    )

    match = log_pattern.match(line.strip())
    if not match:
        return {}

    # parts = line.split(maxsplit=3)
    # if len(parts) < 4:
    #     return {}
    
    return {
        "date": match.group(1),
        "time": match.group(2),
        "level": match.group(3),
        "message": match.group(4).strip()
    }


def count_logs_by_level(logs: list) -> dict:
    levels = [log.get("level").upper() for log in logs if log.get("level")]

    result = dict(Counter(levels))
    return result    


def filter_logs_by_level(logs: list, level: str) -> list:
    level = level.lower()
    # filtered = [log for log in logs if (log.get("level") or "").lower() == level]
    filtered =list(filter(lambda log: (log.get("level") or "").lower() == level, logs))
    return filtered


def display_log_counts(counts: dict):
    level_title = "Рівень логування"
    count_title = "Кількість"
    print(f"{level_title} | {count_title}")
    print(f"{len(level_title) * "-"} | {len(count_title) * "-"}")
    for level, count in counts.items():
        print(f"{level}{(len(level_title) - len(level)) * " "} | {count}")   


def display_logs_details(logs: dict, level: str):
    print(f"\nДеталі логів для рівня {level.upper()}:")
    if not logs:
        print("— нічого не знайдено —")
        return
    
    for log in logs:
        print(f"{log.get('date')} {log.get('time')} - {log.get('message')}")


if __name__ == "__main__":
    main()
