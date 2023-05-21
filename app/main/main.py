from flask import Flask

app = Flask(__name__)


@app.route('/')
def home():
    return '<h1>Hello World</h1>'


@app.route('/about')
def about():
    return '<h1>Informacje o nas</h1>'


@app.route('/contact')
def contact():
    return '<h1>Strona kontaktowa</h1>'


if __name__ == '__main__':
    app.run(debug=True)
