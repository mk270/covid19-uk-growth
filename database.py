from sqlite3 import dbapi2 as sqlite
import sqlite3
import sys
import datetime
import logging

DB = 'cached.db'
SQL = """INSERT INTO cases_log (day, cases, tested) VALUES (?, ?, ?);"""

def save_update(day_formatted, count, tested):
    db = sqlite.connect(DB)
    try:
        with db:
            db.execute(SQL, (day_formatted, count, tested))
    except sqlite3.IntegrityError:
        logging.warn("Couldn't update DB")
        logging.warn("This may be because today's data is not yet available")
        sys.exit(1)

def already_done_today(today):
    db = sqlite.connect(DB)
    sql = """SELECT day from cases_log WHERE day = ?;"""
    with db:
        results = db.execute(sql, (today,))
        rowcount = len(results.fetchall())
        return rowcount > 0
