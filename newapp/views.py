import config
from flask import Flask
import jinja2
import sqlite3
import os
import markdown


app = Flask(__name__, template_folder='templates')
alph = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
buckets = [[i] for i in alph]
db = config.app['db']
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'),
                               autoescape=True)
ART_NAVI = {}
TAG_NAVI = {}


def buildnav(notes):
    nav = {}
    for j in buckets:
        for i in note_range:
            try:
                if nav[j[0]]:
                    if letter_in_dict(notes, i, j):
                        nav[j[0]] += [notes[i]['content']]
                    continue
                else:
                    nav[j[0]] = []
                    if letter_in_dict(notes, i, j):
                        nav[j[0]] += [notes[i]['content']]
                    continue
            except KeyError:
                nav[j[0]] = []
    return nav


def letter_in_dict(notes, i, j):
    if (notes[i]['content'])[0] == j[0]:
        return True


def get_db_connection(db):
    conn = sqlite3.connect(str(db))
    conn.row_factory = sqlite3.Row
    return conn


def getnotes():
    conn = get_db_connection(db)
    db_notes = conn.execute('SELECT * FROM docs').fetchall()
    conn.close()
    notes = []
    for note in db_notes:
        note = dict(note)
        note['content'] = str(note['content'][:-3]+'/index.html')
        notes.append(note)
    return notes


notes = getnotes()
note_range = range(len(notes))
nav = buildnav(notes)


def md_to_html(md):
    with open(os.path.abspath('docs') + '/' + md + '.md', 'r') as f:
        text = f.read()
        html = markdown.markdown(text)
    with open(os.path.abspath('static') + '/' + md + '/index.html', 'w') as f:
        f.write(html)
    return str(html)


def render_temp(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)


@app.route('/')
def index():
    return render_temp("articles.html", posts=notes, navi=nav)


@app.route('/static/<post>/index.html')
def article(post=None):
    if post is None:
        return render_temp("articles.html")
    else:
        html = md_to_html(post)
        lines = html.splitlines()
        return render_temp("article.html", posts=lines)


if __name__ == '__main__':
    app.run()
