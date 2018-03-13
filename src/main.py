import os
import json
import argparse
from enums import FORMATS
from file_checker import FileChecker # noqa

SETTINGS_FILE = 'src/settings.json'
SETTINGS_JSON = {}


def raiser(condition, msg):
    if not condition:
        raise Exception('settings must be dict.')  # pragma: no cover


def import_settings():
    global SETTINGS_JSON

    with open(SETTINGS_FILE, 'r') as s:
        SETTINGS_JSON = json.loads(s.read())

    raiser(isinstance(SETTINGS_JSON, dict),
           Exception('settings must be dict.'))

    SETTINGS_JSON['CHECK_DIRS'] = SETTINGS_JSON.get('CHECK_DIRS', [])
    raiser(isinstance(SETTINGS_JSON['CHECK_DIRS'], list),
           Exception('CHECK_DIRS must be list.'))

    SETTINGS_JSON['ONLY_FILES'] = SETTINGS_JSON.get('ONLY_FILES', [])
    raiser(isinstance(SETTINGS_JSON['ONLY_FILES'], list),
           Exception('ONLY_FILES must be list.'))

    SETTINGS_JSON['ONLY_DIRS'] = SETTINGS_JSON.get('ONLY_DIRS', [])
    raiser(isinstance(SETTINGS_JSON['ONLY_DIRS'], list),
           Exception('ONLY_DIRS must be list.'))

    SETTINGS_JSON['IGNORE_FILES'] = SETTINGS_JSON.get('IGNORE_FILES', [])
    raiser(isinstance(SETTINGS_JSON['IGNORE_FILES'], list),
           Exception('IGNORE_FILES must be list.'))

    SETTINGS_JSON['IGNORE_DIRS'] = SETTINGS_JSON.get('IGNORE_DIRS', [])
    raiser(isinstance(SETTINGS_JSON['IGNORE_DIRS'], list),
           Exception('IGNORE_DIRS must be list.'))

    SETTINGS_JSON['FILE_FORMATS'] = SETTINGS_JSON.get('FILE_FORMATS', {})
    raiser(isinstance(SETTINGS_JSON['FILE_FORMATS'], dict),
           Exception('FILE_FORMATS must be dict.'))

    SETTINGS_JSON['DIR_FORMATS'] = SETTINGS_JSON.get('DIR_FORMATS', {})
    raiser(isinstance(SETTINGS_JSON['DIR_FORMATS'], dict),
           Exception('DIR_FORMATS must be dict.'))

    for k, v in SETTINGS_JSON['FILE_FORMATS'].items():
        raiser(k in FORMATS,
               Exception('FILE_FORMATS has wrong key.'))
        raiser(v in FORMATS[k],
               Exception('FILE_FORMATS[\'{0}\'] has wrong key.'.format(k)))

    for k, v in SETTINGS_JSON['DIR_FORMATS'].items():
        raiser(k in FORMATS,
               Exception('DIR_FORMATS has wrong key.'))
        raiser(v in FORMATS[k],
               Exception('DIR_FORMATS[\'{0}\'] has wrong key.'.format(k)))


def parse():  # pragma: no cover
    global SETTINGS_FILE

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--setting_file', help='The settings file name')
    args = parser.parse_args()
    if args.setting_file:
        SETTINGS_FILE = args.setting_file


def main():  # pragma: no cover
    for d in SETTINGS_JSON['CHECK_DIRS']:
        checker = FileChecker(SETTINGS_JSON)
        checker.check(d)

        for e in checker.error_set:
            print(e)

        print('In folder {0} :'.format(os.path.realpath(d)))
        # print("In folder '../Cosmos/code': ".format(d))
        if checker.error_set:
            print('FAILED (error{0}={1})\n'.format(
                  's' if len(checker.error_set) > 1 else '',
                  len(checker.error_set)))
        else:
            print('OK.\n')


if __name__ == '__main__':
    parse()  # pragma: no cover
    import_settings()  # pragma: no cover
    main()  # pragma: no cover
