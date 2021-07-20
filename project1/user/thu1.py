import json
b='07'
a='media/abc2021x'f'{b}''x17/data.json'
data=open(a, 'r')
data1=json.loads(data.read())
for d in data1:
    print(d['Date'])
c=5
# c=str(c)
print(type(c))
print(c)