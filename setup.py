from setuptools import setup, find_packages

with open('README.md') as fh:
    README = fh.read()

setup(
    name='cigen',
    version='0.1.0',
    description='A Continuous Integration Generator',
    author='Paulo Lopes Estevao',
    packages=find_packages(include=['cigen', 'cigen.*']),
    include_package_data=True,
    install_requires=[
        'Click',
        'PyYAML',
        'rich',
    ],
    license='MIT',
    long_description=README,
    url='https://github.com/Paulo-Lopes-Estevao/ci-generator',
    entry_points={
        'console_scripts': [
            'cigen = cigen.__main__:cli',
        ]
    },
)