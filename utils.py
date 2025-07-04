from dateparser.search import search_dates
from datetime import datetime, timezone
import pytz

def parse_time_from_text(text):
    parsed = search_dates(
        text,
        settings={
            "PREFER_DATES_FROM": "future",
            "TIMEZONE": "Asia/Kolkata",
            "RETURN_AS_TIMEZONE_AWARE": True
        }
    )
    if parsed:
        return parsed[0][1].astimezone(timezone.utc).replace(second=0, microsecond=0)
    return None

def find_closest_slot(target_time, slots, threshold_seconds=900):
    """
    target_time: datetime in UTC
    slots: list of dicts with 'iso' keys (UTC time in ISO format)
    Returns the closest slot within threshold or None
    """
    closest = None
    min_diff = float("inf")

    for slot in slots:
        slot_time = datetime.fromisoformat(slot["iso"]).replace(tzinfo=timezone.utc)
        diff = abs((slot_time - target_time).total_seconds())
        if diff < min_diff:
            min_diff = diff
            closest = slot

    return closest if min_diff <= threshold_seconds else None
