from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/prephouse'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


if __name__ == '__main__':
    app.run(host='0.0.0.0')
