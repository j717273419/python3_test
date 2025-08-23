# python padding and filling of strings

str = "Hello"
print("左对齐，填充字符" + str.ljust(10, '*'))  # 左对齐，填充字符为 '*'
print("右对齐，填充字符" + str.rjust(10, '*'))  # 右对齐，填充字符为 '*'
print("居中对齐，填充字符" + str.center(10, '*'))
