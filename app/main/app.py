from flask import Flask, render_template, flash, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from wtforms.validators import DataRequired, Optional

app = Flask(__name__, template_folder='../templates')
app.config['SECRET_KEY'] = 'd52326c7d845b4b41e4872ae2de9b66b'
bootstrap = Bootstrap(app)


class ArtistFrom(FlaskForm):
    name = StringField('Podaj imię artysty:', validators=[DataRequired()])
    surname = StringField('Podaj nazwisko artysty:', validators=[DataRequired()])
    birth_date = DateField('Data urodzeniao artysty:', validators=[DataRequired()])
    nickname = StringField('Podaj ksywkę artysty:', validators=[Optional()])
    localization = StringField('Skąd pochodzi:', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def home():
    name = None
    surname = None
    birth_date = None
    nickname = None
    localization = None

    form = ArtistFrom()
    if request.method == 'POST':
        if form.validate_on_submit():
            name = form.name.data
            surname = form.surname.data
            birth_date = form.birth_date.data
            nickname = form.nickname.data
            localization = form.localization.data
            form.name.data = ''
            flash('Twoja wiadomość została wysłana!', 'success')
            return redirect(url_for('home'))
    return render_template('home.html', form=form, name=name, surname=surname, birth_date=birth_date, nickname=nickname,
                           localization=localization)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/artists_all')
def artists_all():
    return render_template('all_artists.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
