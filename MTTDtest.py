import unittest
from unittest.mock import patch, MagicMock
import MRTD

class TestScanner(unittest.TestCase):
    @patch('MRTD.scanMRZ')
    @patch('MRTD.accessData')
    def testMRZ(self):
        pass

    def testEncoding(self):
        pass

    def testDecoding(self):
        pass

    def testMismatch(self):
        pass


if __name__ == '__main__':
    unittest.main()

