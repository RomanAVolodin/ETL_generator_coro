
def coro():
    print('Начало работы корутины')
    val = yield
    print(f'В корутину пришло значение: {val}')
    yield val * 2
    print('Завершение работы корутины')


if __name__ == '__main__':
    c = coro()
    next(c)  # c.send(None) - одно и тоже

    c.send(5)  # next(c) - тоже, что и c.send(None)

    next(c)


