from setuptools import setup, find_packages

setup(
    name='noteplus',
    version='1.0.0',
    packages=find_packages(exclude=['docs', 'tests*']),
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'noteplus = noteplus.__main__:main'
        ]
    })
