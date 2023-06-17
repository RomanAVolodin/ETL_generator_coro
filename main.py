from dataclasses import astuple
from datetime import datetime
from time import sleep
from typing import Coroutine, Generator

import psycopg
from psycopg import ServerCursor
from psycopg.conninfo import make_conninfo
from psycopg.rows import dict_row

from decorators import coroutine
from fake_db_filler import fill_source_database
from logger import logger
from settings import database_settings
from state.json_file_storage import JsonFileStorage
from state.models import State, Movie


STATE_KEY = 'last_movies_updated'


@coroutine
def fetch_changed_movies(cursor, next_node: Generator) -> Generator[datetime, None, None]:
    while last_updated := (yield):
        logger.info(f'Fetching movies changed after ' f'{last_updated}')
        sql = 'SELECT * FROM movies WHERE updated_at > %s order by updated_at asc'
        logger.info('Fetching movies updated after %s', last_updated)
        cursor.execute(sql, (last_updated,))
        while results := cursor.fetchmany(size=100):
            next_node.send(results)


@coroutine
def transform_movies(next_node: Generator) -> Generator[list[dict], None, None]:
    while movie_dicts := (yield):
        batch = []
        for movie_dict in movie_dicts:
            movie = Movie(**movie_dict)
            movie.title = movie.title.upper()
            logger.info(movie.json())
            batch.append(movie)
        next_node.send(batch)


@coroutine
def save_movies(state: State) -> Generator[list[Movie], None, None]:
    while movies := (yield):
        logger.info(f'Received for saving {len(movies)} movies')
        print([movie.json() for movie in movies])
        state.set_state(STATE_KEY, str(movies[-1].updated_at))


if __name__ == '__main__':
    # fill_source_database(100)

    state = State(JsonFileStorage(logger=logger))

    dsn = make_conninfo(**database_settings.dict())
    print(dsn)

    with psycopg.connect(dsn, row_factory=dict_row) as conn, ServerCursor(conn, 'fetcher') as cur:
        # Closing a server-side cursor is more important than closing a client-side one
        # because it also releases the resources on the server, which otherwise might remain allocated
        # until the end of the session (memory, locks). Using the pattern: with conn.cursor():
        saver_coro = save_movies(state)
        transformer_coro = transform_movies(next_node=saver_coro)
        fetcher_coro = fetch_changed_movies(cur, transformer_coro)

        while True:
            last_movies_updated = state.get_state(STATE_KEY)
            logger.info('Starting ETL process for updates ...')

            fetcher_coro.send(state.get_state(STATE_KEY) or str(datetime.min))

            sleep(15)
