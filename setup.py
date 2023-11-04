from setuptools import setup, find_packages

with open('README.md') as fh:
    README = fh.read()

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