from setuptools import setup

setup(
    name='mozfinance',
    version='0.2.3',
    packages=['mozfinance'],
    test_suite='tests',
    install_requires=['SQLAlchemy', 'voluptuous', 'mozbase'],
    author='Bastien GANDOUET',
    author_email="bastien@mozaiqu.es"
)
