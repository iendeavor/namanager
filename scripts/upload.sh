# changes version which user defined
# pass version to $1
if [ $# -eq 1 ]; then
    PIP=`which pip$1`
    PYTHON=`which python$1`
else
    PIP=`which pip`
    PYTHON=`which python`
fi

if [ "`$PIP -V`" != "`$PYTHON -m pip -V`" ]; then
    $PIP -V
    $PYTHON -V
    echo "Version of pip and python must be same."
    echo
    echo "Add version suffix as argument if you wnat to specify version."
    echo "example: your python command is 'PYTHON.6' => type 'your_script 3.6'"
    exit 1
fi

cwd=$(pwd)
namanager_root_path="$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )/.."
cd $namanager_root_path

$PYTHON -m venv env/upload
rm -rf build dist
source ./env/upload/bin/activate

$PIP install --upgrade pip
$PIP install -r requirements.txt
$PIP install twine
$PIP install sdist
$PYTHON setup.py sdist
$PIP install wheel
$PYTHON setup.py bdist_wheel --universal
twine upload dist/*
rm -rf dist
deactivate

cd $CWD
