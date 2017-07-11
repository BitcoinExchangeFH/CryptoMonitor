from distutils.core import setup

setup(
    name='CryptoMonitor',
    version='beta',
    author='Aurora Trading Team',
    author_email='auroratradingteam@gmail.com',
    packages=['cryptomon'],
    url='http://pypi.python.org/pypi/CryptoMonitor/',
    license='LICENSE.txt',
    description='Cryptocurrency price arbitrage monitor.',
    entry_points={
            'console_scripts': ['cryptomon=cryptomon.cryptomonitor:main']
        },
    install_requires=[
            'beautifulsoup4'
        ]
    )