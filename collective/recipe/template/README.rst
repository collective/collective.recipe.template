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

Overriding output file
======================

By default re-execute buildout, makes that output file is overwrited, by new
output file. But, if you want generate this file ONLY when it doesn't exist,
you can use overwrite option:

Once again check output file content::

  >>> cat('template')
  #
  My template knows about buildout path:
  .../sample-buildout

Let's change this file::
  >>> print system("sed 's/sample-buildout/spam-ham-eggs/g' template > out && mv out template")
  <BLANKLINE>

Let's check content now::

  >>> cat('template')
  #
  My template knows about buildout path:
  .../spam-ham-eggs

Now try re-execute buildout, and then check our file again::

  >>> print system(join('bin', 'buildout')),
  Updating template.

  >>> cat('template')
  #
  My template knows about buildout path:
  .../sample-buildout

Like you see, re-execute buildout, caused overwrite ourmodified file. Let's try
to prevent this behavior. So we must modify buildout.cfg, re-execute buildout,
and then modify again output file::

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
  ... overwrite = False
  ... ''')

  >>> print system(join('bin', 'buildout')),
  Uninstalling template.
  Installing template.

  >>> cat('template')
  #
  My template knows about buildout path:
  .../sample-buildout

  >>> print system("sed 's/sample-buildout/spam-ham-eggs/g' template > out && mv out template")
  <BLANKLINE>

  >>> cat('template')
  #
  My template knows about buildout path:
  .../spam-ham-eggs

Let's check output file again - it shouldn't be modyfied this time::

  >>> print system(join('bin', 'buildout')),
  Updating template.

  >>> cat('template')
  #
  My template knows about buildout path:
  .../spam-ham-eggs

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

Using URL input
===============

.. Warning:: There is a security risk inherent with using URL input.
    Please be careful.

Similarly, you may want to read input from a URL, e.g.::

  >>> write('buildout.cfg',
  ... '''
  ... [buildout]
  ... parts = template
  ...
  ... [template]
  ... recipe = collective.recipe.template
  ... url = file:///tmp/template.in
  ... output = template
  ... ''')

To demonstrate this, first we create a template file::

  >>> write('/tmp/template.in',
  ... '''#
  ... My template knows about buildout path:
  ...   ${buildout:directory}
  ... ''')

Now we can run buildout::

  >>> print system(join('bin', 'buildout')),
  Uninstalling template.
  Installing template.
  ...

The template should have been created::

  >>> cat('template')
  #
  My template knows about buildout path:
  .../sample-buildout

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
