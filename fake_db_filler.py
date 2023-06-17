import psycopg
from faker import Faker
from progress.bar import FillingCirclesBar

from settings import database_settings

fake = Faker()


def fill_source_database(amount_of_records: int = 1000, batch_size: int = 100) -> None:
    iterations = amount_of_records // batch_size
    bar = FillingCirclesBar('Заполнение исходной БД', max=iterations)

    with psycopg.connect(**database_settings.dict()) as conn, conn.cursor() as cur:
        for _ in range(iterations):
            batch = []
            for _ in range(batch_size):
                batch.append((fake.name(), fake.text()))
            cur.executemany('insert into movies (title, description) values (%s, %s)', batch)
            bar.next()
    # the connection is now closed

    bar.finish()


