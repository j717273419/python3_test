#At first ,use pip install pypyodbc make sure you have the package in you environment
import pypyodbc

# python3使用pypyodbc插入sql server 2012的数据
# python3 use pypyodbc insert data into sql server 2012

connection_string = 'Driver={SQL Server Native Client 11.0};Server=.;Database=Test;Uid=sa;Pwd=123456;'
connection = pypyodbc.connect(connection_string)
print(connection.connected)
SQL = "insert into tb_School(School_Name) VALUES('{0}')".format("TsingHua")

cur = connection.cursor()
result = cur.execute(SQL)
cur.commit()

sql_read = "select * from tb_School"

cur.execute(sql_read)


# 读取所有数据
print("fetchall:")
r = cur.fetchall()
for item in r:
    print(item)


cur.close()

connection.close()
