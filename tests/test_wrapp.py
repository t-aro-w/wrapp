#!/usr/bin/env python3
from unittest.mock import patch
import pytest
import sys
sys.path.insert(0, 'src/wrapp')
import wrapp


_EXPECT_STDOUT_NEW = '''#!/usr/bin/env python3
from logging import getLogger


logger = getLogger(__name__)


def add_arguments(parser):
    group = parser.add_argument_group(__name__)
    ...


def main(args):
    ...
'''


def test_new(capsys):
    wrapp.new()
    captured = capsys.readouterr()
    assert len(captured.out) == len(_EXPECT_STDOUT_NEW)
    for actual, expected in zip(captured.out, _EXPECT_STDOUT_NEW):
        assert actual == expected


_EXPECT_STDOUT_MAIN_H = '''usage: template.py [-h] [--out-dir OUT_DIR] [--option] in_file

optional arguments:
  -h, --help            show this help message and exit

template:
  in_file               An input file.
  --out-dir OUT_DIR, -d OUT_DIR
                        A directory. (default: None)

sub.template2:
  --option              An option. (default: False)
'''.splitlines()


_EXPECT_STDOUT_MAIN_H_PY3_10 = '''usage: template.py [-h] [--out-dir OUT_DIR] [--option] in_file

options:
  -h, --help            show this help message and exit

template:
  in_file               An input file.
  --out-dir OUT_DIR, -d OUT_DIR
                        A directory. (default: None)

sub.template2:
  --option              An option. (default: False)
'''.splitlines()


@patch('sys.argv', ['wrapp', 'template.py', '-h'])
def test_main(capsys):
    with pytest.raises(SystemExit) as e:
        wrapp.main()
    assert e.value.code == 0
    captured = capsys.readouterr()
    actual_lines = captured.out.splitlines()
    expect_lines = _EXPECT_STDOUT_MAIN_H_PY3_10 if sys.version_info.minor >= 10 else _EXPECT_STDOUT_MAIN_H
    for i, (actual, expected) in enumerate(zip(actual_lines, expect_lines)):
        assert actual == expected, i
    assert len(actual_lines) == len(expect_lines)
