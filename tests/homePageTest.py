import unittest, os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from selenium import webdriver

# Flask server is required to be running. User terminates server.

class HomePageTest(unittest.TestCase):
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

  # Ensures that all routes related to home redirect there.
  def test_all_routes(self):
    assert "Home" in self.driver.title, "Not all appropriate routes lead to home."
    self.driver.get("http://127.0.0.1:5000/index")
    assert "Home" in self.driver.title, "Not all appropriate routes lead to home."
    self.driver.get("http://127.0.0.1:5000/home")
    assert "Home" in self.driver.title, "Not all appropriate routes lead to home."

  # Tests that, when on the home page, all necessary elements are present.
  def test_expected_elements_present(self):
    carousel = self.driver.find_element_by_id("home_carousel")
    assert carousel != None, "Carousel not present."
    slides = carousel.find_element_by_id("slides")    
    assert slides != None, "Slides not present."
    leftButton = carousel.find_element_by_class_name("left")
    rightButton = carousel.find_element_by_class_name("right")
    assert leftButton != None, "Carousel left button not present."
    assert rightButton != None, "Carousel right button not present."
    slide = slides.find_elements_by_class_name("slide")
    assert len(slide) == 4, "Appropriate number of slides not present."
    mainContent = self.driver.find_element_by_id("main_content")
    assert mainContent != None, "Main Content not present."

  # Tests that, when on the home page AND authorizsed, all necessary 
  # elements are present.
  def test_modules_present_for_authorised_user(self):
    self.login()
    modules = ["The Vacuum of Space", "The Planets", "Satellites", "The Sun"]
    for m in modules:
      assert self.driver.find_element_by_id(m), "Modules not present."

  @classmethod
  def tearDown(self):
    # close the browser window
    self.driver.quit()

if __name__ == '__main__':
  unittest.main()