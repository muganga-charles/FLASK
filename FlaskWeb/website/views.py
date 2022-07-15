from flask import Flask, Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
import sqlite3,random
from . import db
import json

views = Blueprint('views', __name__)
connection=sqlite3.connect('database.db')
with open('schema.sql') as f:
    connection.executescript(f.read())
cur=connection.close()
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            ids=random.randint(1,23)
            #new_note = Note(data=note, user_id=current_user.id)
            #mycursor.execute('''CREATE TABLE notes (id INT PRIMARY KEY AUTO_INCREMENT, data VARCHAR(255))''')
            cur.execute("INSERT INTO Note (id,data) VALUES(?,?)",(ids,note))
            connection.commit()
            cur.close()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

