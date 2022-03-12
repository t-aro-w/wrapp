#!/usr/bin/env python3
import wrapp
from pytest import capsys


_EXPECT_STDOUT_NEW = '''#!/usr/bin/env python3
from logging import getLogger


logger = getLogger(__name__)


def add_arguments(parser):
    ...


def main(args):
    ...'''


def test_new():
    wrapp.new()
    captured = capsys.readouterr()
    assert captured == _EXPECT_STDOUT_NEW
