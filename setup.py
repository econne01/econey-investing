from setuptools import setup, find_packages

setup(
    name = "econey-investing",
    version = "0.1",
    url = 'https://github.com/econne01/econey-investing',
    author = 'Eric Connelly',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    install_requires = ['setuptools'],
)
