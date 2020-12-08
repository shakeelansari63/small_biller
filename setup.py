import sys
from setuptools import setup

install_requires = ['PyQt5', 'qtmodern', 'xlsxwriter', 'pyinstaller']

setup(
    # basic package data
    name='Small Biller',
    version='0.1',
    author='Shakeel Ansari',
    author_email='shakeel.ansari@gmail.com',
    license='',
    url='https://github.com/shakeelansari63/small_biller',
    install_requires=install_requires,
)
