# 파일의 내용 한 줄을 읽어서 출력하기
# print문의 끝에 enter를 붙이지 않음

f = open('name.txt', encoding='utf-8')
data = f.readline()
print(data, end='')
f.close()

print('\n')

# 읽을 것이 없을 때까지 한 줄 읽기
f2 = open('name.txt', encoding='utf-8')
while True:
    data = f2.readline()
    if data == '':
        break
    print(data, end='')
f.close()