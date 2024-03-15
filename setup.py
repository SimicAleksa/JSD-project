from setuptools import setup, find_packages

setup(
    name='JSD_project',
    version='0.4',
    packages=find_packages(),
    install_requires=[
        'Arpeggio == 2.0.2',
        'click == 8.1.7',
        'colorama == 0.4.6',
        'textX == 4.0.1',
        'twine==5.0.0',
        'setuptools==69.1.0',
        'wheel==0.43.0'
    ],
)
