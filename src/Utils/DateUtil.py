from datetime import datetime, timedelta


def get_week_from_date(date_str):
    return datetime.strptime(date_str, "%d.%m.%Y").isocalendar()[1]

def get_relative_week(start_week, current_week):
    return current_week - start_week + 1

def get_week_range(start_date, week_offset):
    start = datetime.strptime(start_date, "%d.%m.%Y")
    days_to_monday = (start.weekday() - 0) % 7
    start_of_week = start - timedelta(days=days_to_monday) + timedelta(weeks=week_offset)
    end_of_week = start_of_week + timedelta(days=(4 - start_of_week.weekday()) % 7)
    return start_of_week.strftime("%d.%m.%Y"), end_of_week.strftime("%d.%m.%Y")