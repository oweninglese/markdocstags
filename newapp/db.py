#! /usr/bin/python

import sqlite3
import os
import config

db = config.app['db']
ArticlesDir = config.app['ArticlesDir']
schema = config.app['schema']


def get_db_connection(db):
    """Get db conn.

    Args:
        db (docs.db): get row factory.

    Returns:
        sqlite3.Row(): return conn
    """
    conn = sqlite3.connect(str(db))
    conn.row_factory = sqlite3.Row
    return conn


def getnotes():
    """Get notes from db.

    Returns:
        list: current db contents
    """
    conn = get_db_connection(db)
    db_notes = conn.execute('SELECT * FROM docs').fetchall()
    conn.close()
    notes = []
    for note in db_notes:
        note = dict(note)
        note['content'] = str(note['content'][:-3]+'/index.html')
        notes.append(note)
    return notes


def update_db(notes):
    """_Update notes in db_.

    Args:
        notes (dict): close connection
    """
    connection = sqlite3.connect(db)
    with open(schema) as files:
        connection.executescript(files.read())
    cur = connection.cursor()
    for i in notes:
        cur.execute("INSERT INTO docs (content) VALUES (?)", (str(i),))
    connection.commit()
    connection.close()


def get_from_folder():
    """Get articles from folder.

    Returns:
        list: all .md ext
    """
    articles = [j for j in os.listdir(ArticlesDir) if j.endswith('.md')]
    return articles
