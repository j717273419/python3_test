
class FooParent(object):
    def __init__(self):
        self.parent='I\'am the parent.'
        print('Parent')
    def bar(self,message):
        print (message,'from parent')

class FooChild(FooParent):
    def __init__(self):
        FooParent.__init__(self)
        print('child')
    def bar(self,message):
        FooParent.bar(self,message)
        print ('Child bar function')
        print (self.parent)


if __name__=='__main__':
    fooChild=FooChild()
    fooChild.bar('Hello World')


