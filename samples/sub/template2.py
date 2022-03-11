#!/usr/bin/env python3
from logging import getLogger
from pathlib import Path

LOG = getLogger(__name__)


def add_arguments(parser):
    group = parser.add_argument_group(__name__)
    group.add_argument(
            '--option', action='store_true',
            help='An option.')


def main(args):
    LOG.debug('debug')
    LOG.info('info')
    LOG.warning('warning')
    LOG.error('error')
    LOG.critical('critical')
    ...
