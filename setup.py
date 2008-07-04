from setuptools import setup, find_packages
import os

version = '1.0rc2'

setup(name='collective.recipe.template',
      version=version,
      description="Buildout recipe to generate a text file from a template",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
          "Framework :: Buildout",
          "Programming Language :: Python",
          "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Wichert Akkerman',
      author_email='wichert@wiggy.net',
      url='',
      license='BSD',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective', 'collective.recipe' ],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
      ],
      entry_points="""
      [zc.buildout]
      default = collective.recipe.template:Recipe
      """,
      )
