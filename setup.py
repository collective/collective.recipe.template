from setuptools import setup, find_packages
import os
import sys

version = '2.2.dev0'

genshi_requirement = 'Genshi'
if sys.version_info >= (3,):
    genshi_requirement = 'Genshi>=0.7.0'

setup(
    name='collective.recipe.template',
    version=version,
    description="Buildout recipe to generate a text file from a template",
    long_description=(
        open("README.rst", "rb").read().decode("utf-8")
        + "\n\n"
        + open(os.path.join("src", "collective", "recipe", "template",
                            "README.rst"), "rb").read().decode("utf-8")
        + "\n\n"
        + open("CHANGES.rst", "rb").read().decode("utf-8")
    ),
    classifiers=[
        "Framework :: Buildout",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='template recipe',
    author='Wichert Akkerman',
    author_email='wichert@wiggy.net',
    url='https://github.com/collective/collective.recipe.template',
    license='BSD',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['collective', 'collective.recipe'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'six',
        'zc.buildout',
    ],
    extras_require=dict(
        test=['zope.testing', 'zope.testrunner'],
        genshi=[genshi_requirement, ],
    ),
    entry_points="""
    [zc.buildout]
    default = collective.recipe.template:Recipe
    genshi = collective.recipe.template.genshitemplate:Recipe
    """,
)
