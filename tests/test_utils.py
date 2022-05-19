from datetime import datetime

from atlas_client.entity_source_generation.utile import current_milli_time


def test_utils():
    actual_ts = current_milli_time()
    expected_ts = int(datetime.now().timestamp())
    margin = 5
    assert actual_ts <= expected_ts + margin
    assert actual_ts >= expected_ts - margin
