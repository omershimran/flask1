from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from website.models import Note
from website import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        data = request.form.get('data')
        new_note = Note(data=data, user_id=current_user.id)
        db.session.add(new_note)
        db.session.commit()
    return render_template("home/home.html", text="testing", user=current_user)


@views.route('/delete-note', methods=[ 'POST'])
def delete_note():
    note = json.loads(request.data)
    note_id = note['noteId']
    note = Note.query.get(note_id)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
        else:
            flash('this not is not your to delete...', category='error')

    return jsonify({})