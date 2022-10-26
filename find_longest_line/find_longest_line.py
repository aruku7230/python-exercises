#! /usr/bin/env python

import sys

def find_longest_line(file_path):
    """Find longest line of a file."""
    with open(file_path, 'r', encoding = 'utf8') as file:
        return max(file, key = len, default = '')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Please give a file path.')
        sys.exit(1)
    file_path = sys.argv[1]
    print(f'Longest line of file "{file_path}" is:\n{find_longest_line(file_path)}')
