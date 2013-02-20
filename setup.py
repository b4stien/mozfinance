from setuptools import setup

setup(
    name='warfinance',
    version='0.0.1dev',
    packages=['warfbiz', 'warfdata'],
    test_suite='tests',
    install_requires=['SQLAlchemy', 'voluptuous', 'psycopg2', 'warbase'],
    author='Bastien GANDOUET',
    author_email="bastien@pectoribus.net"
)
