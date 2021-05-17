import unittest, os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from selenium import webdriver

# Flask server is required to be running. User terminates server.

class NavigationTest(unittest.TestCase):
  @classmethod
  def setUp(self):
    # create a new Firefox session
    self.driver = webdriver.Firefox()
    self.driver.implicitly_wait(30)
    self.driver.maximize_window()
    # navigate to the home page
    self.driver.get("http://127.0.0.1:5000/")

  # Logs the user in for authorization-specific tests.
  def login(self):
    self.driver.get("http://127.0.0.1:5000/login")
    self.driver.find_element_by_id("username").send_keys("Test_Admin")
    self.driver.find_element_by_id("password").send_keys("HowlingChihuahua")
    self.driver.find_element_by_id("submit-field").click()

  # Tests navigation through the nav bar by an anonymous user.
  def test_traverse_navigation_anonymous(self):
    assert "Home" in self.driver.title, "Home page not reached."
    self.driver.find_element_by_id("nav_login").click()
    assert "Sign" in self.driver.title, "Sign In page not reached."
    self.driver.find_element_by_id("nav_register").click()
    assert "Sign" in self.driver.title, "Register (Sign Up) page not reached."
    self.driver.find_element_by_id("nav_home").click()
    assert "Home" in self.driver.title, "Home page not reached."

  # Tests that an anonymous user cannot access pages that require authorization.
  def test_traverse_hidden_to_anonymous(self):
    pages = [
      "learning_module/vacuum", 
      "learning_module/planets", 
      "learning_module/satellites", 
      "learning_module/sun",
      "edit_profile"
    ]
    for p in pages:
      self.driver.get("http://127.0.0.1:5000/{}".format(p))
      assert "Sign" in self.driver.title, \
      "Unauthorized user able to access '{}' page.".format(p)

  # Tests navigation through the nav bar by an authorized user.
  def test_traverse_navigation_logged_in(self):
    self.login()
    assert "Home" in self.driver.title, "Home page not reached."
    self.driver.find_element_by_id("nav_profile").click()
    assert "Test_Admin" in self.driver.find_element_by_id("user_heading").text, \
      "Test user page not reached."
    self.driver.find_element_by_id("nav_logout").click()
    assert "Home" in self.driver.title, "Logout page not reached."
    self.driver.find_element_by_id("nav_home").click()
    assert "Home" in self.driver.title, "Home page not reached."

  @classmethod
  def tearDown(self):
    # close the browser window
    self.driver.quit()

if __name__ == '__main__':
  unittest.main()