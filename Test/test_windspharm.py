"""Run the test suite for :py:mod:`windspharm`."""
import sys
from unittest import TestSuite, TestLoader, TextTestRunner

import vectorwind_tests
import errorhandling_tests


if __name__ == '__main__':
    tests_to_run = (
            TestLoader().loadTestsFromModule(vectorwind_tests),
            TestLoader().loadTestsFromModule(errorhandling_tests),
    )
    all_tests = TestSuite()
    all_tests.addTests(tests_to_run)
    TextTestRunner(sys.stdout, verbosity=3).run(all_tests)

