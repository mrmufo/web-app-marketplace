from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
)
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/mufo/FlaskProjects/BSRH/bsrh.db'
db = SQLAlchemy(app)
db.create_all()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)


admin = User(username='admin', email='admin@example.com')
guest = User(username='guest', email='guest@example.com')


@app.route('/')
def home():

    return render_template('index.html')


@app.route('/new_ad')
def new_ad_form():
    return render_template('new_ad.html')


@app.route('/new_ad', methods=['POST'])
def post_new_ad():

    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run()

