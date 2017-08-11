tuple = ("a","b",3,4)
for item in tuple:
    print(item,end=",")
print("tuple length is ",len(tuple))
print("first item is {0},{0}".format(tuple[0]))

tuple2 = ('elephant','monkey',tuple)
print(len(tuple2))
print("the right value is 4,and the answer is ",tuple2[2][3])

