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
    user0 = User(id='0', username='JaneDoe', email='Jane.Doe@email.com', about_me='I love dogs')
    user1 = User(id='99999999', username='JohnSmith', email='John.Smith@email.com', about_me='I am indifferent of cats')
    db.session.add(user0)
    db.session.add(user1)
    db.session.commit()

  def test_password_hashing(self):
    u = User.query.first()
    u.set_password('hunter2')
    self.assertTrue(u.check_password('hunter2'))
    self.assertFalse(u.check_password('Test'))

  def tearDown(self):
    db.session.remove()
    db.drop_all()

if __name__ == '__main__':
  unittest.main(verbosity=2)