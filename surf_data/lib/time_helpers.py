from datetime import datetime
from zoneinfo import ZoneInfo
import re

ALEXA_TIME_ZONE_MAPPING = {"PT": "America/Los_Angeles"}

RELATIVE_TIME_REGEX = r"^(?P<tz>[^-]+)-(?P<diff>[^-]+)$"
TIME_DIFF_REGEX = r"(\d)+(?P<unit>\D+)"
UTC_TIME_ZONE = ZoneInfo("UTC")
PST_TIME_ZONE = ZoneInfo("America/Los_Angeles")


def get_current_time(timezone: str = None) -> datetime:
    if timezone is not None:
        tz = ZoneInfo(timezone)
    else:
        tz = PST_TIME_ZONE
    return datetime.now(tz)


def parse_absolute_time(time_string: str) -> datetime:
    """
    Alexa might pass something like '06:33' for the entry time.
    """
    parsed_hour = datetime.strptime(time_string, "%H:%M")
    current_time = get_current_time()
    return current_time.replace(hour=parsed_hour.hour, minute=parsed_hour.minute)


def parse_relative_time(tz: str, diff: str) -> datetime:
    """
    We got something like ('PT', '3H'), so parse that as
    now(tz=pacific time) - timedelta(hours=3)
    """
    raise NotImplementedError("The app doesn't support relative times yet!")


def map_time_to_datetime(date_val: str) -> datetime:
    """
    Parses the time string returned by the alexa skills kit.
    Depending on the user input, we might get an absolute time or a relative time:
        relative: "PT-3H"
        absolute: "05:00"
    All times are assumed to be in the time zone of the entry.
    """
    matches = re.match(RELATIVE_TIME_REGEX, date_val)
    if matches is not None:
        return parse_relative_time(
            matches.groupdict()["tz"], matches.groupdict()["diff"]
        )
    return parse_absolute_time(date_val)
