import unittest
from userTest import UserTest
from homePageTest import HomePageTest

# get all tests from UserTest and HomePageTest classes
user_test = unittest.TestLoader().loadTestsFromTestCase(UserTest)
home_page_test = unittest.TestLoader().loadTestsFromTestCase(HomePageTest)

# create a test suite combining search_text and home_page_test
test_suite = unittest.TestSuite([home_page_test, user_test])

# run the suite
unittest.TextTestRunner(verbosity=2).run(test_suite)