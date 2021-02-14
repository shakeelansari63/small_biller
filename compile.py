from py_compile import compile
from PyInstaller.__main__ import run as pybuild
import os
import sys
import shutil
import tarfile
from zipfile import ZipFile, ZIP_DEFLATED


def compile_package(packagename):
    # App Path
    appth = os.path.dirname(os.path.abspath(__file__))
    print(appth)

    # Cleanup existing build and dist dirs
    if os.path.exists('build/'):
        shutil.rmtree('build/')

    if os.path.exists('dist/'):
        shutil.rmtree('dist/')

    if os.path.exists('__pycache__/'):
        shutil.rmtree('__pycache__/')

    for pyfile in os.listdir(os.path.join(appth, 'MainApp/')):
        if pyfile.endswith('.py'):
            # print(pyfile)
            compile(os.path.join(appth, 'MainApp/') + pyfile,
                    os.path.join(appth, 'pycs/') + pyfile + 'c')

    # For importing qtmodern theme
    import qtmodern
    qtm_path = os.path.dirname(os.path.abspath(qtmodern.__file__))

    # Set Logo File
    platformid = sys.platform
    if platformid == 'linux' or platformid == 'darwin':
        logofile = os.path.join(appth, "logo.png")
        sep = ':'
    else:
        logofile = os.path.join(appth, "logo.ico")
        sep = ';'

    pybuild([
        "{}/main.py".format(appth),
        "--clean",
        "--log-level=INFO",
        "--onedir",
        "--name={}".format(packagename),
        "--hidden-import=qtmodern",
        "--hidden-import=xlsxwriter",
        "--add-data={}/pycs{}./MainApp".format(appth, sep),
        "--add-data={}/MainApp/res{}./MainApp/res".format(appth, sep),
        "--add-data={}/resources{}./qtmodern/resources".format(qtm_path, sep),
        "--windowed",
        "--icon={}".format(logofile)
    ])

    # Cleanup Temporary Files
    shutil.rmtree(os.path.join(appth, 'pycs/'))

    os.remove('{}.spec'.format(packagename))

    # For testing
    # platformid = 'win32'

    # Go to Dist Directory
    os.chdir('dist/')

    # Package in tar File
    target_dir = '{}'.format(packagename)
    if platformid == 'linux' or platformid == 'darwin':
        with tarfile.open('{}.tar.gz'.format(os.path.join(appth, packagename)), 'w:gz') as tar:
            tar.add(target_dir, arcname=packagename)

    # Package in Zip File
    else:
        with ZipFile('{}.zip'.format(target_dir), 'w', ZIP_DEFLATED) as ziph:
            for root, _, files in os.walk(target_dir):
                for file in files:
                    ziph.write(os.path.join(root, file))


if __name__ == '__main__':
    compile_package('SmallBiller')
    print('Code compiled successfully')