from datetime           import datetime
from app                import db, login
from werkzeug.security  import generate_password_hash, check_password_hash
from flask_login        import UserMixin
from hashlib            import md5

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
    return '<Post ID: {}, Char Count: {}, Page: {}, Votes- Up: {} Down: {}>'.format(
      self.id, len(self.body), self.page, self.upvotes, self.downvotes)

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

class Answer(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  attempt_id = db.Column(db.Integer, db.ForeignKey('attempt.id'))
  question = db.Column(db.Integer)
  correct = db.Column(db.Integer)

  def __repr__(self):
    correct = 'Incorrect' if self.correct == 0 else 'Correct' 
    return 'Answer ID: {}, Attempt ID: {}, Question: {}, {}'.format(
      self.id, self.attempt_id, self.question, correct)