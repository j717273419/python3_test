#At first ,use pip install pypyodbc make sure you have the package in you environment
import pypyodbc

# python3使用pypyodbc读取sql server 2012的数据
# python3 use pypyodbc read data from sql server 2012

connection_string = 'Driver={SQL Server Native Client 11.0};Server=.;Database=Test;Uid=sa;Pwd=123456;'
connection = pypyodbc.connect(connection_string)
print(connection.connected)
SQL = 'SELECT School_Id,School_Name FROM tb_School'

cur = connection.cursor()
result = cur.execute(SQL)

count = result.rowcount
print(count)

# 只读取一行
r = cur.fetchone()
print("return type:", type(r))
print("value:", r[1])

# 读取所有数据
print("fetchall:")
r = cur.fetchall()
for item in r:
    print(item, end='\n')

cur.close()
connection.close()
