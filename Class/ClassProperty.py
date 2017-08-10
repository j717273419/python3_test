class person(object):
    def __init__(self,name,age):
        self.Name = name
        self.Age = age

if __name__ == "__main__":
        p = person('xiaoming',28)
        #自由属性并不会报错
        p.ID = 7


class animal(object):
    __slots__=('Name','Age')
    def __init__(self,name,age):
        self.Name = name
        self.Age = age

if __name__ == "__main__":
    a = animal("dog",2)
    #AttributeError: 'animal' object has no attribute 'Id'
    a.Id = 7