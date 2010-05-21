Introduction
************

This recipe can be used to generate textfiles from a (text)
template.

.. contents::

Starting with version 1.3 you can also specify a path to the output
file and the path will be created, if it does not exist.

A short example::

  [buildout]
  parts = message

  [message]
  recipe = collective.recipe.template
  input = templates/message.in
  output = ${buildout:parts-directory}/etc/message

  mymessage = Hello, World!


In the template you can use the exact same variables as you can use
in the buildout configuration. For example an input file can look like this::

  My top level directory is ${buildout:directory}
  Executables are stored in ${buildout:bin-directory}


As an extension to the buildout syntax you can reference variables from
the current buildout part directly. For example::

  My message is: ${mymessage}


Genshi text templates
=====================

Starting with version 1.7 you can use `genshi text templates`_.

A short example::

  [buildout]
  parts = message

  [message]
  recipe = collective.recipe.template[genshi]:genshi
  input = templates/message.in
  output = ${buildout:parts-directory}/etc/message

  mymessage = Hello, World!

In the template you can use the exact same variables as you can use
in the buildout configuration, but you have to use dots instead of colons
as the separator. For example an input file can look like this::

  My top level directory is ${buildout.directory}
  Executables are stored in ${buildout.bin-directory}


Why another template recipe?
============================

Both `iw.recipe.template`_ and `inquant.recipe.textfile`_ claim to do the
same thing. I have found them to be undocumented and too buggy for real
world use, and neither are in a public repository where I could fix them. In
addition this implementation leverages the buildout variable substitution
code, making it a lot simpler.


.. _genshi text templates: http://genshi.edgewall.org/wiki/Documentation/text-templates.html
.. _iw.recipe.template: http://pypi.python.org/pypi/iw.recipe.template
.. _inquant.recipe.textfile: http://pypi.python.org/pypi/inquant.recipe.textfile
