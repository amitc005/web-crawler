import unittest

test_suites = unittest.TestLoader().discover("src/tests", pattern="test_*.py")

unittest.TextTestRunner(verbosity=2).run(test_suites).wasSuccessful()
