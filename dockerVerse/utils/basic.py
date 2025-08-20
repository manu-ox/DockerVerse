from datetime import datetime
from zoneinfo import ZoneInfo
from datetime import datetime
from time import strftime, gmtime



IST_ZONE = ZoneInfo("Asia/Kolkata")

def convert_to_IST(dt: datetime):
    return dt.astimezone(IST_ZONE)


def format_time(time: datetime):
    return time.strftime("%Y-%m-%d %H:%M:%S")


def get_duration_from_seconds(seconds: int):
    return strftime('%H:%M:%S', gmtime(seconds))


def get_status_tag(is_running: bool) -> str:
    return '●' if is_running else '○'


def bold_text(text):
    """Return bold text in Markdown"""
    return f"**{text}**"

