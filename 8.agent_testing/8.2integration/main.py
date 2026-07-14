# main.py

import unittest
import integration

if __name__ == "__main__":
    # Load all tests from test_agent.py
    suite = unittest.defaultTestLoader.loadTestsFromModule(integration)

    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)