#! /usr/bin/env python

""" Search a folder recursively for files equal or greater than a specified size"""

import os
import errno
import re

def _parse_size(size):
    """
    The formats is `<number><unit>`.
    - `<number>` could be an integer or float.
    - Supported `<unit>` are `B` for bytes, `KB` for KiloBytes, `MB` for
        MegaBytes (default), and `GB` for GegaBytes. `<unit>` may be ommited, then
        the default unit (`MB`) will be used.
    - There could be whitespace charater between `<number>` and `<unit>`.

    One limitation of `parse_size` is that the parsed result of very large
    integer could not be precise as it convert it to float at first.
    """

    size = str(size)
    match = re.match(r'^(\d+(\.\d+)?)\s*(([KMG]?B)?)$', size, re.IGNORECASE)
    if match:
        size_number = float(match.group(1))
        size_unit = match.group(3).upper()
        if size_unit == 'B':
            return int(size_number)
        elif size_unit == 'KB':
            return int(size_number * 1024)
        elif size_unit == 'MB' or size_unit == '': # the default unit
            return int(size_number * 1024 * 1024)
        elif size_unit == 'GB':
            return int(size_number * 1024 * 1024 * 1024)
        else:
            raise ValueError(f'Size unit is not sopported: {size_unit}')
    else:
        raise ValueError(f'Cannot recognize this size: {size}')

def _get_readable_size(size):
    """
    In order to print a more readable
    size, use less significant digits and a proper unit according to the range
    of file size.

    - byte or bytes: when size is less than 1000 bytes, show the number as is. E.g.,
      1 byte, 50 bytes, 900 bytes.
    - KB: when size is equal to or greater than 1000 bytes and less than 1000 KB, use
      KB and round to 0 decimal places. 1 KB is 2^10 bytes. E.g., 1 KB, 50 KB, 900 KB.
    - MB: when size is equal to or greater than 1000 KB and less than 1000 MB, use
      MB and round to 1 decimal places. 1 MB is 2^10 KB. E.g., 1.0 MB, 50.3 MB,
      950.7 MB.
    - GB: when size is equal to or greater than 1000 MB, use GB and Round to 2
      decimal palaces. 1 GB is 2^10 MB. E.g., 1.00 GB, 50.32 GB, 250.72 GB.
    """
    # size should be an integer represent the size of file in bytes.
    if size < 1000:
        r_unit = 'bytes' if size > 1 else 'byte'
        r_size = str(size)
    elif size < 1000 * 1024:
        r_unit = 'KB'
        r_size = f'{round(size / 1024, 0):.0f}'
    elif size < 1000 * 1024 * 1024:
        r_unit = 'MB'
        r_size = f'{round(size / 1024 / 1024, 1):.1f}'
    else:
        r_unit = 'GB'
        r_size = f'{round(size / 1024 / 1024 / 1024, 2):.2f}'

    return f'{r_size} {r_unit}'

def search_big_files(top, min_size):
    """
    Search a directory recursively to find files that equal or larger
    than a specified size in bytes. Default search size is 1 MB
    (1MB = 1048567 Bytes).
        min_size: accept number and string. If it is a number, treat its unit
        is bytes. Accepted string is like "10B", "10KB", "10MB",
        or "10GB".
    """

    min_size = _parse_size(min_size)
    min_size_info = f'{_get_readable_size(min_size)} ({min_size:,d} bytes)'
    print(f'Searching files equal to or larger than {min_size_info} in folder: "{top}" ...')
    try:
        for root, _dirs, files in os.walk(top):
            for name in files:
                try:
                    filepath = os.path.join(root, name)
                    filesize = os.path.getsize(filepath)
                    if filesize >= min_size:
                        size_info = f'{_get_readable_size(filesize)} ({filesize:,d} bytes)'
                        print(f'{size_info} {filepath}')
                except OSError as err:
                    if err.errno == errno.ENOENT and os.path.islink(err.filename):
                        # suppress the error message when the file or folder a
                        # symlink referenced does not exist.
                        pass
                    else:
                        print(err)
    except OSError as err:
        print(err)
    print('Search is done.')

if __name__ == '__main__':
    import sys

    if len(sys.argv) != 3:
        raise ValueError('Please provide the root folder and min size to search')

    search_big_files(sys.argv[1], sys.argv[2])
