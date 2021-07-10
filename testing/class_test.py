class Hello:
    def __init__(self):
        self.name = self.__class__.__name__

    def print_hello(self):
        print('Class method', self.name)

    @staticmethod
    def print_hello_static(name):
        print('static method', name)


class World(Hello):

    def __init__(self):
        super().__init__()
        self.name = self.__class__.__name__


    def world(self):
        super().print_hello()

    def world_self(self):
        super().print_hello_static(self.name)

w = World()

w.world_self()
