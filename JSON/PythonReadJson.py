import json

# python 字典类型转换为JSON对象
data = {
    'no' : 1,
    'name' : 'ps',
    'url' : 'python.org'
}

json_str = json.dumps(data);
print("Python原始数据为：",data)
print("JSON对象为：",json_str)

#将JSON对象转换为Python Dict

data2 = json.loads(json_str)
print("从JSON转换到Python Dict的值为：",data2)
print("data2['name']",data2["name"])
print("data2['url']",data2["url"])