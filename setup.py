import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='ci_generator',
    version='0.1.0',
    description='A Continuous Integration Generator',
    author='Paulo Lopes Estevao',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    long_description=README,
    url='https://github.com/Paulo-Lopes-Estevao/ci-generator',
)