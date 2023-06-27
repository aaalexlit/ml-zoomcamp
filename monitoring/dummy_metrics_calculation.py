import datetime
import time
import random
import logging
import uuid
import pytz
import pandas as pd
import io
import psycopg

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s]: %(message)s")

SEND_TIMEOUT = 10
rand = random.Random()

create_table_statement = """
drop table if exists dummy_metrics;
create table dummy_metrics(
	timestamp timestamptz,
	value1 integer,
	value2 varchar,
	value3 float
)
"""

dbname = "monitoring"


def prep_db():
    with psycopg.connect("host=localhost port=5432 user=postgres password=example", autocommit=True) as conn:
        res = conn.execute(
            f"SELECT 1 FROM pg_database WHERE datname='{dbname}'")
        if len(res.fetchall()) == 0:
            conn.execute("create database monitoring;")
        with psycopg.connect(f"host=localhost port=5432 dbname={dbname} user=postgres password=example") as conn:
            conn.execute(create_table_statement)


def calculate_dummy_metrics_postgresql(curr):
    value1 = rand.randint(0, 1000)
    value2 = str(uuid.uuid4())
    value3 = rand.random()

    insert_query = f"""insert into dummy_metrics(timestamp, value1, value2, value3) 
    values ('{datetime.datetime.now(pytz.timezone('Europe/Madrid'))}', {value1}, '{value2}',{value3})"""

    curr.execute(insert_query)


def main():
    prep_db()
    last_send = datetime.datetime.now()
    with psycopg.connect(f"host=localhost port=5432 dbname={dbname} user=postgres password=example", autocommit=True) as conn:
        for _ in range(10):
            with conn.cursor() as curr:
                calculate_dummy_metrics_postgresql(curr)

            new_send = datetime.datetime.now()
            seconds_elapsed = (new_send - last_send).total_seconds()
            if seconds_elapsed < SEND_TIMEOUT:
                time.sleep(SEND_TIMEOUT - seconds_elapsed)
            last_send = last_send + datetime.timedelta(seconds=10)
            logging.info("data sent")


if __name__ == '__main__':
    main()
