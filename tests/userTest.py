import unittest, os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Flask server is required to be running. User terminates server.

class UserTest(unittest.TestCase):
  @classmethod
  def setUp(self):
    # create a new Firefox session
    self.driver = webdriver.Firefox()
    self.driver.implicitly_wait(30)
    self.driver.maximize_window()
    # navigate to the home page
    self.driver.get("http://127.0.0.1:5000/login")

  def test_correct_page(self):
    assert "Sign" in self.driver.title

  def test_user_login(self):
    form = self.driver.find_element_by_id("main_content").find_element_by_id("login_form")
    assert form != None
    username = form.find_element_by_id("username_p").find_element_by_id("username")
    assert username != None
    password = form.find_element_by_id("password_p").find_element_by_id("password")
    assert password != None
    submit = form.find_element_by_id("form_submit").find_element_by_id("submit_login")
    assert submit != None


  @classmethod
  def tearDown(self):
    # close the browser window
    self.driver.quit()

if __name__ == '__main__':
  unittest.main()