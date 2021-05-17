import unittest, os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from selenium import webdriver

# Flask server is required to be running. User terminates server.

class ModuleTest(unittest.TestCase):
  @classmethod
  def setUp(self):
    # create a new Firefox session
    self.driver = webdriver.Firefox()
    self.driver.implicitly_wait(30)
    self.driver.maximize_window()
    # Log in and navigate to the home page
    self.driver.get("http://127.0.0.1:5000/login")
    self.driver.find_element_by_id("username").send_keys("Test_Admin")
    self.driver.find_element_by_id("password").send_keys("HowlingChihuahua")
    self.driver.find_element_by_id("submit-field").click()
  
  # Tests navigation to each module. Further navigation handled in quizTest.py
  def test_module_navigation(self):
    modules = ["The Vacuum of Space", "The Planets", "Satellites", "The Sun"]
    for m in modules:
      self.driver.get("http://127.0.0.1:5000/")
      self.driver.find_element_by_id(m).click()
      assert "Modules" in self.driver.title, "Did not navigate to '{}' page.".format(m)
      title = self.driver.find_element_by_css_selector("h1").text
      assert m in title, "Appropriate title not present. Found: '{}.' Required: '{}'".format(title, m)

  @classmethod
  def tearDown(self):
    # close the browser window
    self.driver.quit()

if __name__ == '__main__':
  unittest.main()