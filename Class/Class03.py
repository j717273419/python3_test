__author__  = "wdj"

class Hello:
    def __init__(self):
        print("Hello Python")
    def SayHello(self):
        print("Hello")
# c = Hello();
# c.SayHello();


class World(Hello):
    def __init__(self):
        print("World")


d = World();
d.SayHello();




