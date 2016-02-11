"""Test setup for collective.recipe.template.
"""

import re

import zc.buildout.testing

import doctest
import unittest
from zope.testing import renormalizing


def setUp(test):
    zc.buildout.testing.buildoutSetUp(test)
    zc.buildout.testing.install_develop('collective.recipe.template', test)
    zc.buildout.testing.install('zope.testing', test)
    zc.buildout.testing.install('Genshi', test)


checker = renormalizing.RENormalizing([
    zc.buildout.testing.normalize_path,
    (re.compile('#![^\n]+\n'), ''),
    (re.compile('-\S+-py\d[.]\d(-\S+)?.egg'),
     '-pyN.N.egg',
    ),
    ])


def test_suite():
    return unittest.TestSuite([
        doctest.DocFileSuite('README.rst',
            setUp=setUp, tearDown=zc.buildout.testing.buildoutTearDown,
            optionflags=doctest.ELLIPSIS|doctest.NORMALIZE_WHITESPACE,
            checker=checker),
        doctest.DocFileSuite('genshitemplate.rst',
            setUp=setUp, tearDown=zc.buildout.testing.buildoutTearDown,
            optionflags=doctest.ELLIPSIS|doctest.NORMALIZE_WHITESPACE,
            checker=checker),
        ])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
