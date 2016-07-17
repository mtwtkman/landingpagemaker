#! /usr/bin/bash

if [ $# == 0 ]; then
  # all tests
  test_name="tests/test_*.py"
elif [ $# == 1 ]; then
  # test module
  test_name="tests.test_${1}"
elif [ $# == 2 ]; then
  # test case
  test_name="tests.test_${1}.${2}"
elif [ $# == 3 ]; then
  # test method
  test_name="tests.test_${1}.${2}.test_${3}"
fi

python -m unittest ${test_name}
