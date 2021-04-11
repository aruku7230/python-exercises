import pytest
from search_big_files import _parse_size as parse_size
from search_big_files import _get_readable_size as get_readable_size

def test_parse_size():
    """Test _parse_size function"""
    # normal cases
    assert parse_size(1) == 1*1024*1024
    assert parse_size(100000) == 100000*1024*1024
    assert parse_size(100.2) == int(100.2*1024*1024)
    assert parse_size(100.7) == int(100.7*1024*1024)
    assert parse_size('1B') == 1
    assert parse_size('200 B') == 200
    assert parse_size('20 b') == 20
    assert parse_size('1KB') == 1024
    assert parse_size('1.2 KB') == int(1.2 * 1024)
    assert parse_size('1.2    kb') == int(1.2 * 1024)
    assert parse_size('5MB') == 5* 1024 * 1024
    assert parse_size('1.5 MB') == int(1.5 * 1024 * 1024)
    assert parse_size('1.5 mb') == int(1.5 * 1024 * 1024)
    assert parse_size('1 GB') == 1 * 1024 * 1024 * 1024
    assert parse_size('2.5 GB') == int(2.5 * 1024 * 1024 * 1024)
    assert parse_size('2.5 gb') == int(2.5 * 1024 * 1024 * 1024)

    # error cases
    with pytest.raises(ValueError):
        not_a_string = [1234]
        parse_size(not_a_string)

    with pytest.raises(ValueError):
        parse_size('1Byte')

    with pytest.raises(ValueError):
        parse_size('1KByte')

    with pytest.raises(ValueError):
        parse_size('2PB')

    # rare cases
    # large integer (16 digits)
    assert parse_size(1234567890123456) == 1234567890123456*1024*1024

    # very large integer (30 digits)
    # one limitation of `parse_size` is that the parsed result of very large
    # integer could not be precise as it convert it to float at first.
    assert parse_size(123456789012345678901234567890) != 123456789012345678901234567890*1024*1024

    # infinite float
    with pytest.raises(ValueError):
        # 1.5e1000 should be treated as 'inf', and could not be parsed.
        parse_size(1.5e1000)

def test_get_readable_size():
    """Test _get_readable_size function"""
    one_kb = 1024
    one_mb = one_kb * 1024
    one_gb = one_mb * 1024
    assert get_readable_size(1) == '1 byte'
    assert get_readable_size(50) == '50 bytes'
    assert get_readable_size(999) == '999 bytes'
    assert get_readable_size(1000) == '1 KB'
    assert get_readable_size(one_kb) == '1 KB'
    assert get_readable_size(one_kb * 70) == '70 KB'
    assert get_readable_size(one_kb * 70 + 510) == '70 KB'
    assert get_readable_size(one_kb * 70 + 512) == '70 KB'
    assert get_readable_size(one_kb * 70 + 513) == '71 KB'
    assert get_readable_size(one_kb * 910) == '910 KB'
    assert get_readable_size(one_kb * 1000) == '1.0 MB'
    assert get_readable_size(one_mb * 6) == '6.0 MB'
    assert get_readable_size(one_mb * 10 + 104857) == '10.1 MB'
    assert get_readable_size(one_mb * 500 + 576716) == '500.5 MB'
    assert get_readable_size(one_mb * 500 + 576717) == '500.6 MB'
    assert get_readable_size(one_mb * 1000) == '0.98 GB'
    assert get_readable_size(one_gb) == '1.00 GB'
    assert get_readable_size(one_gb * 3 + 241591910) == '3.22 GB'
    assert get_readable_size(one_gb * 3 + 241591911) == '3.23 GB'
    assert get_readable_size(one_gb * 1000) == '1000.00 GB'
    assert get_readable_size(one_gb * 1024) == '1024.00 GB'
    assert get_readable_size(one_gb * 2048) == '2048.00 GB'
