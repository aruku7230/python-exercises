#!/bin/bash

# Only tested on macOS

# Change current directory to script directory
pushd "$(dirname "$0")" > /dev/null

[[ -d test_files ]] && rm -rf test_files
mkdir test_files && pushd test_files > /dev/null
mkdir home && pushd home > /dev/null

dd if=/dev/zero of=zero.out bs=1 count=0 2> /dev/null
dd if=/dev/zero of=a.out bs=1 count=1 2> /dev/null
dd if=/dev/zero of=readme.out bs=300 count=1 2> /dev/null
dd if=/dev/zero of=todo.out bs=200 count=1 2> /dev/null
ln -sf /tmp/not_existed_file_99999999 link.out

mkdir app
dd if=/dev/zero of=app/text_editor.out bs=1m count=2 2> /dev/null
dd if=/dev/zero of=app/tree.out bs=3k count=1 2> /dev/null

mkdir books
dd if=/dev/zero of=books/learn_emacs.out bs=1228 count=1  2> /dev/null #1.2 kibibytes
dd if=/dev/zero of=books/learn_javascript.out bs=1k count=1 2> /dev/null
dd if=/dev/zero of=books/learn_python.out bs=2k count=1 2> /dev/null

mkdir videos && mkdir videos/family
dd if=/dev/zero of=videos/family/happy_birthday.out bs=1m count=10 2> /dev/null
dd if=/dev/zero of=videos/family/happy_newyear.out bs=1m count=30 2> /dev/null
dd if=/dev/zero of=videos/family/weekend.out bs=1m count=12 2> /dev/null

popd > /dev/null && popd > /dev/null