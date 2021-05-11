import unittest, os
from app import app, db
from app.models import User, Post, Attempt, Answer

class tests(unittest.TestCase):
  def setUp(self):
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI']=\
      'sqlite:///'+os.path.join(basedir, 'test.db')
    self.app = app.test_client()
    db.create_all()
    u1 = User(id='1', username='JaneDoe', email='Jane.Doe@email.com')
    u2 = User(id='99999999', username='JohnSmith', email='John.Smith@email.com', about_me='I am indifferent of cats')
    att = Attempt(user_id=u1.id)
    db.session.add(u1)
    db.session.add(u2)
    db.session.add(att)
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
   # self.assertEqual(u.email, 'john.smith@email.com', "Email is case sensitive (incorrect).")

  def test_user_about_me(self):
    u = User.query.first()
    self.assertFalse(u.about_me, "About me is not None.")
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

  def test_post_voting(self):
    u = User.query.first()
    _str = "This is a test post with 39 characters."
    p = Post(user_id=u.id, body=_str, page="test_page")
    db.session.add(p)
    db.session.commit()

    self.assertEqual(p.upvotes, 0, "Initial upvote count noy 0.")
    self.assertEqual(p.downvotes, 0, "Initial downvote count not 0.")
    self.assertEqual(p.vote_spread(), 0, "Initial vote spread not 0.")

    for i in range(17):
      p.upvote()

    for i in range(5):
      p.downvote()

    self.assertEqual(p.upvotes, 17, "Upvote count incorrect.")
    self.assertEqual(p.downvotes, 5, "Downvote count incorrect.")
    self.assertEqual(p.vote_spread(), 12, "Vote spread incorrect.")

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

#  def test_post_body_validation(self):
    # Validation must be implemented first.

# Quiz Attempt specific tests
  def test_answer_count_in_range(self):
    att = Attempt.query.first()
    self.assertFalse(att.answers.count(), "Answer count is not 0.")

    # Add 5 answers
    for i in range(1, 6):
      a = Answer(attempt_id=att.id, question=i)
      att.add_answer(a)
    self.assertEqual(att.answers.count(), 5, "Answer count is not 5.")

    # Add 5 more answers
    for i in range(6, 11):
      a = Answer(attempt_id=att.id, question=i)      
      att.add_answer(a)
    self.assertEqual(att.answers.count(), 10, "Answer count is not 10.")

    # Add an 11th answer
    # No more than 10 unique answers can be present due to answer validation, 
    # so this is part of the test is functionally useless at this time.
    a = Answer(attempt_id=att.id)      
    att.add_answer(a)
    self.assertEqual(att.answers.count(), 10, "11th answer was accepted (Out of Bounds).")

  def test_duplicate_answer(self):
    att = Attempt.query.first()
    self.assertFalse(att.answers.count(), "Answer count is not 0.")

    a1 = Answer(attempt_id=att.id, question=5)
    a2 = Answer(attempt_id=att.id, question=5)
    att.add_answer(a1)
    att.add_answer(a2)
    self.assertEqual(att.answers.count(), 1, "Duplicate answer was accepted.")

# Answer specific tests
  def test_question_number_valid(self):
    with self.assertRaises(AssertionError):
      a1 = Answer(question=-1)
      a2 = Answer(question=11)

  def test_answer_correct_valid(self):
    with self.assertRaises(AssertionError):
      a1 = Answer(correct=-1)
      a2 = Answer(correct=2)
    
    att = Attempt.query.first()
    self.assertFalse(att.answers.count(), "Answer count is not 0.")
    a1 = Answer(attempt_id=att.id, question=1, correct=0)
    a2 = Answer(attempt_id=att.id, question=2, correct=1)
    att.add_answer(a1)
    att.add_answer(a2)
    self.assertEqual(att.answers.count(), 2, "Answer count is not 2.")

  def tearDown(self):
    db.session.remove()
    db.drop_all()

if __name__ == '__main__':
  unittest.main(verbosity=2)