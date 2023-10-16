
def coro():
    print('Начало работы корутины')
    val = (yield)
    print(f'В корутину пришло значение: {val}')
    yield val * 2
    print('Завершение работы корутины')



if __name__ == '__main__':
    print(sum(0, 1))

    print("Конец программы")


