from setuptools import setup, find_packages

setup(
    name = "derpbot",
    author = "#funnels",
    packages = find_packages(),
    install_requires = [
        open('requirements.txt').read().splitlines()
    ],
    zip_safe = False
)
