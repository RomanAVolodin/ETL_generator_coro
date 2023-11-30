import time
import psycopg2

# dbname should be the same for the listening process
conn = psycopg2.connect(host="localhost", dbname="example", user="example", password="example")

cursor = conn.cursor()
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

while True:
    val = time.time()
    cursor.execute(f"NOTIFY match_updates, '{val}';")
    time.sleep(1)