from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='oopsgenie',
    version='0.1.0',
    description='Functions to run analysis on an exported OpsGenie alert CSV',
    long_description=readme(),
    url='https://github.com/tlugger/oopsgenie',
    author='tlugger, dianaabishop',
    author_email='notnottyler@gmail.com',
    keywords=['opsgenie'],
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
    ],
    packages=find_packages(),
    install_requires=[
        'fuzzywuzzy',
    ],
)