import unittest
from userTest import UserTest
from homePageTest import HomePageTest
from navigationTest import NavigationTest
from moduleTest import ModuleTest
from quizTest import QuizTest

# get all tests from UserTest and HomePageTest classes
user_test = unittest.TestLoader().loadTestsFromTestCase(UserTest)
home_page_test = unittest.TestLoader().loadTestsFromTestCase(HomePageTest)
navigation_test = unittest.TestLoader().loadTestsFromTestCase(NavigationTest)
module_test = unittest.TestLoader().loadTestsFromTestCase(ModuleTest)
quiz_test = unittest.TestLoader().loadTestsFromTestCase(QuizTest)

# create a test suite combining search_text and home_page_test
test_suite = unittest.TestSuite([home_page_test, user_test, navigation_test, module_test, quiz_test])

# run the suite
unittest.TextTestRunner(verbosity=2).run(test_suite)