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
  ... recipe = collective.recipe.template[genshi]:genshi
  ... input = template.in
  ... output = template
  ... some-option = value
  ... ''')

We create a template file::

  >>> write('template.in',
  ... '''#
  ... My template knows about buildout path:
  ...   ${parts.buildout.directory}
  ... You can also write bash/zsh variable expansions by doubling the dollar
  ... sign like this: $${SOME_VARIABLE}
  ... To access options with a dash, use dictionary access:
  ...   ${parts.buildout['bin-directory']}
  ... To access the current part, use ``options``:
  ...   ${options['some-option']}
  ... ''')

Now we can run buildout::

  >>> print system(join('bin', 'buildout')),
  Installing template.

The template was indeed created::

  >>> cat('template')
  #
  My template knows about buildout path:
  .../sample-buildout
  You can also write bash/zsh variable expansions by doubling the dollar
  sign like this: ${SOME_VARIABLE}
  To access options with a dash, use dictionary access:
  .../sample-buildout/bin
  To access the current part, use ``options``:
    value

The variable ``buildout:directory`` was also substituted by a path.
