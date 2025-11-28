def show(m):
    if m == 1:
        text='let it go'
    elif m == 2:
        text='let it be'

    f = open(text + '.txt', encoding='utf-8')
    data = f.read()
    print(data)
    f.close()

print('1. let if go')
print('2. let it be')

while True:
    menu = int(input('선곡(종료: 0): '))
    if menu == 0:
        break
    show(menu)