import os
import json
import datetime
from namanager.core import Namanager
from namanager.archieve_manager import ArchieveManager

SETTINGS_JSON = {}


def raiser(condition, msg):
    if not condition:
        raise Exception(msg)  # pragma: no cover


def import_settings(settings_file):
    global SETTINGS_JSON

    with open(settings_file, 'r') as s:
        SETTINGS_JSON = json.loads(s.read())

    raiser(isinstance(SETTINGS_JSON, dict), 'settings must be dict.')


def test_writing_permission(**kwargs):
    """
    param dirname:
    type dirname: str
    param required: default True
    type required: True, False
    param error_msg:
    type error_msg: str
    """

    try:
        dirname = kwargs.get('dirname', os.getcwd())
        if dirname[-1] != os.sep:
            dirname += os.sep
        # test directory is exists or not and raise
        os.path.realpath(dirname)

        filename = ''.join([dirname, 'test_file'])
        while os.path.exists(filename):
            filename += '_'

        with open(filename, 'w') as f:
            f.write('test...')
        os.remove(filename)

    except Exception as e:
        print(kwargs.get('error_msg', ''))
        required = kwargs.get('required', True)
        if required:
            raise e


def get_src_dst_pair(error_info):
    # we need to move this function to/into a better place
    src_dst_pair = []

    for e in error_info:
        src_dst_pair.append([e['actual'], e['expect']])

    return src_dst_pair


def get_bak_filename(**kwargs):
    prefix = kwargs.get('prefix', '')
    when = kwargs.get('when', '{:%Y%m%d%H%M%S}'.format(
        datetime.datetime.now()))

    return prefix + when + '.bak'


def check(**kwargs):
    REQUIRED = kwargs.get('required', False)
    FMT = kwargs.get('fmt', 'json')
    PRETTY_DUMP = kwargs.get('pretty_dump', False)
    RENAME = kwargs.get('rename', False)
    RENAME_BACKUP = kwargs.get('rename_backup', False)
    RENAME_BACKUP_DIR = kwargs.get('rename_backup_dir', os.getcwd())
    RENAME_RECOVER = kwargs.get('rename_recover', False)
    REVERT_FILE = kwargs.get('revert_file', None)

    if REVERT_FILE is not None:
        am = ArchieveManager()
        with open(REVERT_FILE, 'r') as f:
            am.rename(json.loads(f.read()))

    errors = []

    for d in SETTINGS_JSON['CHECK_DIRS']:
        checker = Namanager(SETTINGS_JSON)

        checker.check(d)

        if FMT == 'dict':
            RESULT = checker.get_dict(checker.error_info)
        elif FMT == 'json':
            RESULT = checker.get_json(checker.error_info, PRETTY_DUMP)
        elif FMT == 'xml':
            RESULT = checker.get_xml(checker.error_info, PRETTY_DUMP)

        print(RESULT)
        if RESULT:
            if RENAME:
                am = ArchieveManager()
                error_info = checker.get_dict(checker.error_info)
                error_info = get_src_dst_pair(error_info)

                if RENAME_BACKUP:
                    test_writing_permission(dirname=RENAME_BACKUP_DIR)
                    filename = get_bak_filename(prefix='namanager_rename_')
                    with open(os.sep.join([RENAME_BACKUP_DIR, filename]),
                              'w') as f:
                        f.write(json.dumps(
                            am.gen_revert_path_pairs(error_info),
                            indent=4, sort_keys=True))

                error_pairs = am.rename(error_info)

                if RENAME_RECOVER and error_pairs:
                    # try to directly revert all paths
                    recover_pairs = am.gen_revert_path_pairs(error_info)
                    am.rename(recover_pairs)

            errors.append('In folder {0} :'.format(os.path.realpath(d)))
            errors.append('FAILED (error{0}={1})'.format(
                  's' if len(RESULT) > 1 else '',
                  checker.error_info_count))

    print("")
    if errors:
        for e in errors:
            print(e)
        if REQUIRED:
            exit(1)
    else:
        print('OK.\n')


def entry(settings_file, **kwargs):
    import_settings(settings_file)
    check(**kwargs)


if __name__ == '__main__':  # pragma: no cover
    entry('namanager/file_checker/settings.json')
