with open('test.txt', mode='r') as file:
    data = file.readlines()

with open('test2.txt', mode='r') as file:
    data1 = file.readlines()

print(len(data))
print(len(data1))

for d in data:
    if d not in data1:
        print(d)