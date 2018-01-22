import zc.buildout
from collective.recipe.template import Recipe as Base


class Recipe(Base):

    def _execute(self):
        from genshi.template import Context, NewTextTemplate
        from genshi.template.eval import UndefinedError

        template = NewTextTemplate(
            self.source,
            filepath=self.input, filename=self.input)
        context = Context(parts=self.buildout, options=self.options)
        try:
            self.result = template.generate(
                context).render(encoding='utf-8').decode('utf-8')
        except UndefinedError, e:
            raise zc.buildout.UserError(
                "Error in template {}:\{}".format(self.input, e.msg))
