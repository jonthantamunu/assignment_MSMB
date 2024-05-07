from flask import Blueprint, render_template, request
from flask_login import current_user, login_required
from . import db
from .models import Feedback

lahan = Blueprint('lahan', __name__)

@lahan.route('/lahan')
@login_required
def index():
    return render_template('lahan.html', user=current_user)

@lahan.route('/submit', methods=['POST'])
@login_required
def submit():
    if request.method == 'POST':
        nama_lahan = request.form['nama_lahan']
        tanaman = request.form['tanaman']
        luas = request.form['luas']
        deskripsi = request.form['deskripsi']
        
        if nama_lahan == '' or tanaman == '':
            return render_template('lahan.html', message='Please enter required fields')
        
        if db.session.query(Feedback).filter(Feedback.nama_lahan == nama_lahan).count() == 0:
            data = Feedback(nama_lahan=nama_lahan, tanaman=tanaman, luas=luas, deskripsi=deskripsi)
            db.session.add(data)
            db.session.commit()
            return render_template('success.html')
        
        return render_template('lahan.html', message='You have already submitted feedback', user=current_user)
