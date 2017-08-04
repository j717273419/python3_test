x = 50
def fun1():
    global x
    x = 10
    print("x value is {0}".format(x))
fun1()
print("x value still {0}".format(x))