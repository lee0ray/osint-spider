from setuptools import setup, find_packages
setup(
    name='osint',
    version='1.0',
    packages=find_packages(),
    entry_points={'scrapy':['settings=osint.settings']},
)
