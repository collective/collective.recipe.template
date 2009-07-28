import logging
import os
import re
import stat
import zc.buildout

class Recipe:
    def __init__(self, buildout, name, options):
        self.buildout=buildout
        self.name=name
        self.options=options
        self.logger=logging.getLogger(self.name)

        if "input" not in options:
            self.logger.error("No input file specified.")
            raise zc.buildout.UserError("No input file specified.")

        if "output" not in options:
            self.logger.error("No output file specified.")
            raise zc.buildout.UserError("No output file specified.")


        self.input=options["input"]
        if not os.path.exists(self.input):
            msg="Input file '%s' does not exist." % self.input
            self.logger.error(msg)
            raise zc.buildout.UserError(msg)

        self.output=options["output"]

        source=open(self.input).read()
        template=re.sub(r"\$\{([^:]+?)\}", r"${%s:\1}" % name, source)
        self.result=options._sub(template, [])


    def install(self):
        mode=stat.S_IMODE(os.stat(self.input).st_mode)

        self.createIntermediatePaths(os.path.dirname(self.output))
        output=open(self.output, "wt")
        output.write(self.result)
        output.close()

        os.chmod(self.output, mode)

        self.options.created(self.output)
        return self.options.created()


    def update(self):
        # Variables in other parts might have changed so we need to do a
        # full reinstall.
        return self.install()


    def createIntermediatePaths(self, path):
        parent = os.path.dirname(path)
        if os.path.exists(path) or parent == path:
            return
        self.createIntermediatePaths(parent)
        os.mkdir(path)
        self.options.created(path)
