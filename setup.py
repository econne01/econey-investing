from setuptools import setup, find_packages

setup(
    name = "yahoo-stock-db",
    version = "0.1",
    url = 'https://github.com/econne01/yahoo-stock-db',
    author = 'Eric Connelly',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    install_requires = ['setuptools'],
)