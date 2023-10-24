"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""
from setuptools import setup
DATA_FILES = ['faces', 'word_files']
APP = ['PySpell.py']
#OPTIONS = {'argv_emulation': True}

setup(
    app=APP,
    data_files=DATA_FILES,
    options=
            dict(py2app=dict(
            #iconfile =  'cupcake.icns',
            plist=dict(
                Copyright='2010 Daniel Ross',
                NSHumanReadableCopyright='2010 Daniel Ross',
                CFBundleVersion='.5',
            ),
    )),
    #options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)