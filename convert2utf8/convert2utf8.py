#!/usr/bin/env python

"""Convert file encoded with Shift-JIS to UTF-8."""

import sys
import tempfile

BLOCKSIZE = 1048576 # 1 MB. Unit is Byte.

def convert_to_utf8(source_file_name, source_encoding = 'shift-jis'):
    """Convert file encoded with Shift-JIS to UTF-8."""

    with tempfile.TemporaryFile("w+t") as temp_file:
        read_succeeded = False
        try :
            with open(source_file_name, "r", encoding = source_encoding) as source_file:
                while True:
                    contents = source_file.read(BLOCKSIZE)
                    if not contents:
                        break
                    temp_file.write(contents)
        except FileNotFoundError as err:
            print(f'No such file or directory: "{err.filename}"')
        except IsADirectoryError as err:
            print(f'Error: Is a directory: "{err.filename}"')
        except PermissionError as err:
            print(f'Have no read permission: "{err.filename}"')
        else:
            read_succeeded = True

        if read_succeeded :
            temp_file.seek(0)

            # Overwrite original file with different encoding.
            try :
                with open(source_file_name, "w", encoding = "utf-8") as source_file:
                    while True:
                        contents = temp_file.read(BLOCKSIZE)
                        if not contents:
                            break
                        source_file.write(contents)
            except PermissionError as err:
                print(f'Have no write permission: "{err.filename}"')

if __name__ == '__main__':
    # Parse command line arguments
    if len(sys.argv) != 2:
        raise ValueError('Please provide the name of file to be converted to utf-8 encoded.')

    convert_to_utf8(sys.argv[1])
