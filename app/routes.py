from flask import (
    render_template,
    redirect,
    url_for
)
from app import app
from app.forms import LoginForm


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/new_ad')
def new_ad_form():
    return render_template('new_ad.html')


@app.route('/new_ad', methods=['POST'])
def post_new_ad():
    return redirect(url_for('home'))


@app.route('/login')
def login():
    form = LoginForm()
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('login.html', title='Sign in', form=form)
