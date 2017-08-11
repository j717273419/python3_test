ab = {'Swaroop' : "swaroop@swaroopch.com",
      'Larry' : 'larry@wall.org'}
print("swaroop's address is ",ab["Swaroop"])
ab["wdj"] = "admin@wangdongjie.com"
for a,b in ab.items():
    print(a,' ',b)
del ab["wdj"]
print("dictionary length is {0}".format(len(ab)))

if "wdj" in ab:
    print("wdj is int ab,it's value is ",ab["wdj"])
ab["wdj"] = "admin@wangdongjie.com"

if "wdj" in ab:
    print("wdj is int ab,haha, ",ab["wdj"])