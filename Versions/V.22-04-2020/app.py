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
    return render_template('testinggraphs1.html')

#graph 1
@app.route('/difftasks')
def difftasks():
    return jsonify({'difftasks': query_db(
        "SELECT task as lbl, count(*) as val from user_tasks group by task order by count(*) desc limit 10 "
    )})

#graph 2
@app.route('/sql')
def results():
    return jsonify({'results': query_db(
        "SELECT count(succeeded) as val,course as lbl from user_tasks where succeeded='true' GROUP BY succeeded,course"
    )})

#graph 2 
@app.route('/sql1')
def results1():
    return jsonify({'results1': query_db(
        "SELECT count(succeeded) as val,course as lbl from user_tasks where succeeded='false' GROUP BY succeeded,course"
    )})

#graph 1 top 10 most tried exercises and how many succeed them
@app.route('/percent')
def percent():
    return jsonify({'percent': query_db(
        "select task, count(*) as val from user_tasks  where task in (" + request.args.get('tasks', '') + ") and succeeded='true' group by task order by 2 DESC;"
    )})

#graph 3 avg number of tries for most tried exercises
@app.route('/try')
def avgtries():
    return jsonify({'avgtries': query_db(
        'select avg(tried) as val, task as lbl from user_tasks group by task order by avg(tried) desc limit 30'
    )})

#submenu LSINF1101-PYTHON 
@app.route('/topten1')
def top10_LSINF1101():
    return jsonify({'topten1': query_db(
        'SELECT task as lbl from user_tasks where course="LSINF1101-PYTHON" group by task order by count(*) desc limit 10'
    )})

#submenu LSINF1252
@app.route('/topten2')
def top10_LSINF1252():
    return jsonify({'topten2': query_db(
        'SELECT id,task as lbl from user_tasks where course="LSINF1252" group by task order by count(*) desc limit 10'
    )})

#submenu LEPL1402
@app.route('/topten3')
def top10_LEPL1402():
    return jsonify({'topten3': query_db(
        'SELECT id,task as lbl from user_tasks where course="LEPL1402" group by task order by count(*) desc limit 10'
    )})

#exercise_graph1
@app.route('/time_late/<task>')
def timel(task=None):

    x = 'SELECT substr(submitted_on,12,2) as lbl,count(*) as val FROM submissions where task="'+task+'" group by lbl'
    print(x)
    return jsonify({'timel': query_db(x)})


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
    