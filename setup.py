from setuptools import setup, find_packages
import os
import sys

version = '2.0'

genshi_requirement = 'Genshi'
if sys.version_info >= (3,):
    genshi_requirement = 'Genshi>=0.7.0'

setup(
    name='collective.recipe.template',
    version=version,
    description="Buildout recipe to generate a text file from a template",
    long_description=(
        open("README.rst").read() + "\n\n" +
        open(os.path.join("collective", "recipe", "template",
                          "README.rst")).read() + "\n\n" +
        open(os.path.join("docs", "HISTORY.rst")).read()
    ),
    classifiers=[
        "Framework :: Buildout",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='template recipe',
    author='Wichert Akkerman',
    author_email='wichert@wiggy.net',
    url='http://pypi.python.org/pypi/collective.recipe.template',
    license='BSD',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['collective', 'collective.recipe'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'zc.buildout',
    ],
    extras_require=dict(
        test=['zope.testing', ],
        genshi=[genshi_requirement, ],
    ),
    entry_points="""
    [zc.buildout]
    default = collective.recipe.template:Recipe
    genshi = collective.recipe.template.genshitemplate:Recipe
    """,
    use_2to3=True,
    convert_2to3_doctests=[
        os.path.join('collective', 'recipe', 'template', 'README.rst'),
        os.path.join(
            'collective', 'recipe', 'template', 'genshitemplate.rst')
    ]
)
