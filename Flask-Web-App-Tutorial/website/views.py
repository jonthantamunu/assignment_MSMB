from flask import Blueprint, render_template, request, flash, jsonify, request, redirect, current_app, send_from_directory
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
import os
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)

@views.route('/images')
def image():
    current_app.config['UPLOAD_DIRECTORY'] = 'uploads/'
    current_app.config['ALLOWED_EXTENSIONS'] = ['.jpg', '.jpeg', '.png', '.gif']
    files = os.listdir(current_app.config['UPLOAD_DIRECTORY'])
    images = []
    for file in files:
        extension = os.path.splitext(file)[1].lower()
        if extension in current_app.config['ALLOWED_EXTENSIONS']:
            images.append(file)

    return render_template("image.html", images=images, user=current_user)

@views.route('/upload', methods=['GET', 'POST'])
def upload():
    current_app.config['UPLOAD_DIRECTORY'] = 'uploads/'
    current_app.config['MAX_CONTENT_LENGTH'] = 16*1024*1024
    current_app.config['ALLOWED_EXTENSIONS'] = ['.jpg', '.jpeg', '.png', '.gif']
    try:
        file = request.files['file']
        extension = os.path.splitext(file.filename)[1]
        if file:
            if extension not in current_app.config['ALLOWED_EXTENSIONS']:
                flash('File is not an image')
                return redirect('/images')
            file.save(os.path.join(current_app.config['UPLOAD_DIRECTORY'], secure_filename(file.filename)))

    except RequestEntityTooLarge:
        flash('File is larger than the 16MB limit')
        return redirect('/images')
    return redirect('/images')

@views.route('/uploads/<filename>', methods=['GET'])
def uploads(filename):
    current_app.config['ALLOWED_EXTENSIONS']
    current_app.config['UPLOAD_DIRECTORY'] = 'uploads/'
    return send_from_directory(current_app.config['UPLOAD_DIRECTORY'], filename)

@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
