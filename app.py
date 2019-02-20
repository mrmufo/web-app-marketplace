from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
)

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/new_ad')
def new_ad_form():
    return render_template('new_ad.html')


@app.route('/new_ad', methods=['POST'])
def post_new_ad():
    return redirect(url_for('/'))


if __name__ == "__main__":
    app.run()
