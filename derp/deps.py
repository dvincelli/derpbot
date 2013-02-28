
class Container(object):

    components = {}

    @classmethod
    def register(cls, name, instance):
        cls.components[name] = instance

    @classmethod
    def get(cls, name):
        return cls.components[name]

class Inject(object):

    container = Container

    def __init__(self, want):
        self.want = want

    def __get__(self, obj, objtype):
        return Container.get(self.want)

