#!/usr/bin/env python
"""
Remove any files on disk that have no corresponding DownloadFile record.
"""
#######################
from __future__ import print_function, unicode_literals

import os
#######################
from optparse import make_option

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from download.models import Download_File

DJANGO_COMMAND = 'main'
OPTION_LIST = (
    make_option(
        '',
        '--noinput',
        action='store_true',
        default=False,
        help='Do NOT prompt for input of any kind.'),
    make_option(
        '-n',
        '--dry-run',
        action='store_true',
        default=False,
        help='Do everything except modify the filesystem.'),
)
ARGS_USAGE = ''
HELP_TEXT = __doc__.strip()


def remove_file(storage, path, basename, dry_run, verbosity):
    filename = os.path.join(path, basename)
    assert os.path.exists(
        filename
    ), 'File does not exists, but django FileSystemStorage claims it does!'
    if verbosity > 0:
        if not dry_run:
            print('DELETING', end=' ')
        else:
            print('WOULD DELETE', end=' ')
        print(repr(filename), '...', end=' ')
    if not dry_run:
        storage.delete(filename)
    if verbosity > 0:
        print()


def delete_orphans(path='', dry_run=True, verbosity=1):
    """
    Include the path argument, for future recursive descent.
    """
    storage = FileSystemStorage(location=settings.DOWNLOAD_STORAGE_PATH)
    directory_list, file_list = storage.listdir(path)
    # we ignore the directory_list, since Download_File
    # specifies recursive=False for the FilePathField
    downloadfile_list = Download_File.objects.all()  # including inactive.

    seen_files = set()
    for dlfile in downloadfile_list:
        path, basename = os.path.split(dlfile.filename)
        if basename in file_list:
            seen_files.add(basename)
        else:
            # no physical file matching DB record!
            if verbosity > 0:
                print('WARNING: no physical file found for {0}'.format(dlfile))

    rm_list = set(file_list).difference(seen_files)
    for basename in rm_list:
        remove_file(storage, path, basename, dry_run, verbosity)


def main(options, args):
    proceed = False
    if not options['noinput']:
        print(
            'CAUTION: Use this *only* on the machine that actually has the file system storage!'
        )
        print('Are you sure you want to continue?')
        resp = input('[y/N] ')
        if resp.lower() in ['y', 'ye', 'yes']:
            proceed = True
    else:
        proceed = True

    if proceed:
        delete_orphans(
            dry_run=options['dry_run'], verbosity=int(options['verbosity']))
