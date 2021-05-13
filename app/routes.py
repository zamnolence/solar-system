<<<<<<< HEAD
import sys
import json
import random
from flask           import render_template, flash, redirect, url_for, request, jsonify
from flask_login     import current_user, login_user, logout_user, login_required
from app             import app, db
from app.forms       import LoginForm, RegistrationForm, EditProfileForm, ResetPasswordRequestForm, ResetPasswordForm
from app.models      import User, Post, Question, CurrentQuestion, QuestionSet, Option, Score
from app.email       import send_password_reset_email
from app.controllers import UserController, QuizController
from werkzeug.urls   import url_parse
from datetime        import datetime
from dateutil        import tz

# Home view
@app.route('/', methods = ['GET','POST'])
def home():
    questionSet = QuestionSet.query.all()
    return render_template('home.html', questionSet = questionSet)


# Login view (redirect authenticated user to home)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return UserController.login()

# Log out view
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))
    
=======
from flask          import render_template, flash, redirect, url_for, request
from flask_login    import current_user, login_user, logout_user, login_required
from app            import app, db
from app.forms      import LoginForm, RegistrationForm, EditProfileForm, ResetPasswordRequestForm, ResetPasswordForm, PostForm
from app.models     import User, Post
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
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
  if current_user.is_authenticated:
    page = request.args.get('page', 1, type=int)
    posts = current_user.posts.paginate(
      page, app.config['POSTS_PER_PAGE'], False)
    form = PostForm()
    next_url = url_for('index', page=posts.next_num) \
      if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) \
      if posts.has_prev else None

    if form.validate_on_submit():
      post = Post(user_id=current_user.id, body=form.post.data, page='index')
      db.session.add(post)
      db.session.commit()
      flash('Your post is now live!')
      form.post.data = ""
      posts = current_user.posts.paginate(
        page, app.config['POSTS_PER_PAGE'], False)

    return render_template('index.html', title='Home', form=form,
      posts=posts.items, next_url=next_url,
      prev_url=prev_url)
  else:
    return render_template('index.html', title='index')

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
>>>>>>> comments

# Register view
@app.route('/register', methods=['GET', 'POST'])
def register():
<<<<<<< HEAD
    return UserController.register()

=======
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
>>>>>>> comments

# Record time of last visit for user profile page
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

# User profile view
<<<<<<< HEAD
@app.route('/user/<username>', methods = ['GET','POST'])
def user_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    # posts = [
    #     {'author': user, 'body': 'Test post #1'},
    #     {'author': user, 'body': 'Test post #2'}
    # ]
    score_dict = [] # initialise module score dictionary
    total = 0       # initialise total score as zero
    # get all scores of current_user
    user_scores = Score.query.filter_by(user_id=current_user.id).all()
    for score in user_scores:
        score_dict.append({'module': score.questionset_id}) # append scores for each learning module
        total += score.score    # add total score
        scoreSorted = Score.query.filter_by(user_id=current_user.id).order_by(Score.score.desc()).all()
    return render_template('user_profile.html', user=user, score=total, scoreSorted = scoreSorted)

=======
@app.route('/user/<username>')  # dynamic component username
def user(username):
  user = User.query.filter_by(username=username).first_or_404() # first() if exists or sends 404 error if not exists
  return render_template('user.html', user=user, posts=user.posts)
>>>>>>> comments

# Edit profile view
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
<<<<<<< HEAD
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

=======
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
>>>>>>> comments

# Reset password request view
@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
<<<<<<< HEAD
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_pass_request.html',
                           title='Reset Password', form=form)

=======
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
>>>>>>> comments

# Password reset view
@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
<<<<<<< HEAD
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
    return render_template('reset_pass.html', form=form)


# Quiz view
@app.route('/quiz', methods = ['GET','POST'])
def generate_quiz():
    return QuizController.generate_quiz()


# Result view of latest submission
@app.route('/result', methods=['GET'])
def result():
    # Get score and module of current user
    latest_score = Score.query.filter_by(user_id=current_user.id).all()[-1]
    latest_module_id = latest_score.questionset_id
    scoreSorted = Score.query.filter_by(questionset_id=latest_module_id).order_by(Score.score.desc()).all()
    return render_template('result.html', latestScore=latest_score, scoreSorted=scoreSorted)

# Result submission
@app.route('/submit-results', methods=['POST'])
def submit_results():
    return UserController.submit_results()
=======
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
>>>>>>> comments
