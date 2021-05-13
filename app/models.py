import jwt
from time               import time
from datetime           import datetime
<<<<<<< HEAD
=======
from time               import time
import jwt
>>>>>>> comments
from app                import app, db, login
from werkzeug.security  import generate_password_hash, check_password_hash
from flask_login        import UserMixin
from hashlib            import md5
from sqlalchemy.orm     import validates


# User table
class User(UserMixin, db.Model):
    __tablename__ = 'user_table'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    user_type = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    # quiz_attempts = db.relationship('Attempt', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    score_child = db.relationship("Score", backref = 'user_parent')

    def __repr__(self):
      return '<User: {}, ID: {}, Total Posts: {}, Quiz Attempts: {}>'.format(
        self.username, self.id, self.posts.count(), self.quiz_attempts.count())
  
<<<<<<< HEAD
    def set_password(self, password):
      self.password_hash = generate_password_hash(password)

    def check_password(self, password):
      return check_password_hash(self.password_hash, password)

    def avatar(self, size):
      digest = md5(self.email.lower().encode('utf-8')).hexdigest()
      return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

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
    

# Load authenticated user
=======
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

>>>>>>> comments
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


# Post table
class Post(db.Model):
<<<<<<< HEAD
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_table.id')) #user.id
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


# Question table
class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key = True)
    question = db.Column(db.String(128))
    question_type = db.Column(db.String(128))
    answer = db.Column(db.String(128))
    child = db.relationship("CurrentQuestion", backref="parent")
    option_child = db.relationship("Option", backref="parent")
    reference_value = db.Column(db.String(128))

    #Print current question
    def __repr__(self):
        return self.question


# Curent question table for tracking
class CurrentQuestion(db.Model):
    __tablename__ = 'current_question'
    id = db.Column(db.Integer, primary_key = True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    questionset_id = db.Column(db.Integer, db.ForeignKey('questionset.id'))
    question_number = db.Column(db.Integer)

    def __repr__(self):
        return self.question


# Question set table (At the moment, we have 4.)
class QuestionSet(db.Model):
    __tablename__ = 'questionset'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64))
    number_of_questions = db.Column(db.Integer)
    child = db.relationship("CurrentQuestion")
    score_child = db.relationship('Score', backref= 'questionset_parent')

    def __repr__(self):
        return self.name


# MCQ option table 
class Option(db.Model):
    __tablename__ = 'option'
    id = db.Column(db.Integer, primary_key = True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    option_value = db.Column(db.String(64))

    def __repr__(self):
        return self.option_value


# Score table
class Score(db.Model):
    __tablename__ = 'score'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_table.id'))
    questionset_id = db.Column(db.Integer, db.ForeignKey('questionset.id'))
    score = db.Column(db.Integer)
    time_taken = db.Column(db.Time)



# class Attempt(db.Model):
#   id = db.Column(db.Integer, primary_key=True)
#   user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#   answers = db.relationship('Answer', backref='attempt', lazy='dynamic')
#   timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

#   def __repr__(self):
#     return 'Attempt ID: {}, User: {}, Progress: {}/10, Timestamp: {}'.format(
#       self.id, self.user_id, self.answers.count(), self.timestamp)

#   def add_answer(self, answer):
#     att_answers = self.answers.all()    
#     if len(att_answers) >= 10:
#       return 1
#     for a in att_answers:
#       if answer.question == a.question:
#         return 1
#     db.session.add(answer)
#     db.session.commit()
#     return 0

# class Answer(db.Model):
#   id = db.Column(db.Integer, primary_key=True)
#   attempt_id = db.Column(db.Integer, db.ForeignKey('attempt.id'))
#   question = db.Column(db.Integer)
#   correct = db.Column(db.Integer)

#   def __repr__(self):
#     correct = 'Incorrect' if self.correct == 0 else 'Correct' 
#     return 'Answer ID: {}, Attempt ID: {}, Question: {}, {}'.format(
#       self.id, self.attempt_id, self.question, correct)
=======
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
>>>>>>> comments
  
#   @validates('question')
#   def validate_question(self, key, question):
#     if question <= 0 or question > 10:
#       raise AssertionError('Question must be between 1 and 10. Provided: {}'.format(question))
#     return question

#   @validates('correct')
#   def validate_correct(self, key, correct):
#     if correct not in [0, 1]:
#       raise AssertionError('Correct must be 0 (correct) or 1 (incorrect). Provided: {}'.format(correct))
#     return correct