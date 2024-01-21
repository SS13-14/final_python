from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine, text
# from flask_cors import CORS
import random
import sqlite3

app = Flask(__name__)
# CORS(app)
engine = create_engine("mysql+mysqlconnector://root:1234@localhost/ss13.14_pos")
connection = engine.connect()

BASE_URL = 'http://127.0.0.1:5000'
app.secret_key = 'your_secret_key'


@app.context_processor
def utility_processor():
    def getBaseUrl():
        return 'http://127.0.0.1:5000'

    def getImagePath():
        return 'http://127.0.0.1:5000/'

    return dict(
        getBaseUrl=getBaseUrl,
        getImagePath=getImagePath
    )


import routes

import routes


@app.route('/')
def web():
    result = connection.execute(text("SELECT * FROM product"))
    return render_template('product_card.html', products=result)


@app.route('/detail/<string:id>')
def detail(id):
    return render_template('product_detail.html', id=id)


@app.route('/admin')
def admin():
    return render_template('admin/dashboard/index.html', module='dashboard')


@app.route('/admin/student')
def indexStudent():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from students")
    rows = cur.fetchall()
    return render_template('admin/student/index.html',
                           module='student',
                           BASE_URL=BASE_URL,
                           rows=rows)


@app.route('/admin/add_student')
def addStudent():
    return render_template('admin/student/add.html')


@app.route('/admin/add_new_student', methods=['POST'])
def insertStudent():
    conn = None
    try:
        name = request.form['name']
        if request.form['gender'] == 'male':
            gender = 'M'
        else:
            gender = 'F'
        address = request.form['address']
        dob = request.form['dob']
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        pob = request.form['pob']

        insert_query = "INSERT INTO students (name, gender, address, DateOfBirth,PlaceOfBirth) VALUES (?, ?, ?, ?,?)"
        cursor.execute(insert_query, (name, gender, address, dob, pob))
        conn.commit()
        flash("Student added successfully", "success")
    finally:
        if conn is not None:
            conn.close()
    return redirect(url_for('indexStudent'))


@app.route('/admin/edit_student/<string:name>')
def editStudent(name):
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(f"select * from students WHERE name='{name}'")
    rows = cur.fetchall()
    return render_template('admin/student/edit.html', row=rows)


@app.route('/admin/update_student/<int:id>', methods=['POST'])
def updateStudent(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    try:
        # Get the data from the form
        name = request.form['name']
        gender = request.form['gender']
        address = request.form['address']
        dob = request.form['dob']
        pob = request.form['pob']

        # Update the student information in the database
        update_query = "UPDATE students SET name = ?, gender = ?, address = ?, DateOfBirth = ?, PlaceOfBirth = ? WHERE id = ?"
        cursor.execute(update_query, (name, gender, address, dob, pob, id))
        conn.commit()

        flash('Student information updated successfully', 'success')  # Flash success message
    except Exception as e:
        conn.rollback()
        flash('An error occurred while updating student information', 'error')  # Flash error message
    finally:
        conn.close()

    return redirect(url_for('indexStudent'))


@app.route('/admin/delete_student/<int:id>', methods=['GET'])
def deleteStudent(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    try:
        # Check if the student exists
        cursor.execute("SELECT id FROM students WHERE id = ?", (id,))
        student = cursor.fetchone()

        if student:
            # The student exists run delete statement.
            cursor.execute("DELETE FROM students WHERE id = ?", (id,))
            conn.commit()

    except Exception as e:
        conn.rollback()

    finally:
        conn.close()
    return redirect(url_for('indexStudent'))


@app.errorhandler(404)
def pageNotFound(e):
    return render_template('/404.html')


@app.errorhandler(500)
def ErrorServer(e):
    return render_template('/500.html')


if __name__ == '__main__':
    app.run()


def jsonify():
    return None
