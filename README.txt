Introduction
============

This recipe can be used to generate textfiles from a (text) template.

A short example::

  [buildout]
  parts = zope.conf

  [message]
  recipe = collective.recipe.template
  input = templates/message.in
  output = /message

  mymessage = Hello, World!


In the template you can use the exact same variables as you can use
in the buildout configuration. For example an input file can look like this::

  My top level directory is ${buildout:directory}
  Executables are stored in ${buildout:bin-directory}


As an extension to the buildout syntax you can reference variables from
the current buildout part directly. For example::

  My message is: ${mymessage}


Why another template recipe?
----------------------------

Both `iw.recipe.template`_ and `inquant.recipe.textfile`_ claim to do the
same thing. I have found them to be undocumented and too buggy for real
world use, and neither are in a public repository where I could fix them. In
addition this implementation leverages the buildout variable substitution
code, making it a lot simpler.



