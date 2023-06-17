def coro():
    print('Начало работы корутины')
    val = (yield)
    print(f'В корутину пришло значение: {val}')
    yield val * 2
    print('Завершение работы корутины')

