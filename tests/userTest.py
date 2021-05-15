import unittest, os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

# Flask server is required to be running. User terminates server.

class UserTest(unittest.TestCase):
  @classmethod
  def setUp(inst):
    # create a new Firefox session
    inst.driver = webdriver.Firefox()
    inst.driver.implicitly_wait(30)
    inst.driver.maximize_window()
    # navigate to the home page
    inst.driver.get("http://127.0.0.1:5000/")

  @classmethod
  def tearDown(inst):
    # close the browser window
    inst.driver.quit()

if __name__ == '__main__':
  unittest.main()