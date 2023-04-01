#!/usr/bin/env python3
from unittest.mock import patch
import os
import pytest
import subprocess
import sys
sys.path.insert(0, 'src')
import wrapp


_EXPECT_STDOUT_NEW = '''#!/usr/bin/env python3
from logging import getLogger


LOG = getLogger(__name__)


def set_logger(parent_name):
    global LOG
    LOG = getLogger(f'{parent_name}.{__name__}')


def add_arguments(parser):
    group = parser.add_argument_group(__name__)
    ...


def main(args):
    ...


# code below is an option.
# if you want to run it as an normal Python script
# (`python THIS_SCRIPT.py`), uncomment it.
# if __name__ == '__main__':
#     import wrapp
#     wrapp.main(add_arguments, main, set_logger)'''


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
def test_app_help(capsys):
    with pytest.raises(SystemExit) as e:
        wrapp.app()
    assert e.value.code == 0
    captured = capsys.readouterr()
    actual_lines = captured.out.splitlines()
    expect_lines = _EXPECT_STDOUT_MAIN_H_PY3_10 if sys.version_info.minor >= 10 else _EXPECT_STDOUT_MAIN_H
    for i, (actual, expected) in enumerate(zip(actual_lines, expect_lines)):
        assert actual == expected, i
    assert len(actual_lines) == len(expect_lines)


def capture(command):
    env = os.environ.copy()
    env['PYTHONPATH']= 'src'
    proc = subprocess.Popen(command,
        stdout= subprocess.PIPE,
        stderr= subprocess.PIPE,
        env= env,
    )
    out,err = proc.communicate()
    return out, err, proc.returncode


def test_app():
    command = 'python', 'tests/template.py', '--option', 'in_file'
    expect_lines = [
            'wrapp.py:91 in_file= in_file',
            'wrapp.py:91 out_dir= None',
            'wrapp.py:91 option= True',
            'template.py:30 info',
            'template.py:31 warning',
            'template.py:32 error',
            'template.py:33 critical',
            'template2.py:22 info',
            'template2.py:23 warning',
            'template2.py:24 error',
            'template2.py:25 critical'
            ]
    out, err, returncode = capture(command)
    actual_lines = [' '.join(i.decode().split()[3:]) for i in err.splitlines()]
    for i, (actual, expected) in enumerate(zip(actual_lines, expect_lines)):
        assert actual == expected, actual_lines
    assert len(actual_lines) == len(expect_lines)


def test_cli():
    command = 'python', '-m', 'wrapp', 'tests/template.py', '--option', 'in_file'
    expect_lines = [
            '__main__.py:91 in_file= in_file',
            '__main__.py:91 out_dir= None',
            '__main__.py:91 option= True',
            'template.py:30 info',
            'template.py:31 warning',
            'template.py:32 error',
            'template.py:33 critical',
            'template2.py:22 info',
            'template2.py:23 warning',
            'template2.py:24 error',
            'template2.py:25 critical'
            ]
    out, err, returncode = capture(command)
    actual_lines = [' '.join(i.decode().split()[3:]) for i in err.splitlines()]
    for i, (actual, expected) in enumerate(zip(actual_lines, expect_lines)):
        assert actual == expected, i
    assert len(actual_lines) == len(expect_lines)


def test_wrapp_help():
    command = 'python', '-m', 'wrapp', '-h'
    expect_lines = [
            'usage: __main__.py MODULE_OR_SCRIPT ..',
            '',
            'optional arguments:' if sys.version_info.minor <= 9 else 'options:',
            '  -h, --help  show this help message and exit'
            ]
    out, err, returncode = capture(command)
    actual_lines = [i.decode() for i in out.splitlines()]
    for i, (actual, expected) in enumerate(zip(actual_lines, expect_lines)):
        assert actual == expected, i
    assert len(actual_lines) == len(expect_lines)


def test_wrapp_noargs():
    command = 'python', '-m', 'wrapp'
    expect_lines = [
            'usage: __main__.py MODULE_OR_SCRIPT ..',
            '',
            'optional arguments:' if sys.version_info.minor <= 9 else 'options:',
            '  -h, --help  show this help message and exit'
            ]
    out, err, returncode = capture(command)
    actual_lines = [i.decode() for i in out.splitlines()]
    for i, (actual, expected) in enumerate(zip(actual_lines, expect_lines)):
        assert actual == expected, i
    assert len(actual_lines) == len(expect_lines)


@patch('sys.argv', ['template.py', 'aaa', '--option'])
def test_main():
    import template
    wrapp.main(template.add_arguments,
            template.main,
            template.set_logger)
