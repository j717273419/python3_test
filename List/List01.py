list1 = ['wdj','hello',1990,20]

print("list[0]:", list1[0])
print("List1:",list1[0:3])

list1[0] = 'world'

print(list1[0:4])

del list1[3]
print(list1[0:4])

print(len(list1))

tuple1 = ('a','b')
tuple2 = ('c','d')

list10 = [tuple1,tuple2]
print(list10)
for item in list10:
    for value in item:
        print(value)