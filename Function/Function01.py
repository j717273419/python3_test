def test():
    print 'hello,function'

test()

def test(a):
    print a
test('hehe')

def test2():
    return 1
result = test2();
print result


def test3():
    return 1,2,3
print test3()
print type(test3())

def test4():
    return [1,2,3]
print test4()
print type(test4())
