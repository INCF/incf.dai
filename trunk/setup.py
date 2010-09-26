from setuptools import setup, find_packages
import os

version = '0.6'

setup(name='incf.dai',
      version=version,
      description="Python API for the INCF Digital Atlasing infrastructure",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='WPS INCF "Digital Atlasing"',
      author='Raphael Ritz',
      author_email='raphael.ritz@incf.org',
      url='http://software.incf.org/software/incfdai',
      license='GPL',
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
