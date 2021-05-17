import unittest, os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Flask server is required to be running. User terminates server.

class QuizTest(unittest.TestCase):
  @classmethod
  def setUp(self):
    # create a new Firefox session
    self.driver = webdriver.Firefox()
    self.driver.implicitly_wait(30)
    self.driver.maximize_window()
    # navigate to the home page
    self.driver.get("http://127.0.0.1:5000/login")
    self.driver.find_element_by_id("username").send_keys("Test_Admin")
    self.driver.find_element_by_id("password").send_keys("HowlingChihuahua")
    self.driver.find_element_by_id("submit-field").click()
    # List of modules to navigate
    self.modules = ["learning_module/vacuum", 
      "learning_module/planets", 
      "learning_module/satellites", 
      "learning_module/sun",
      ]

  # Tests general navigation through the quiz; ending at the result page.
  def test_quiz_navigation(self):
    for m in self.modules:
      self.driver.get("http://127.0.0.1:5000/{}".format(m))
      self.driver.find_element_by_class_name("start-quiz").click()
      # For each question navigation button (above the question):
      buttons = self.driver.find_elements_by_class_name("qBtn")
      for b in buttons:
        b.click()
      self.driver.find_element_by_id("submit_quiz").click()
      assert "Result" in self.driver.title, "Navigation does not lead to 'Result' page."

# This test is unfortunately unfinished.
# The idea of this test was that we would iterate over each option (4 total),
# selecting it once per question and checking if it was the correct answer.
# After testing each option for each question, if there was a value other than 
# '1' for each key in 'self.answers' we would return as failed.

# As it stands right now, the check button and then the next radio button are return
# "could not be scrolled in to view." Unforunately, even with implicit and webdriver 
#  waits, the issue persists.
  def test_quiz_selection(self):
    for m in self.modules:
      self.driver.get("http://127.0.0.1:5000/{}".format(m))
      self.driver.find_element_by_class_name("start-quiz").click()
      # self.navigate_quiz_selections()

  # Iterates through every selection to check that there is only one correct answer
  # per question.
  def navigate_quiz_selections(self):
    buttons = self.driver.find_elements_by_class_name("qBtn")
    # Dictionary storing number of correct answers found for each question.
    self.answers = {1:0, 2:0, 3:0, 4:0, 5:0}
    # For each option (1-4)
    for option in range(1, 5):
      # for each question (0-5, to account for indexing in buttons array):
      for question in range(0, 5):
      # For each question:
        self.iterate_selections(option, question+1)
        buttons[question].click()
      self.driver.find_element_by_id("submit_quiz").click()
      assert "Result" in self.driver.title
    for answer in self.answers:
      assert answer.value == 1

  # Specifically makes the selection in each test and records answer.
  def iterate_selections(self, option, question):
      self.driver.find_element_by_name("Q{}".format(option)).click()
      WebDriverWait(self.driver, 1).until(EC.element_to_be_clickable((By.ID, "check")))
      self.driver.find_element_by_id("check").click()
      if "correct!" in self.driver.find_element_by_id("msg{}".format(option)).text:
        self.answers[question] += 1

  @classmethod
  def tearDown(self):
    # close the browser window
    self.driver.quit()

if __name__ == '__main__':
  unittest.main()