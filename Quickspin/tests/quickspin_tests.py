from unittest import TestCase
import unittest
import os
import sys
from coverage import coverage

# initialise coverage, this might need amending d    epending on your environment
cov = coverage(branch=True, omit=['flask/*', 'quickspin_tests.py', '*/Library/*', '/home/travis/virtualenv/*'])
cov.start()

# Add source home into python path and import themonitor.py
mypath = os.path.abspath('..')
sys.path.insert(0,mypath)
from quickspin import create_parser, upIt, downIt, listAllRunning, listRunning

# Make a class that will add the parse from quickspin.py
class CommandLineTestCase(TestCase):
    @classmethod
    def setUp(cls):
        args = create_parser()
        cls.args = args

class QuickspinTestCase(CommandLineTestCase):
    def test_listing_active(self):
        t1 = self.args.parse_args(["-l"])
        self.assertIsNotNone(t1.list)

    def test_listing_all(self):
        testAll = listAllRunning()
        self.assertEqual(True, testAll)

    def test_spin_up(self):
        result = upIt(["i-dcc98560"], DryRun=True)
        self.assertEqual(result, "DryRun")

    def test_spin_down(self):
        result = downIt(["i-dcc98560"], DryRun=True)
        self.assertEqual(result, "DryRun")

if __name__ == '__main__':
    try:
        unittest.main()
    except:
        pass
    cov.stop()
    cov.save()
    print("\n\nCoverage Report:\n")
    cov.report()
    basedir = os.path.join(os.path.dirname(__file__), 'Quickspin')
    print("HTML version: " + os.path.join(basedir, "tmp/coverage/index.html"))
    cov.html_report(directory='tmp/coverage')
    #cov.erase()