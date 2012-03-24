from setuptools import setup, find_packages
import os

entry_points = """

[console_scripts]

youtuber = youtuber.__init__:main
"""

setup(
  name='youtuber',
  version='0',
  author="Jackie Murphy",
  author_email="jackie.murphy@gmail.com",
  description="Download Youtube videos",
  packages=find_packages(),
  package_dir={'': os.sep.join(['src'])},
  include_package_data=True,
  install_requires=[
      "feedparser",
      "bottle",
  ],
  entry_points=entry_points,
)
