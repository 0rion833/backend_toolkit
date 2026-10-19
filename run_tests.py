"""Run the test suite from the repository root."""
import os, sys, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
suite = unittest.defaultTestLoader.discover(os.path.join(os.path.dirname(__file__), "tests"))
result = unittest.TextTestRunner(verbosity=2).run(suite)
raise SystemExit(not result.wasSuccessful())
