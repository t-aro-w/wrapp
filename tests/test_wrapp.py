#!/usr/bin/env python3
import sys
sys.path.insert(0, 'src/wrapp')
import wrapp


_EXPECT_STDOUT_NEW = '''#!/usr/bin/env python3
from logging import getLogger


logger = getLogger(__name__)


def add_arguments(parser):
    ...


def main(args):
    ...'''


def test_new(capsys):
    wrapp.new()
    captured = capsys.readouterr()
    assert captured == _EXPECT_STDOUT_NEW
