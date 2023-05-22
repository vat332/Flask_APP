import os

from flask import Flask, render_template, flash, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, FileField
from wtforms.validators import DataRequired, Optional
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_wtf.file import FileRequired, FileAllowed

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['SECRET_KEY'] = 'd52326c7d845b4b41e4872ae2de9b66b'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

migrate = Migrate(app, db)

UPLOAD_FOLDER = '../static/images'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
app.config['UPLOAD_FOLDER'] = '../static/images'


class Artist(db.Model):
    __tablename__ = 'artists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.String(100), nullable=False)
    nickname = db.Column(db.String(100), nullable=False)
    localization = db.Column(db.String(100), nullable=False)
    photo = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return '<Artysta %r "%r" %r >' % self.name, self.nickname, self.surname

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    class Role(db.Model):
        __tablename__ = 'roles'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(64), unique=True)
        users = db.relationship('User', backref='role', lazy='dynamic')

        def __repr__(self):
            return '<Role %r>' % self.name

    class User(db.Model):
        __tablename__ = 'users'
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(64), unique=True, index=True)
        role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<Role %r>' % self.name


class ArtistForm(FlaskForm):
    name = StringField('Imię', validators=[DataRequired()])
    surname = StringField('Nazwisko', validators=[DataRequired()])
    birth_date = DateField('Data urodzenia (YYYY-MM-DD)', format="%Y-%m-%d", validators=[DataRequired()])
    nickname = StringField('Ksywka', validators=[DataRequired()])
    localization = StringField('Pochodzenie', validators=[DataRequired()])
    photo = FileField('Zdjęcie',
                      validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png', "'gif"], 'Tylko obrazki!')])
    submit = SubmitField('Dodaj')


@app.route('/', methods=['GET', 'POST'])
def home():
    form = ArtistForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            artist = Artist(name=form.name.data, surname=form.surname.data, birth_date=form.birth_date.data,
                            nickname=form.nickname.data, localization=form.localization.data)
            if form.photo.data:
                filename = secure_filename(form.photo.data.filename)
                form.photo.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                artist.photo = filename
            db.session.add(artist)
            db.session.commit()
            flash('Artysta został dodany!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Oops coś poszło nie tak. Spróbuj ponownie!', 'danger')
    return render_template('home.html', form=form)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/artists_all')
def artists_all():
    artists = Artist.query.all()
    return render_template('all_artists.html', artists=artists)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
