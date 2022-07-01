#!/usr/bin/env python3
from logging import getLogger
from pathlib import Path

from sub import template2

LOG = getLogger(__name__)


def add_arguments(parser):
    group = parser.add_argument_group(__name__)
    group.add_argument(
            'in_file', type=Path,
            help='An input file.')
    group.add_argument(
            '--out-dir', '-d', type=Path, default=None,
            help='A directory.')
    template2.add_arguments(parser)


def main(args):
    LOG.debug('debug')
    LOG.info('info')
    LOG.warning('warning')
    LOG.error('error')
    LOG.critical('critical')
    ...


if __name__ == '__main__':
    import wrapp
    wrapp.main(add_arguments, main, LOG)
