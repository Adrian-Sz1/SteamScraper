import unittest
from io import StringIO
import sys
import main
from main import BColors


class ScrapeUnitTests(unittest.TestCase):

    def ToExcel_NoData_displayError(self):
        main.currentGameData = None

        capturedOutput = StringIO.StringIO()  # Create StringIO object
        sys.stdout = capturedOutput  # and redirect stdout.
        actualOutput = main.convertToExcel()  # Call unchanged function.
        sys.stdout = sys.__stdout__  # Reset redirect.

        expectedConsoleOutput = BColors.WARNING("No data detected. Create a new scrape event first.", True)
        expectedBoolOutput = False
        actualOutput = main.convertToExcel()

        self.assertEquals(expectedConsoleOutput, actualOutput)
        self.assertFalse(actualOutput, expectedBoolOutput)


if __name__ == '__Tests__':
    unittest.main()

