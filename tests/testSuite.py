import unittest
from databaseTest import DatabaseTest
from userTest import UserTest
from homePageTest import HomePageTest
from navigationTest import NavigationTest
from moduleTest import ModuleTest
from quizTest import QuizTest
# get all tests from UserTest and HomePageTest classes
database_test = unittest.TestLoader().loadTestsFromTestCase(DatabaseTest)
user_test = unittest.TestLoader().loadTestsFromTestCase(UserTest)
home_page_test = unittest.TestLoader().loadTestsFromTestCase(HomePageTest)
navigation_test = unittest.TestLoader().loadTestsFromTestCase(NavigationTest)
module_test = unittest.TestLoader().loadTestsFromTestCase(ModuleTest)
quiz_test = unittest.TestLoader().loadTestsFromTestCase(QuizTest)

# Please note that the quiz_test is not currently implemented due to some 
# last-minute issues. See quizTest.py or the README for more information.

# create a test suite combining search_text and home_page_test
test_suite = unittest.TestSuite([database_test, home_page_test, user_test, navigation_test, module_test])

# run the suite
unittest.TextTestRunner(verbosity=2).run(test_suite)