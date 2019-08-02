#!/usr/bin/env python
"""
Show the download history for a single individual.
"""
#######################
from __future__ import print_function, unicode_literals

import os
import sys

from download.models import History_Record

#######################

DJANGO_COMMAND = 'entrypoint'
OPTION_LIST = ()
ARGS_USAGE = '[who] [what]'
HELP_TEXT = __doc__.strip()


def main(who, what):
    for rec in History_Record.objects.filter(
            user__username=who, software__slug=what):
        print(rec)


def entrypoint(options, args):
    if len(args) != 2:
        print('syntax: ./%s download list_history_reset [who] [what]' %
              os.path.basename(sys.argv[0]))
        print('  e.g.: ./%s download list_history_reset umgabri0 jmp' %
              os.path.basename(sys.argv[0]))
        return
    main(args[0], args[1])
