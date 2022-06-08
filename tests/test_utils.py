from datetime import datetime

from atlaspyapi.entity_source_generation.utile import current_milli_time


def test_utils():
    actual_ts = current_milli_time()
    expected_ts = int(datetime.now().timestamp())*1000
    margin = 5000

    print(actual_ts)
    print(expected_ts)
    assert actual_ts <= expected_ts + margin
    assert actual_ts >= expected_ts - margin
