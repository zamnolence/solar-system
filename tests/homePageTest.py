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

  def test_all_routes(self):
    assert "Home" in self.driver.title
    self.driver.get("http://127.0.0.1:5000/index")
    assert "Home" in self.driver.title
    self.driver.get("http://127.0.0.1:5000/home")
    assert "Home" in self.driver.title

  def test_expected_elements_present(self):
    carousel = self.driver.find_element_by_id("home_carousel")
    assert carousel != None
    slides = carousel.find_element_by_id("slides")    
    assert slides != None
    leftButton = carousel.find_element_by_class_name("left")
    rightButton = carousel.find_element_by_class_name("right")
    assert leftButton != None
    assert rightButton != None
    slide = slides.find_elements_by_name("slide")
    assert len(slide) == 4

    mainContent = self.driver.find_element_by_id("main_content")
    assert mainContent != None

  @classmethod
  def tearDown(self):
    # close the browser window
    self.driver.quit()

if __name__ == '__main__':
  unittest.main()