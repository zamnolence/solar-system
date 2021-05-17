import unittest, os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from app import app, db
from app.models import *

class DatabaseTest(unittest.TestCase):
  def setUp(self):
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI']=\
      'sqlite:///'+os.path.join(basedir, 'test.db')
    self.app = app.test_client()
    db.create_all()
    u1 = User(id='1', username='JaneDoe', email='Jane.Doe@email.com')
    u2 = User(id='99999999', username='JohnSmith', email='John.Smith@email.com', about_me='I am indifferent of cats')
    db.session.add(u1)
    db.session.add(u2)
    
    for i in range(1, 5):
      q = Question(question="Test{}".format(i), answer="Answer{}".format(i))
      db.session.add(q)

    for i in range(1, 5):
      for j in range(1, 5):
        o = Option(question_id=i, option_value="Answer{}".format(j))
        db.session.add(o)

    questionSet = QuestionSet(name="Test Module", number_of_questions=4)
    db.session.add(questionSet)
    db.session.commit()

# User specific tests
  def test_password_hashing(self):
    u = User.query.first()
    u.set_password('hunter2')
    self.assertTrue(u.check_password('hunter2'))
    self.assertFalse(u.check_password('Test'))

  def test_create_user(self):
    u = User.query.get('99999999')
    self.assertEqual(u.id, 99999999, "ID incorrect.")
    self.assertEqual(u.username, 'JohnSmith', "Username incorrect.")
    self.assertEqual(u.email, 'John.Smith@email.com', "Email incorrect.")

  def test_user_about_me(self):
    u = User.query.first()
    self.assertFalse(u.about_me, "About me is not empty.")
    _str = "Updated about me with 36 characters."
    u.about_me = _str
    self.assertEqual(len(u.about_me), len(_str), "About me not set correctly (Length of string).")
    self.assertEqual(u.about_me, _str, "About me not set correctly.")

  def test_delete_user(self):
    count = User.query.count()
    self.assertEqual(count, 2, "Two users must be present for test.")
    user = User.query.get('99999999')
    db.session.delete(user)
    db.session.commit()
    self.assertEqual(User.query.count(), 1, "Incorrect number of users remains after deletion of 1.")

# Post specific tests
  def test_new_post(self):
    u = User.query.first()
    count = u.posts.count()
    self.assertEqual(count, 0, "Users initial post count not 0.")

    _str = "This is a test post with 39 characters."
    p = Post(user_id=u.id, body=_str, page="test_page")
    db.session.add(p)
    db.session.commit()

    count = u.posts.count()
    self.assertEqual(count, 1, "Users post count not 1.")

    p = u.posts.first()
    self.assertEqual(len(p.body), len(_str), "Post length incorrect.")
    self.assertEqual(p.body, _str, "Post body does not equal the string given.")

  def test_delete_post(self):
    u = User.query.first()
    _str = "This is a test post with 39 characters."
    p = Post(user_id=u.id, body=_str, page="test_page")
    db.session.add(p)
    db.session.commit()

    post = Post.query.first()
    db.session.delete(post)
    db.session.commit()
    self.assertEqual(u.posts.count(), 0, "Users post count not 0.")
    self.assertEqual(Post.query.count(), 0, "Post count not 0.")

# Question specific tests (Question, QuestionSet, Option, CurrentQuestion)
  def test_question_answer_present_in_options(self):
    questions = Question.query.all()
    for question in questions:
      opt=[]
      for o in question.option_child:
        opt.append(o.option_value)
      self.assertIn(question.answer, opt, "Answer {} not present in question's option children.".format(question.answer))

  def test_question_set_score(self):
    set = QuestionSet.query.first()
    score = Score(user_id=User.query.first(), questionset_id=set.id)
    with self.assertRaises(AssertionError):
      score.score =-1
    score.score = 0
    score.score = 1

  def test_questionset_num_questions(self):
    set = QuestionSet.query.first()
    with self.assertRaises(AssertionError):
      set.number_of_questions=-1
    set.number_of_questions=0

  def test_current_question_number(self):
    questions = Question.query.all()
    set = QuestionSet.query.first()
    set.number_of_questions=len(questions)
    currQuestion = CurrentQuestion(question_id=questions[1].id, questionset_id=set.id, question_number=1)
    with self.assertRaises(AssertionError):
      currQuestion.question_number = 0
      currQuestion.question_number = len(questions) + 1
    currQuestion.question_number = 1
    currQuestion.question_number = len(questions)
    
  def tearDown(self):
    db.session.remove()
    db.drop_all()

if __name__ == '__main__':
  unittest.main(verbosity=2)