import sqlite3

from flask import Flask, render_template,flash, jsonify, g,request
from random import sample
app= Flask(__name__)
DATABASE = 'inginious.sqlite'

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    db.row_factory = make_dicts
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


with app.app_context():
    cur = get_db().cursor()

@app.route('/')
def index3():
    return render_template('testinggraphs.html')

@app.route('/difftasks')
def difftasks():
    return jsonify({'difftasks': query_db(
        "SELECT task as lbl, count(*) as val from user_tasks group by task order by count(*) desc limit 10 "
    )})

@app.route('/sql')
def results():
    return jsonify({'results': query_db(
        "SELECT count(succeeded) as val,course as lbl from user_tasks where succeeded='true' GROUP BY succeeded,course"
    )})

@app.route('/sql1')
def results1():
    return jsonify({'results1': query_db(
        "SELECT count(succeeded) as val,course as lbl from user_tasks where succeeded='false' GROUP BY succeeded,course"
    )})

@app.route('/percent')
def percent():
    return jsonify({'percent': query_db(
        "select task, count(*) as val from user_tasks  where task in (" + request.args.get('tasks', '') + ") and succeeded='true' group by task order by 2 DESC;"
    )})

@app.route('/try')
def avgtries():
    return jsonify({'avgtries': query_db(
        'select avg(tried) as val, task as lbl from user_tasks group by task order by avg(tried) desc limit 50'
    )})

if __name__ == "__main__":
    app.run(debug=True)
    