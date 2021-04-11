Search a folder recursively for files the size of which are equal to or bigger
than a specified size.

## Usage:

    search_big_files root_directory min_size

- `root_directory` is the root directory to search.
- `min_size` is the minimum size to search. The formats is `<number><unit>`.
  - `<number>` could be an integer or float.
  - Supported `<unit>` are `B` for bytes, `KB` for KibiBytes(2^10Bytes), `MB` for
    MebiBytes (2^10KB, the default), and `GB` for GibiBytes(2^10MB). `<unit>`
    may be ommited, then the default unit (`MB`) will be used.
  - There could be whitespace charater between `<number>` and `<unit>`.

## Output

The output will go to `stdout`, the first line will output the root directory
and minmum size to search, followed by qualified files one file one line. Before
the file full name, the size of that file will also be printed.

### Print the size of file

The size of file in bytes can be get directly. In order to print a more readable
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

### Deal with symbolic file

When the file or folder that the symbolic file points to does not exist, do not
print an error.

## Todo

- Add integration test.
