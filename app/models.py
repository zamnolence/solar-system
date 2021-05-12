from datetime           import datetime
from time               import time
import jwt
from app                import app, db, login
from werkzeug.security  import generate_password_hash, check_password_hash
from flask_login        import UserMixin
from hashlib            import md5
from sqlalchemy.orm import validates

class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(64), index=True, unique=True)
  email = db.Column(db.String(120), index=True, unique=True)
  password_hash = db.Column(db.String(128))
  posts = db.relationship('Post', backref='author', lazy='dynamic')
  quiz_attempts = db.relationship('Attempt', backref='author', lazy='dynamic')
  about_me = db.Column(db.String(140))
  last_seen = db.Column(db.DateTime, default=datetime.utcnow)

  def __repr__(self):
    return '<User: {}, ID: {}, Total Posts: {}, Quiz Attempts: {}>'.format(
      self.username, self.id, self.posts.count(), self.quiz_attempts.count())
  
  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password_hash, password)

  def avatar(self, size):
    digest = md5(self.email.lower().encode('utf-8')).hexdigest()
    return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
      digest, size)

  def get_reset_password_token(self, expires_in=600):
    return jwt.encode(
      {'reset_password': self.id, 'exp': time() + expires_in},
      app.config['SECRET_KEY'], algorithm='HS256')

  @staticmethod
  def verify_reset_password_token(token):
    try:
      id = jwt.decode(token, app.config['SECRET_KEY'],
                      algorithms=['HS256'])['reset_password']
    except:
      return
    return User.query.get(id)

@login.user_loader
def load_user(id):
  return User.query.get(int(id))

class Post(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  body = db.Column(db.String(140))
  timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
  page = db.Column(db.String)
  upvotes = db.Column(db.Integer, default=0)
  downvotes = db.Column(db.Integer, default=0)

  def __repr__(self):
    return '<User: {}, Post ID: {}, Char Count: {}, Page: {}, Votes- Up: {} Down: {}>'.format(
      self.user_id, self.id, len(self.body), self.page, self.upvotes, self.downvotes)

  def upvote(self):
    self.upvotes += 1

  def downvote(self):
    self.downvotes += 1

  def vote_spread(self):
    return self.upvotes - self.downvotes

class Attempt(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  answers = db.relationship('Answer', backref='attempt', lazy='dynamic')
  timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

  def __repr__(self):
    return 'Attempt ID: {}, User: {}, Progress: {}/10, Timestamp: {}'.format(
      self.id, self.user_id, self.answers.count(), self.timestamp)

  def add_answer(self, answer):
    att_answers = self.answers.all()    
    if len(att_answers) >= 10:
      return 1
    for a in att_answers:
      if answer.question == a.question:
        return 1
    db.session.add(answer)
    db.session.commit()
    return 0

class Answer(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  attempt_id = db.Column(db.Integer, db.ForeignKey('attempt.id'))
  question = db.Column(db.Integer)
  correct = db.Column(db.Integer)

  def __repr__(self):
    correct = 'Incorrect' if self.correct == 0 else 'Correct' 
    return 'Answer ID: {}, Attempt ID: {}, Question: {}, {}'.format(
      self.id, self.attempt_id, self.question, correct)
  
  @validates('question')
  def validate_question(self, key, question):
    if question <= 0 or question > 10:
      raise AssertionError('Question must be between 1 and 10. Provided: {}'.format(question))
    return question

  @validates('correct')
  def validate_correct(self, key, correct):
    if correct not in [0, 1]:
      raise AssertionError('Correct must be 0 (correct) or 1 (incorrect). Provided: {}'.format(correct))
    return correct