import zc.buildout
import sys
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
                context).render(encoding='utf-8')
        except UndefinedError, e:
            raise zc.buildout.UserError(
                "Error in template {}:\{}".format(self.input, e.msg))
        if sys.version_info > (3,):
            self.result = self.result.decode('utf-8')
