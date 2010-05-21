from collective.recipe.template import Recipe as Base
from genshi.template import Context, NewTextTemplate
from genshi.template.base import deque


class MyContext(Context):
    def __init__(self, *args):
        self.frames = deque(args)
        self.pop = self.frames.popleft
        self.push = self.frames.appendleft


class Recipe(Base):
    def _execute(self):
        template = NewTextTemplate(self.source)
        self.result = template.generate(MyContext(self.buildout)).render()
