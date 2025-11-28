# 읽을 줄 없을 때까지 읽기

f = open('data.txt', encoding='utf-8')
data = f.readlines()
print(data)
f.close()
for line in data:
    print(line.rstrip())
f.close()