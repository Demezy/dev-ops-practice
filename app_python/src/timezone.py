import datetime
from zoneinfo import ZoneInfo

TIME_ZONE = "Europe/Moscow"


def getMskTime():
    # Get UTC time first, then convert to Moscow time
    utc_time = datetime.datetime.now(datetime.timezone.utc)
    msk_time = utc_time.astimezone(ZoneInfo(TIME_ZONE))
    return msk_time.strftime("%Y-%m-%d %H:%M:%S")


if __name__ == "__main__":

    class DatetimeMock(datetime.datetime):
        @classmethod
        def now(cls, tz=None):
            return cls(2077, 1, 1, 12, 0, 0)

    datetime.datetime = DatetimeMock

    print(getMskTime())
