# 파일의 내용을 읽어서 출력하기

f = open('name.txt', encoding='utf-8')
data = f.read()
print(data)
f.close()