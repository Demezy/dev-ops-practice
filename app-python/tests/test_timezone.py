import pytest
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo
from src.timezone import getMskTime, TIME_ZONE


def test_getMskTime_format():
    time = getMskTime()
    # Verify the format matches YYYY-MM-DD HH:MM:SS
    assert len(time) == 19
    datetime.strptime(time, "%Y-%m-%d %H:%M:%S")  # Should not raise exception


def test_getMskTime_timezone():
    # Get current time in UTC and MSK
    utc_now = datetime.now(timezone.utc)
    msk_time = datetime.strptime(getMskTime(), "%Y-%m-%d %H:%M:%S")
    msk_time = msk_time.replace(tzinfo=ZoneInfo(TIME_ZONE))

    # Convert UTC to MSK for comparison
    utc_in_msk = utc_now.astimezone(ZoneInfo(TIME_ZONE))

    # Times should be within 1 second of each other
    assert abs(msk_time.timestamp() - utc_in_msk.timestamp()) < 1


def test_getMskTime_consistency():
    # Test that multiple calls within a short time return similar times
    time1 = getMskTime()
    time2 = getMskTime()

    dt1 = datetime.strptime(time1, "%Y-%m-%d %H:%M:%S")
    dt2 = datetime.strptime(time2, "%Y-%m-%d %H:%M:%S")

    # Times should be within 3 seconds of each other
    assert abs((dt2 - dt1).total_seconds()) < 3


@pytest.mark.parametrize(
    "test_timezone", ["Europe/Moscow", "Asia/Dubai", "UTC", "America/New_York"]
)
def test_getMskTime_different_system_timezones(monkeypatch, test_timezone):
    # Test that getMskTime returns correct MSK time regardless of system timezone
    monkeypatch.setenv("TZ", test_timezone)
    time = getMskTime()

    # Verify it's in correct format
    dt = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")

    # Verify the time is reasonable (not in the far future or past)
    now = datetime.now()
    assert abs((dt - now).total_seconds()) < 24 * 3600  # Within 24 hours


def test_getMskTime_mock_specific_time(monkeypatch):
    class MockDateTime:
        @classmethod
        def now(cls, tz=None):
            return datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

    monkeypatch.setattr("datetime.datetime", MockDateTime)

    time = getMskTime()
    assert time == "2024-01-01 15:00:00"  # MSK is UTC+3


@pytest.mark.parametrize(
    "mock_time,expected",
    [
        ((2024, 1, 1, 0, 0, 0), "2024-01-01 03:00:00"),
        ((2024, 6, 1, 0, 0, 0), "2024-06-01 03:00:00"),
        ((2024, 12, 31, 23, 59, 59), "2025-01-01 02:59:59"),
    ],
)
def test_getMskTime_edge_cases(monkeypatch, mock_time, expected):
    class MockDateTime:
        @classmethod
        def now(cls, tz=None):
            return datetime(*mock_time, tzinfo=timezone.utc)

    monkeypatch.setattr("datetime.datetime", MockDateTime)

    time = getMskTime()
    assert time == expected
