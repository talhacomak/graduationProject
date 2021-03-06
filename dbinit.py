import os
import sys
from configurations import db_url
import psycopg2 as dbapi2


INIT_STATEMENTS = [
"CREATE TABLE IF NOT EXISTS USERS(ID SERIAL PRIMARY KEY, USERNAME VARCHAR(255), PASSWORD VARCHAR(255), MAIL VARCHAR(255), ISADMIN BOOL DEFAULT FALSE)",
"CREATE TABLE IF NOT EXISTS MUSICS(ID SERIAL PRIMARY KEY, SONG VARCHAR(255), GENRE VARCHAR(255), SCORE INTEGER)",
]

def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()


if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    initialize(db_url)
