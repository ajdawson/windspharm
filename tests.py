import nose


#: Test modules to run by default.
default_test_modules = [
    'windspharm.tests.test_solution',
    'windspharm.tests.test_error_handling',
    'windspharm.tests.test_tools',
]


def run():
    """Run the :mod:`windspharm` test suite."""
    nose.main(defaultTest=default_test_modules)


if __name__ == '__main__':
    run()
