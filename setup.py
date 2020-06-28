from distutils.core import setup
from setuptools import find_packages

setup(
    name='Cop Reporter',
    version='1.1',
    description='Cop Reporter setup.py',
    author='Dhruv Sharma',
    author_email='shdhruvsh@address.com',
    packages=find_packages(),
#    options=options,
    package_data={'testapp': ['*.py', '*.png', '*.kv']}
)