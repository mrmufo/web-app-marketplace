from datetime import datetime
from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    request,
    g,
    jsonify
)
from flask_login import (
    current_user,
    login_user,
    logout_user,
    login_required
)
from flask_babel import _, get_locale
from werkzeug.urls import url_parse
from guess_language import guess_language
from app import app, db
from app.forms import (
    EditProfileForm, LoginForm, AdForm, AdSearchForm, RegistrationForm, ResetPasswordForm, ResetPasswordRequestForm
)
from app.email import send_password_reset_email
from app.models import User, Ad
from app.translate import translate


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    g.locale = str(get_locale())


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    ads = current_user.followed_ads().paginate(page, app.config['ADS_PER_PAGE'], False)
    next_url = url_for('index', page=ads.next_num) \
        if ads.has_next else None
    prev_url = url_for('index', page=ads.prev_num) \
        if ads.has_prev else None
    return render_template('index.html', title=_('Home'), ads=ads.items, next_url=next_url, prev_url=prev_url)


@app.route('/new_ad', methods=['GET', 'POST'])
@login_required
def new_ad():
    form = AdForm()
    if form.validate_on_submit():
        language = guess_language(form.description.data)
        if language == 'UNKNOWN' or len(language) > 5:
            language = ''
        new_ad = Ad(
            title=form.title.data, category=form.category.data, description=form.description.data, language=language,
            author=current_user)
        db.session.add(new_ad)
        db.session.commit()
        flash(_('New ad posted!'))
        return redirect(url_for('index'))
    return render_template('new_ad.html', title=_('New ad'), form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(_('Invalid username or password'))
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        # Redirect only to relative URL
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title=_('Sign In'), form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(_('Great, your account has been created! You can BSRH now!'))
        return redirect(url_for('login'))
    return render_template('register.html', title=_('Register'), form=form)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash(_('Check your email for the instructions to reset your password'))
        return redirect(url_for('login'))
    return render_template('reset_password_request.html', title=_('Reset Password'), form=form)
 

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_('Your password has been reset.'))
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    ads = user.ads.order_by(Ad.timestamp.desc()).paginate(page, app.config['ADS_PER_PAGE'], False)
    next_url = url_for('user', username=user.username, page=ads.next_num) \
        if ads.has_next else None
    prev_url = url_for('user', username=user.username, page=ads.prev_num) \
        if ads.has_prev else None
    return render_template('user.html', user=user, ads=ads.items,
                           next_url=next_url, prev_url=prev_url)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title=_('Edit Profile'), form=form)


@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    ads = Ad.query.order_by(Ad.timestamp.desc()).paginate(page, app.config['ADS_PER_PAGE'], False)
    next_url = url_for('explore', page=ads.next_num) \
        if ads.has_next else None
    prev_url = url_for('explore', page=ads.prev_num) \
        if ads.has_prev else None
    return render_template('index.html', title='Explore', ads=ads.items,
                           next_url=next_url, prev_url=prev_url)


@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %(username)s not found.', username=username))
        return redirect(url_for('index'))
    if user == current_user:
        flash(_('You cannot follow yourself!'))
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash(_('You are following %(username)s!', username=username))
    return redirect(url_for('user', username=username))


@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %(username)s not found.', username=username))
        return redirect(url_for('index'))
    if user == current_user:
        flash(_('You cannot unfollow yourself!'))
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash(_('You are not following %(username)s anymore', username=username))
    return redirect(url_for('user', username=username))


@app.route('/show_ads/<category>')
def show_ads(category):
    form = AdSearchForm()
    keyword = request.form['keyword']
    page = request.args.get('page', 1, type=int)
    ads = Ad.query.filter_by(category=category).ilike('%'+keyword+'%').order_by(Ad.timestamp.desc())
    next_url = url_for('show_ads', category=category, page=ads.next_num) \
        if ads.has_next else None
    prev_url = url_for('show_ads', category=category, page=ads.prev_num) \
        if ads.has_prev else None
    return render_template('show_ads.html', title='Show ads', keyword=keyword, category=category, ads=ads.items,
                           next_url=next_url, prev_url=prev_url)
    # todo select field with category choices


@app.route('/translate', methods=['POST'])
@login_required
def translate_text():
    return jsonify({'text': translate(request.form['text'],
                                      request.form['source_language'],
                                      request.form['dest_language'])})
