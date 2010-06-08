import zc.buildout
from collective.recipe.template import Recipe as Base


class Recipe(Base):
    def _execute(self):
        from genshi.template import Context, NewTextTemplate
        from genshi.template.eval import UndefinedError

        template = NewTextTemplate(self.source)
        context = Context(parts=self.buildout, options=self.options)
        try:
            self.result = template.generate(context).render()
        except UndefinedError, e:
            raise zc.buildout.UserError("Error in template %s:\n%s" % (self.input, e.msg))
