from setuptools import setup, find_packages

setup(
    name='JSD-project',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'Arpeggio == 2.0.2',
        'click == 8.1.7',
        'colorama == 0.4.6',
        'textX == 4.0.1'
    ],
)
