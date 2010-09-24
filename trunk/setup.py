from setuptools import setup, find_packages
import os

version = '0.4'

setup(name='incf.dai',
      version=version,
      description="Python API for the INCF Digital Atlasing infrastructure",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author='Raphael Ritz',
      author_email='raphael.ritz@incf.org',
      url='http://svn.incf.org/svn/incfdai/',
      license='BSD',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['incf'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'httplib2',
          'odict',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
