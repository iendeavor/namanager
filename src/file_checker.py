import os
import re
from enums import FORMATS
from settings import (CHECK_DIRS, FILE_FORMATS, DIR_FORMATS,
                      IGNORE_FILES, IGNORE_DIRS)


class FileChecker():
    def __init__(self):
        self.error_list = []

    def is_string_matching(self, string, re_match_list=[]):
        for pattern in re_match_list:
            if re.match(pattern, string):
                return True
        return False

    def convert_sep(self, string, cases):
        for case in cases:
            if case == 'dash_to_underscore':
                string = string.replace('-', '_')
            if case == 'underscore_to_dash':
                string = string.replace('_', '-')
        return string

    def _convert_filename(self, filename):
        pass

    def _convert_dirname(self, dirname):
        pass

    def check(self, root):
        for (dirpath, dirname, filename) in os.walk(root):
            pass


def check_settings():
    if not isinstance(CHECK_DIRS, list):
        raise Exception('CHECK_DIRS must be list.')
    if not isinstance(IGNORE_FILES, list):
        raise Exception('IGNORE_FILES must be list.')
    if not isinstance(IGNORE_DIRS, list):
        raise Exception('IGNORE_DIRS must be list.')
    if not isinstance(FILE_FORMATS, dict):
        raise Exception('FILE_FORMATS must be dict.')
    if not isinstance(DIR_FORMATS, dict):
        raise Exception('DIR_FORMATS must be dict.')

    for k, v in FILE_FORMATS.items():
        if k not in FORMATS:
            raise Exception('FILE_FORMATS has wrong key.')
        elif v not in FORMATS[k]:
            raise Exception('FILE_FORMATS[\'{0}\'] has wrong key.'.format(k))

    for k, v in DIR_FORMATS.items():
        if k not in FORMATS:
            raise Exception('DIR_FORMATS has wrong key.')
        elif v not in FORMATS[k]:
            raise Exception('DIR_FORMATS[\'{0}\'] has wrong key.'.format(k))


if __name__ == '__main__':
    check_settings()

    checker = FileChecker()
    for d in CHECK_DIRS:
        checker.check(d)

    for e in checker.error_list:
        print(e)
