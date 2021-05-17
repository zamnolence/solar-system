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

  # Logs the user in for authorization-specific tests.
  def login(self, username, password):
    self.driver.get("http://127.0.0.1:5000/login")
    self.driver.find_element_by_id("username").send_keys(username)
    self.driver.find_element_by_id("password").send_keys(password)
    self.driver.find_element_by_id("submit-field").click()

  # Tests whether a valid users details work to log in.
  def test_user_login_valid(self):
    self.login("Test_Admin", "HowlingChihuahua")
    assert "Home" in self.driver.title

  # Tests whether an invalid users details fail to log in.
  def test_user_login_invalid(self):
    self.login("Fake_User", "-.-")
    assert "Sign" in self.driver.title

  # Tests access to user profiles.
  def test_user_profile(self):
    # Anonymous user can visit profiles.
    self.driver.get("http://127.0.0.1:5000/user/Test_Admin")
    assert "Profile" in self.driver.title
    assert "Test_Admin" in self.driver.find_element_by_id("user_heading").text

    # Logged in user can visit profiles.
    self.login("Test_Admin", "HowlingChihuahua")
    self.driver.get("http://127.0.0.1:5000/user/Test_Admin")
    assert "Profile" in self.driver.title
    assert "Test_Admin" in self.driver.find_element_by_id("user_heading").text

  # Tests that the forgotten password links redirects correctly.
  def test_forgotten_password(self):
    self.driver.get("http://127.0.0.1:5000/login")
    self.driver.find_element_by_id("forgotten_password").click()
    assert "Reset" in self.driver.title

  # Tests that the register link redirects correctly.
  def test_register(self):
    self.driver.get("http://127.0.0.1:5000/login")
    self.driver.find_element_by_id("register").click()
    assert "Sign" in self.driver.title #Needs to be better

  @classmethod
  def tearDown(self):
    # close the browser window
    self.driver.quit()

if __name__ == '__main__':
  unittest.main()