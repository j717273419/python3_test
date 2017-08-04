def param2(init,**params):
    print(init)
    for item in params:
        print(params[item])
'''
**p 这种用法是接收不定长的字典参数，调用时要设置一个key，类似hello(a=1,b=2).不然会报错
'''
param2(1,a=2,b=3,c=7)