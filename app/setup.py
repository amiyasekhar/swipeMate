from setuptools import setup

APP = ['main_testing.py']
OPTIONS = {
    'packages': ['PyQt6', 'requests', 'pychrome'],
    'plist': {
        'CFBundleName': 'SwipeMate',
        'CFBundleDisplayName': 'SwipeMate',
        'CFBundleIdentifier': 'com.amiyasekhar.swipemate',
        'CFBundleShortVersionString': '1.0',
        'CFBundleVersion': '1.0.0',
        'LSMinimumSystemVersion': '10.14.0',
    },
}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)