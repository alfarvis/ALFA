from setuptools import setup, find_packages

setup(
    name='Alfarvis',
    version='0.1dev',
    packages=find_packages(exclude=['tests*']),
    license='Mozilla Public License Version 2.0',
    long_description=open('README.md').read(),
)
