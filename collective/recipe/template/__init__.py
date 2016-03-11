import logging
import os
import re
import stat
import sys
import urllib2
import zc.buildout


TRUE_VALUES = ('y', 'yes', '1', 'true')


class Recipe:
    def __init__(self, buildout, name, options):
        self.buildout=buildout
        self.name=name
        self.options=options
        self.logger=logging.getLogger(self.name)
        self.msg = None

        if "input" not in options and "inline" not in options and "url" not in options:
            self.logger.error("No input file, inline template, or URL specified.")
            raise zc.buildout.UserError("No input file, inline template, or URL specified.")

        if "output" not in options:
            self.logger.error("No output file specified.")
            raise zc.buildout.UserError("No output file specified.")

        if ("input" in options and "inline" in options or
            "input" in options and "url" in options):
            self.logger.error("Too many input sources.")
            raise zc.buildout.UserError("Too many input sources.")

        self.output=options["output"]
        self.input=options.get("input")
        self.input_encoding=options.get("input-encoding", "utf-8")
        self.output_encoding=options.get("output-encoding", "utf-8")
        self.inline=options.get("inline")
        self.url = options.get("url")
        self.timeout = float(options.get("timeout", 1.0))
        self.overwrite = options.get("overwrite", 'true').lower() in TRUE_VALUES
        if "inline" in options:
            self.source = self.inline.lstrip()
            self.mode = None
        elif "input" in options and os.path.exists(self.input):
            with open(self.input, 'rb') as f:
                self.source = f.read().decode(self.input_encoding)
            self.mode=stat.S_IMODE(os.stat(self.input).st_mode)
        elif "input" in options and self.input.startswith('inline:'):
            self.source=self.input[len('inline:'):].lstrip()
            self.mode=None
        elif "url" in options and self._checkurl():
            self.source = self.url.read().decode(self.input_encoding)
            self.mode=None
        else:
            # If the error is not from urllib2
            if self.url == None:
                msg="Input file '%s' does not exist." % self.input
            else:
                msg = self.msg
            self.logger.error(msg)
            raise zc.buildout.UserError(msg)

        self._execute()

        if "mode" in options:
            self.mode=int(options["mode"], 8)


    def _execute(self):
        template = self.source
        if sys.version_info < (3,):
            template = template.encode('utf-8')
        template = re.sub(r"\$\{([^:]+?)\}", r"${%s:\1}" % self.name, template)
        self.result = self.options._sub(template, [])
        if sys.version_info < (3,):
            self.result = self.result.decode('utf-8')

    def _checkurl(self):
        try:
            self.url = urllib2.urlopen(self.url, timeout=self.timeout)
        except urllib2.HTTPError, error:
            self.msg = error
            return False
        except urllib2.URLError, error:
            self.msg = error
            return False
        except ValueError, error:
            self.msg = error
            return False
        return True

    def install(self):
        if not self.overwrite and os.path.isfile(self.output):
            return self.options.created()

        self.createIntermediatePaths(os.path.dirname(self.output))
        try:
            os.remove(self.output)
        except OSError:
            pass
        with open(self.output, "wb") as output:
            output.write(self.result.encode(self.output_encoding))

        if self.mode is not None:
            os.chmod(self.output, self.mode)

        if self.overwrite:
            # prevents deleting after execute buildout after modifying buildout.cfg
            self.options.created(self.output)

        return self.options.created()


    def update(self):
        # Variables in other parts might have changed so we may need to do a
        # full reinstall.
        try:
            with open(self.output, "rb") as f:
                output = f.read()
        except IOError:
            result_changed = True
        else:
            result_changed = output != self.result.encode(self.output_encoding)

        if result_changed:
            # Output has changed, re-write output file
            return self.install()


    def createIntermediatePaths(self, path):
        parent = os.path.dirname(path)
        if os.path.exists(path) or parent == path:
            return
        self.createIntermediatePaths(parent)
        os.mkdir(path)
        self.options.created(path)
