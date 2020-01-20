import datetime
import json
import os

import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, jsonify, render_template, request

conn = psycopg2.connect(host='localhost', dbname='db', user='postgres', password='postgres')

app = Flask(__name__)
app.secret_key=os.urandom(24)

@app.route('/', methods=['GET'])
def main():
    return render_template('index.html')


@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.get_json()
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute('SELECT EXISTS (SELECT * FROM Users WHERE username=%s);', (data['username'],))
        d = cur.fetchone()
        # print(d)
        if d['exists']:
            return jsonify({'exists':1}) # Username in use
        cur.execute('SELECT create_user(%s, %s, %s, %s, %s, %s, %s, %s)',
                (data['first_name'], data['last_name'], data['username'],
                    data['password'], data['email'], data['skype'],
                    data['is_teacher'], data['grade_level']))
        conn.commit()
        return jsonify({'exists':0})

@app.route('/create_worksheet', methods=['POST'])
def create_worksheet():
    data = request.get_json()
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute('SELECT create_worksheet(%s, %s, %s, %s)',
                (data['creator_id'], data['grade_level'],
                    data['category'], data['content']))
        conn.commit()
    return ''

@app.route('/data', methods=['GET'])
def data():
    queries = [
        'SELECT * FROM Users;',
        'SELECT * FROM Users WHERE skype_address is NULL;',
        'SELECT username, language FROM Users NATURAL JOIN Languages WHERE language=\'en\';',
        'SELECT COUNT(*) FROM TeacherAvailability WHERE start_time <= TIME \'12:00:00\' AND end_time >= TIME \'3:00:00\';',
        'SELECT first_name, last_name FROM Users JOIN Teachers ON user_id = teacher_id JOIN Students ON teacher_id = student_id JOIN GradeLevel ON students.grade_level_id = GradeLevel.grade_level_id WHERE GradeLevel.name = \'9\' OR GradeLevel.name = \'10\' OR GradeLevel.name = \'11\' OR GradeLevel.name = \'12\';',
        'SELECT first_name, last_name, skype_address FROM Users JOIN Teachers ON user_id = teacher_id WHERE skype_address IS NOT NULL;',
        'SELECT first_name, last_name FROM Users WHERE user_id = (SELECT student_id FROM Students WHERE student_id = (SELECT DISTINCT student_id FROM Submitted WHERE submission_id = (SELECT submission_id FROM Returned WHERE grade > 89))) ORDER BY last_name;'
        ] # Put queries here
    data = []
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        for q in queries:
            cur.execute(q)
            d = cur.fetchall()
            # print(d)
            data.append((q,[json.dumps(i, default=dtconv) for i in d]))
    return render_template('data.html', data=data)

def dtconv(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
