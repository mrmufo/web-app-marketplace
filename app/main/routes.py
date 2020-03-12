from datetime import datetime
from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    request,
    g,
    jsonify,
    current_app
)
from flask_login import (
    current_user,
    login_required
)
from flask_babel import _, get_locale
from guess_language import guess_language, _get_name
from app import db
from app.main import bp
from app.main.forms import EditProfileForm, AdForm, SearchForm
from app.models import User, Ad
from app.translate import translate


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        # db.session.commit()
    g.locale = str(get_locale())


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    ads = current_user.followed_ads().paginate(page, current_app.config['ADS_PER_PAGE'], False)
    next_url = url_for('main.index', page=ads.next_num) \
        if ads.has_next else None
    prev_url = url_for('main.index', page=ads.prev_num) \
        if ads.has_prev else None
    return render_template('index.html', title=_('Home'), ads=ads.items, next_url=next_url, prev_url=prev_url)


@bp.route('/new_ad', methods=['GET', 'POST'])
@login_required
def new_ad():
    form = AdForm()
    if form.validate_on_submit():
        language = guess_language(form.description.data)
        if language == 'UNKNOWN' or len(language) > 5:
            language = ''
        new = Ad(
            title=form.title.data, category=form.category.data, description=form.description.data, language=language,
            author=current_user)
        db.session.add(new)
        db.session.commit()
        flash(_('New ad posted!'))
        return redirect(url_for('main.index'))
    return render_template('new_ad.html', title=_('New ad'), form=form)


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    ads = user.ads.order_by(Ad.timestamp.desc()).paginate(page, current_app.config['ADS_PER_PAGE'], False)
    next_url = url_for('main.user', username=user.username, page=ads.next_num) \
        if ads.has_next else None
    prev_url = url_for('main.user', username=user.username, page=ads.prev_num) \
        if ads.has_prev else None
    return render_template('user.html', user=user, ads=ads.items,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title=_('Edit Profile'), form=form)


@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    ads = Ad.query.order_by(Ad.timestamp.desc()).paginate(page, current_app.config['ADS_PER_PAGE'], False)
    next_url = url_for('main.explore', page=ads.next_num) \
        if ads.has_next else None
    prev_url = url_for('main.explore', page=ads.prev_num) \
        if ads.has_prev else None
    return render_template('index.html', title='Explore', ads=ads.items,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %(username)s not found.', username=username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash(_('You cannot follow yourself!'))
        return redirect(url_for('main.user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash(_('You are following %(username)s!', username=username))
    return redirect(url_for('main.user', username=username))


@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %(username)s not found.', username=username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash(_('You cannot unfollow yourself!'))
        return redirect(url_for('main.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash(_('You are not following %(username)s anymore', username=username))
    return redirect(url_for('main.user', username=username))


@bp.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.explore'))
    page = request.args.get('page', 1, type=int)
    ads, total = Ad.search(g.search_form.q.data, page, current_app.config['ADS_PER_PAGE'])
    next_url = url_for('main.search', q=g.search_form.q.data, page=page + 1) \
        if total > page * current_app.config['ADS_PER_PAGE'] else None
    prev_url = url_for('main.search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None
    return render_template('search.html', title=_('Search'), ads=ads,
                           next_url=next_url, prev_url=prev_url)


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        g.search_form = SearchForm()
    g.locale = str(get_locale())


@bp.route('/translate', methods=['POST'])
@login_required
def translate_text():
    return jsonify({'text': translate(request.form['text'],
                                      request.form['source_language'],
                                      request.form['dest_language'])})


@bp.route('/show_category/<category>')
@login_required
def show_category(category):
    page = request.args.get('page', 1, type=int)
    ads = Ad.query.filter(Ad.category == category).order_by(Ad.timestamp.desc())\
        .paginate(page, current_app.config['ADS_PER_PAGE'], False)
    next_url = url_for('main.show_category', category=category, page=ads.next_num) \
        if ads.has_next else None
    prev_url = url_for('main.show_category', category=category, page=ads.prev_num) \
        if ads.has_prev else None
    return render_template('search.html', title=_('Explore'), ads=ads.items,
                           next_url=next_url, prev_url=prev_url, category=category)


@bp.route('/ad_view/<id>')
@login_required
def ad_view(id):
    ad = Ad.query.filter_by(id=id).first()
    lang = _get_name(ad.language)
    return render_template('ad_view.html', ad=ad, lang=lang)
