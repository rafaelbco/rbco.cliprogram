from setuptools import setup, find_packages
import os

version = '0.0.1'

setup(name='rbco.cliprogram',
      version=version,
      description="Helpers to write Command Line Interface (CLI) programs.",
      long_description='\n'.join([
        open('README.txt').read(),
        open('TODO.txt').read(),
        open('HISTORY.txt').read()
      ]),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='cli command shell',
      author='Rafael Oliveira',
      author_email='rafaelbco@gmail.com',
      url='http://code.google.com/p/rbco-cliprogram/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['rbco'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'prdg.util>=0.0.3,<=0.0.99',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
