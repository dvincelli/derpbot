from setuptools import setup, find_packages

setup(
    name = "derpbot",
    author = "#funnels",
    packages = find_packages(),
    install_requires = [
        'sleekxmpp == 1.1.11',
        'dnspython',
        'requests'
    ],
)
