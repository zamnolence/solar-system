import unittest, os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from selenium import webdriver

# Flask server is required to be running. User terminates server.

class UserTest(unittest.TestCase):
  @classmethod
  def setUp(self):
    # create a new Firefox session
    self.driver = webdriver.Firefox()
    self.driver.implicitly_wait(30)
    self.driver.maximize_window()

  def login(self):
    self.driver.get("http://127.0.0.1:5000/login")
    self.driver.find_element_by_id("username").send_keys("Test_Admin")
    self.driver.find_element_by_id("password").send_keys("HowlingChihuahua")
    self.driver.find_element_by_id("submit-field").click()

  # def test_correct_page(self):
  #   assert "Sign" in self.driver.title

  # def test_user_login(self):
  #   self.login()
  #   assert "Home" in self.driver.title

  def test_user_profile(self):
    self.driver.get("http://127.0.0.1:5000/user/Test_Admin")
    assert "Profile" in self.driver.title

    self.login()
    self.driver.get("http://127.0.0.1:5000/user/Test_Admin")
    assert "Profile" in self.driver.title


  @classmethod
  def tearDown(self):
    # close the browser window
    self.driver.quit()

if __name__ == '__main__':
  unittest.main()