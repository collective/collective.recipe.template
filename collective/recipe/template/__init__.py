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

        if "input" not in options and "inline" not in options:
            self.logger.error("No input file or inline template specified.")
            raise zc.buildout.UserError("No input file specified.")

        if "output" not in options:
            self.logger.error("No output file specified.")
            raise zc.buildout.UserError("No output file specified.")

        self.output=options["output"]
        self.input=options.get("input")
        self.inline=options.get("inline")
        if "inline" in options:
            self.source = self.inline.lstrip()
            self.mode = None
        elif os.path.exists(self.input):
            self.source=open(self.input).read()
            self.mode=stat.S_IMODE(os.stat(self.input).st_mode)
        elif self.input.startswith('inline:'):
            self.source=self.input[len('inline:'):].lstrip()
            self.mode=None
        else:
            msg="Input file '%s' does not exist." % self.input 
            self.logger.error(msg) 
            raise zc.buildout.UserError(msg)

        self._execute()

        if "mode" in options:
            self.mode=int(options["mode"], 8)


    def _execute(self):
        template=re.sub(r"\$\{([^:]+?)\}", r"${%s:\1}" % self.name, self.source)
        self.result=self.options._sub(template, [])


    def install(self):
        self.createIntermediatePaths(os.path.dirname(self.output))
        output=open(self.output, "wt")
        output.write(self.result)
        output.close()

        if self.mode is not None:
            os.chmod(self.output, self.mode)

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
