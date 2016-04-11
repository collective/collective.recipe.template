import zc.buildout
from collective.recipe.template import Recipe as Base


class Recipe(Base):

    def _execute(self):
        from genshi.template import Context, NewTextTemplate
        from genshi.template.eval import UndefinedError

        template = NewTextTemplate(
            self.source,
            filepath=self.input, filename=self.input,
            encoding='utf-8')

        # Buildout seems not to "know" anything about decoding option values
        # into unicode - it actually seems to generally dislike non-ascii
        # values. We can do it here before handing it over to the template.
        decoded = {}
        for key, value in self.options.items():
            decoded[key] = value.decode('utf-8')

        context = Context(parts=self.buildout, options=decoded)
        try:
            self.result = template.generate(context).render(encoding='utf-8')
        except UndefinedError, e:
            raise zc.buildout.UserError(
                "Error in template %s:\n%s" % (self.input, e.msg))
