import unittest, os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Flask server is required to be running. User terminates server.

class ModuleTest(unittest.TestCase):
  @classmethod
  def setUp(self):
    # create a new Firefox session
    self.driver = webdriver.Firefox()
    self.driver.implicitly_wait(30)
    self.driver.maximize_window()
    # navigate to the home page
    self.driver.get("http://127.0.0.1:5000/")

  @classmethod
  def tearDown(self):
    # close the browser window
    self.driver.quit()

if __name__ == '__main__':
  unittest.main()