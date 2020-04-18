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

@app.route('/sql')
def results():
    return jsonify({'results': query_db(
        "SELECT count(result) as val,course as lbl from submissions WHERE result='failed' GROUP BY course"
    )})

@app.route('/try')
def avgtries():
    return jsonify({'avgtries': query_db(
        'select avg(tried) as val, task as lbl from user_tasks group by task'
    )})

@app.route('/button',methods=['GET'])
def dropdown():
    colours = ['Red','Orange','Blue']
    return render_template('testinggraphs.html',colours=colours)

if __name__ == "__main__":
    app.run(debug=True)
    