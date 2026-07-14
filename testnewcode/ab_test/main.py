# main.py

import unittest
import test_agent

if __name__ == "__main__":
    # Load all tests from test_agent.py
    suite = unittest.defaultTestLoader.loadTestsFromModule(test_agent)

    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)