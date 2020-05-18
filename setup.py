"""
    This module store all setup data
"""

from setuptools import setup

setup(
    name='P5',
    version='1.0',
    packages=['src',
              'src.api',
              'src.api',
              'src.app',
              'src.models',
              'src.utils'],
    url='https://github.com/CamClrt/FoodChoice',
    license='',
    author='Camille Clarret',
    author_email='camille.clarret@gmail.com',
    description='[P5] : OpenClassrooms student project - Import '
                'data from the OpenFoodFact API and find healthier products',
    scripts=['src/main.py']
)

