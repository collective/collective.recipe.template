Detailed Description
********************

Simple creation of a file out of a template
===========================================

Lets create a minimal `buildout.cfg` file::

  >>> write('buildout.cfg',
  ... '''
  ... [buildout]
  ... parts = template
  ... offline = true
  ...
  ... [template]
  ... recipe = collective.recipe.template
  ... input = template.in
  ... output = template
  ... ''')

We create a template file::

  >>> write('template.in',
  ... '''#
  ... My template knows about buildout path:
  ...   ${buildout:directory}
  ... ''')

Now we can run buildout::

  >>> print system(join('bin', 'buildout')),
  Installing template.

The template was indeed created::

  >>> cat('template')
  #
  My template knows about buildout path:
  .../sample-buildout

The variable ``buildout:directory`` was also substituted by a path.


Using inline input
==================

For very short script it can make sense to put the source directly into
`buildout.cfg`::

  >>> write('buildout.cfg',
  ... '''
  ... [buildout]
  ... parts = template
  ... offline = true
  ...
  ... [template]
  ... recipe = collective.recipe.template
  ... input = inline:
  ...    #!/bin/bash
  ...    echo foo
  ... output = ${buildout:parts-directory}/template
  ... ''')

Now we can run buildout::

  >>> print system(join('bin', 'buildout')),
  Uninstalling template.
  Installing template.

The template should have been created::

  >>> cat('parts', 'template')
  #!/bin/bash
  echo foo

Normally the file mode gets copied from the template, but it can also be
specified manually, which especially makes sense in this case:

  >>> write('buildout.cfg',
  ... '''
  ... [buildout]
  ... parts = template
  ... offline = true
  ...
  ... [template]
  ... recipe = collective.recipe.template
  ... inline =
  ...    #!/bin/bash
  ...    echo foo
  ... output = ${buildout:parts-directory}/template
  ... mode = 755
  ... ''')

Run buildout again ::

  >>> print system(join('bin', 'buildout')),
  Uninstalling template.
  Installing template.

The template should have the specified file mode::

  >>> from os import stat
  >>> from stat import S_IMODE
  >>> print '%o' % S_IMODE(stat('parts/template').st_mode)
  755


Creating a template in a variable path
======================================

Lets create a minimal `buildout.cfg` file. This time the output should
happen in a variable path::

  >>> write('buildout.cfg',
  ... '''
  ... [buildout]
  ... parts = template
  ... offline = true
  ...
  ... [template]
  ... recipe = collective.recipe.template
  ... input = template.in
  ... output = ${buildout:parts-directory}/template
  ... ''')

Now we can run buildout::

  >>> print system(join('bin', 'buildout')),
  Uninstalling template.
  Installing template.

The template was indeed created::

  >>> cat('parts', 'template')
  #
  My template knows about buildout path:
  .../sample-buildout


Creating missing paths
======================

If an output file should be created in a path that does not yet exist,
then the missing items will be created for us::

  >>> write('buildout.cfg',
  ... '''
  ... [buildout]
  ... parts = template
  ... offline = true
  ...
  ... [template]
  ... recipe = collective.recipe.template
  ... input = template.in
  ... output = ${buildout:parts-directory}/etc/template
  ... ''')

  >>> print system(join('bin', 'buildout')),
  Uninstalling template.
  Installing template.

Also creation of several subdirectories is supported::


  >>> write('buildout.cfg',
  ... '''
  ... [buildout]
  ... parts = template
  ... offline = true
  ...
  ... [template]
  ... recipe = collective.recipe.template
  ... input = template.in
  ... output = ${buildout:parts-directory}/foo/bar/template
  ... ''')

  >>> print system(join('bin', 'buildout')),
  Uninstalling template.
  Installing template.

  >>> cat('parts', 'foo', 'bar', 'template')
  #
  My template knows about buildout path:
  .../sample-buildout

When changes happen to the output path, then the old path is removed
on uninstall. Therefore the ``etc/`` directory created above has
vanished now::

  >>> ls('parts')
  d  foo


Substituting variables with options of other parts
==================================================

When substituting variables in a template, dependencies on other buildout
parts can occur. Buildout will resolve them by determining the values of those
other parts' options first. To see this, we create a buildout involving a
template that uses a variable computed by a part that would not otherwise be
built:

  >>> write('dummy.py',
  ... '''
  ... class Recipe(object):
  ...
  ...     def __init__(self, buildout, name, options):
  ...         options['foo'] = 'bar'
  ...
  ...     def install(self):
  ...         return ()
  ...
  ...     def update(self):
  ...         pass
  ... ''')

  >>> write('setup.py',
  ... '''
  ... from setuptools import setup
  ...
  ... setup(name='dummyrecipe',
  ...       entry_points = {'zc.buildout': ['default = dummy:Recipe']})
  ... ''')

  >>> write('buildout.cfg',
  ... '''
  ... [buildout]
  ... develop = .
  ... parts = template
  ... offline = true
  ...
  ... [template]
  ... recipe = collective.recipe.template
  ... input = template.in
  ... output = template
  ...
  ... [other]
  ... recipe = dummyrecipe
  ... ''')

  >>> write('template.in',
  ... '''#
  ... My template knows about another buildout part:
  ... ${other:foo}
  ... ''')

  >>> print system(join('bin', 'buildout')),
  Develop: '/sample-buildout/.'
  Uninstalling template.
  Installing other.
  Installing template.

  >>> cat('template')
  #
  My template knows about another buildout part:
  bar
