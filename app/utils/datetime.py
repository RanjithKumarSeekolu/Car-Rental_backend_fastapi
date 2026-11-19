from datetime import datetime, timezone


def to_iso(value):
    if isinstance(value, datetime):
        utc = value.astimezone(timezone.utc)
        return utc.isoformat(timespec="milliseconds").replace("+00:00", "Z")
    return value