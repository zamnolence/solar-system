import sys
import json
import random
from flask           import render_template, flash, redirect, url_for, request, jsonify
from flask_login     import current_user, login_user, logout_user, login_required
from app             import app, db
from app.forms       import LoginForm, RegistrationForm, EditProfileForm, ResetPasswordRequestForm, ResetPasswordForm, PostForm
from app.models      import User, Post, Question, CurrentQuestion, QuestionSet, Option, Score
from app.email       import send_password_reset_email
from app.controllers import UserController, QuizController
from werkzeug.urls   import url_parse
from datetime        import datetime
from dateutil        import tz

# Home view
@app.route('/', methods = ['GET','POST'])
@app.route('/index', methods = ['GET','POST'])
@app.route('/home', methods = ['GET','POST'])
def home():
    questionSet = QuestionSet.query.all()
    return render_template('home.html', questionSet = questionSet)

# More Learning view
@app.route('/more_learning')
def more_learning():
    return render_template('more_learning.html')

# Scoreboard view
@app.route('/scoreboard')
@login_required
def scoreboard():
    return render_template('scoreboard.html')

# Delete Post
@app.route('/delete_post', methods = ['GET','POST'])
@login_required
def delete_post():
  post=Post.query.filter_by(id=request.args.get('postId')).first_or_404()
  db.session.delete(post)
  db.session.commit()
  module = request.args.get('module') # save requested (protected) URL
  if not module:
      return redirect(url_for('user_profile', username=current_user.username))
  return redirect(url_for('learning_module', module=module))

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

# Register view
@app.route('/register', methods=['GET', 'POST'])
def register():
    return UserController.register()

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
@app.route('/user/<username>', methods = ['GET','POST'])
def user_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.paginate(
      page, 5, False)
    next_url = url_for('user_profile', username=username, page=posts.next_num) \
      if posts.has_next else None
    prev_url = url_for('user_profile', username=username, page=posts.prev_num) \
      if posts.has_prev else None

    score_dict = [] # initialise module score dictionary
    total = 0       # initialise total score as zero
    # get all scores of current_user
    user_scores = Score.query.filter_by(user_id=user.id).all()
    for score in user_scores:
        score_dict.append({'module': score.questionset_id}) # append scores for each learning module
        total += score.score    # add total score
        scoreSorted = Score.query.filter_by(user_id=user.id).order_by(Score.score.desc()).all()
    return render_template('user_profile.html', user=user, score=total, posts=posts.items, 
    scoreSorted = scoreSorted, next_url=next_url, prev_url=prev_url)

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
    return render_template('reset_pass_request.html',
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
    return render_template('reset_pass.html', form=form)

# Learning Module view
@app.route('/learning_module/<module>', methods=['GET', 'POST'])
@login_required
def learning_module(module):
  page = request.args.get('page', 1, type=int)
  posts = Post.query.filter_by(page=module).paginate(
    page, app.config['POSTS_PER_PAGE'], False)
  next_url = url_for('learning_module', module=module, page=posts.next_num) \
    if posts.has_next else None
  prev_url = url_for('learning_module', module=module, page=posts.prev_num) \
    if posts.has_prev else None
  form = PostForm()
  
  if form.validate_on_submit():
    post = Post(body=form.post.data, author=current_user, page=module)
    db.session.add(post)
    db.session.commit()
    flash('Your post is now live!')
    next_url = url_for('learning_module', module=module, page=posts.next_num) \
      if posts.has_next else None
    prev_url = url_for('learning_module', module=module, page=posts.prev_num) \
      if posts.has_prev else None
    posts = Post.query.filter_by(page=module).paginate(
      page, app.config['POSTS_PER_PAGE'], False)
    form.post.data=""

  return render_template('modules/learning_module.html', module=module, form=form,
      posts=posts.items, next_url=next_url,
      prev_url=prev_url)

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
    latest_module = latest_score.questionset_parent.name
    latest_time_taken = latest_score.time_taken
    scoreSorted = Score.query.filter_by(questionset_id=latest_module_id).order_by(Score.score.desc()).all()
    return render_template('result.html', latestScore=latest_score, scoreSorted=scoreSorted, moduleName=latest_module, timeTaken=latest_time_taken)

# Result submission
@app.route('/submit-results', methods=['POST'])
def submit_results():
    return UserController.submit_results()