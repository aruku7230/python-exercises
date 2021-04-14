import os
import subprocess
import pytest
from search_big_files import _parse_size as parse_size
from search_big_files import _get_readable_size as get_readable_size
from search_big_files import search_big_files

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

def test_search_big_files(capsys):
    """Test search_big_files function"""
    # Test files structure:
    # test_files\
    # |--home\
    #    |--app\
    #       |--text_editor.out 2MB
    #       |--tree.out 3KB
    #    |--books\
    #       |--learn_emacs.out 1.2KB
    #       |--learn_javascript.out 1KB
    #       |--learn_python.out 2KB
    #    |--videos\
    #       |--famaily\
    #          |--happy_birthday.out 10MB
    #          |--happy_newyear.out 30MB
    #          |--weekend.out 12MB
    #    |--a.out 1B
    #    |--zero.out 0B
    #    |--link.out -> /tmp/not_existed_file_99999999
    #    |--readme.out 300B
    #    |--todo.out 200B
    # Create test folders and files.
    script_dir = os.path.dirname(os.path.realpath(__file__))
    os.chdir(script_dir)
    shell_script = './create_test_files.sh'
    process = subprocess.run([shell_script], check=True)
    if process.returncode != 0:
        assert False, 'Create test files failed.'

    def verify_test_result():
        expected_first_line = ('Searching files equal to or larger than '
                               + f'{file_size_info} in folder: "{test_files_root}" ...')
        expected_last_line = 'Search is done.'

        search_big_files(test_files_root, file_size)
        captured = capsys.readouterr().out
        captured_list = captured.splitlines()
        captured_first_line = captured_list[0]
        captured_last_line = captured_list[-1]
        captured_result_files = set(captured_list[1:-1])

        assert captured_first_line == expected_first_line
        assert captured_last_line == expected_last_line
        assert captured_result_files == expected_result_files

    test_files_root = 'test_files/home'

    # Test search_big_files(root, '1B')
    file_size = '1B'
    file_size_info = '1 byte (1 bytes)'
    expected_result_files = {
        '1 byte (1 bytes) test_files/home/a.out',
        '200 bytes (200 bytes) test_files/home/todo.out',
        '300 bytes (300 bytes) test_files/home/readme.out',
        '2.0 MB (2,097,152 bytes) test_files/home/app/text_editor.out',
        '3 KB (3,072 bytes) test_files/home/app/tree.out',
        '1 KB (1,024 bytes) test_files/home/books/learn_javascript.out',
        '1 KB (1,228 bytes) test_files/home/books/learn_emacs.out',
        '2 KB (2,048 bytes) test_files/home/books/learn_python.out',
        '30.0 MB (31,457,280 bytes) test_files/home/videos/family/happy_newyear.out',
        '10.0 MB (10,485,760 bytes) test_files/home/videos/family/happy_birthday.out',
        '12.0 MB (12,582,912 bytes) test_files/home/videos/family/weekend.out',
    }
    verify_test_result()

    # Test search_big_files(root, '500B')
    file_size = '500B'
    file_size_info = '500 bytes (500 bytes)'
    expected_result_files = {
        '3 KB (3,072 bytes) test_files/home/app/tree.out',
        '1 KB (1,024 bytes) test_files/home/books/learn_javascript.out',
        '1 KB (1,228 bytes) test_files/home/books/learn_emacs.out',
        '2 KB (2,048 bytes) test_files/home/books/learn_python.out',
        '2.0 MB (2,097,152 bytes) test_files/home/app/text_editor.out',
        '10.0 MB (10,485,760 bytes) test_files/home/videos/family/happy_birthday.out',
        '12.0 MB (12,582,912 bytes) test_files/home/videos/family/weekend.out',
        '30.0 MB (31,457,280 bytes) test_files/home/videos/family/happy_newyear.out',
    }
    verify_test_result()

    # Test search_big_files(root, '1KB')
    file_size = '1 kb'
    file_size_info = '1 KB (1,024 bytes)'
    expected_result_files = {
        '3 KB (3,072 bytes) test_files/home/app/tree.out',
        '2.0 MB (2,097,152 bytes) test_files/home/app/text_editor.out',
        '1 KB (1,024 bytes) test_files/home/books/learn_javascript.out',
        '1 KB (1,228 bytes) test_files/home/books/learn_emacs.out',
        '2 KB (2,048 bytes) test_files/home/books/learn_python.out',
        '30.0 MB (31,457,280 bytes) test_files/home/videos/family/happy_newyear.out',
        '10.0 MB (10,485,760 bytes) test_files/home/videos/family/happy_birthday.out',
        '12.0 MB (12,582,912 bytes) test_files/home/videos/family/weekend.out',
    }
    verify_test_result()

    # Test search_big_files(root, '1.2KB')
    file_size = '1.2KB'
    file_size_info = '1 KB (1,228 bytes)'
    expected_result_files = {
        '2.0 MB (2,097,152 bytes) test_files/home/app/text_editor.out',
        '3 KB (3,072 bytes) test_files/home/app/tree.out',
        '1 KB (1,228 bytes) test_files/home/books/learn_emacs.out',
        '2 KB (2,048 bytes) test_files/home/books/learn_python.out',
        '10.0 MB (10,485,760 bytes) test_files/home/videos/family/happy_birthday.out',
        '12.0 MB (12,582,912 bytes) test_files/home/videos/family/weekend.out',
        '30.0 MB (31,457,280 bytes) test_files/home/videos/family/happy_newyear.out',
    }
    verify_test_result()

    # Test search_big_files(root, '10MB')
    file_size = '10 MB'
    file_size_info = '10.0 MB (10,485,760 bytes)'
    expected_result_files = {
        '10.0 MB (10,485,760 bytes) test_files/home/videos/family/happy_birthday.out',
        '30.0 MB (31,457,280 bytes) test_files/home/videos/family/happy_newyear.out',
        '12.0 MB (12,582,912 bytes) test_files/home/videos/family/weekend.out',
    }
    verify_test_result()

    # Test search_big_files(root, '10')
    file_size = '10'
    file_size_info = '10.0 MB (10,485,760 bytes)'
    expected_result_files = {
        '10.0 MB (10,485,760 bytes) test_files/home/videos/family/happy_birthday.out',
        '30.0 MB (31,457,280 bytes) test_files/home/videos/family/happy_newyear.out',
        '12.0 MB (12,582,912 bytes) test_files/home/videos/family/weekend.out',
    }
    verify_test_result()

    # Delete test files if succeeded.
    process = subprocess.run(['rm', '-rf', 'test_files'], check=True)
    if process.returncode != 0:
        assert False, 'Clear test files failed.'
