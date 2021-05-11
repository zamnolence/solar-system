from flask          import render_template, flash, redirect, url_for, request
from flask_login    import current_user, login_user, logout_user, login_required
from app            import app, db
from app.forms      import LoginForm, RegistrationForm, EditProfileForm, ResetPasswordRequestForm, ResetPasswordForm
from app.models     import User
from app.email      import send_password_reset_email
from werkzeug.urls  import url_parse
from datetime       import datetime
from dateutil       import tz

# Record time of last visit
@app.before_request
def before_request():
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    utc = datetime.utcnow()
    utc = utc.replace(tzinfo=from_zone)
    central = utc.astimezone(to_zone)   # convert to local timezone
    if current_user.is_authenticated:
        current_user.last_seen = central
        db.session.commit()

# Index view
@app.route('/')
@app.route('/index')
## @login_required
def index():
  user = {'username': 'Squeebs'}
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
  return render_template('index.html', title='Home', posts=posts)

# Login view
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:           # redirect if already logged in
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():               # validate login form
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')    # save requested (protected) URL
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')        # redirect to index if requested URL doesn't exist
        return redirect(next_page)   # reditect to requested URL if exists
    return render_template('login.html', title='Sign In', form=form)

# Logout view
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# Register view
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:           # redirect if already logged in
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():               # validate registration form
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)                    # add to db
        db.session.commit()                     # commit to db
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

# User profile view
@app.route('/user/<username>')  # dynamic component username
@login_required                 # only logged in user allow
def user(username):
    user = User.query.filter_by(username=username).first_or_404() # first() if exists or sends 404 error if not exists
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)

# Edit profile view
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)

# Reset password request view
@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)

# Password reset view
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
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)