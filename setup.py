from setuptools import setup, find_packages

setup(
    name = 'mindsweeper',
    version = '0.1.0',
    author = 'Bar Amir',
    description = 'An example package.',
    packages = find_packages(),
    install_requires = ['click'],
    tests_require = ['pytest', 'pytest-cov'],
)