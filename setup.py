from setuptools import setup

VERSION = '0.1.0'


setup(
    name='tc-wkhtmltopdf',
    version=VERSION,
    description='Wkhtmltopdf service',
    author='Andrey Maksimov',
    author_email='nndii@pm.me',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    platforms='any',
    packages=['tc_wkhtmltopdf'],
    install_requires=[
        'aiohttp (>=3.5.4,<4.0)',
        'hostport',
        'docopt',
        'loguru',
    ],
    include_package_data=True,
)
