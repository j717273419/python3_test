import re
r = re.findall("\d","abc123")
print(r)

r2 = re.findall("\d+","abc123")
print(r2)


r3 = re.findall("\d+","abc123efgg987")
print(r3)

r4 = re.findall("\w[^d]","abc=123efgg987")
print(r4)
