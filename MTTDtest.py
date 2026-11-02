import unittest
from unittest.mock import patch, Mock, MagicMock
import MRTD


SAMPLE_INFO = {
    "document_code": "P<",
    "country": "UTO",
    "lastname": "ERIKSSON",
    "name": "ANNA MARIA",
    "passnumber": "L898902C3",
    "nationality": "UTO",
    "birthdate": "740812",
    "sex": "F",
    "expiredate": "120415",
    "personalnumber": "ZE184226B"
}


class TestMRZ(unittest.TestCase):
    def test_encode(self): #test for the encoding function
        line1, line2 = MRTD.encode(SAMPLE_INFO)

        expected_line1 = (
            "P<UTO" + "ERIKSSON<<ANNA<MARIA".ljust(39, "<")
        )

        expected_line2 = (
            "L898902C36UTO7408122F1204159ZE184226B<<<<<10"
        )

        self.assertEqual(line1, expected_line1)
        self.assertEqual(line2, expected_line2)

    def test_encode_line_lengths(self): #ensuring line length is correct
        line1, line2 = MRTD.encode(SAMPLE_INFO)

        self.assertEqual(len(line1), 44)
        self.assertEqual(len(line2), 44)

    def test_decode(self): #testing the decode function
        line1, line2 = MRTD.encode(SAMPLE_INFO)

        info, checkdigits, composite = MRTD.decode(line1, line2)

        self.assertEqual(info["type"], "P<")
        self.assertEqual(info["country"], "UTO")
        self.assertEqual(info["lastname"], "ERIKSSON")
        self.assertEqual(info["name"], "ANNA MARIA")
        self.assertEqual(info["passnumber"], "L898902C3")
        self.assertEqual(info["nationality"], "UTO")
        self.assertEqual(info["birthdate"], "740812")
        self.assertEqual(info["sex"], "F")
        self.assertEqual(info["expiredate"], "120415")
        self.assertEqual(info["personalnumber"], "ZE184226B<<<<<")
        self.assertEqual(checkdigits, ["6", "2", "9", "1"])
        self.assertEqual(composite, "0")

    def test_reportMismatch_valid(self): #test for reportMismatch if there is no mismatch
        checks = [
            "L898902C3",
            "740812",
            "120415",
            "ZE184226B<<<<<"
        ]

        checkdigits = ["6", "2", "9", "1"]

        self.assertTrue(
            MRTD.reportMismatch(checks, checkdigits)
        )
    def test_reportMismatch_invalid(self): #test for reportMismatch if there is a mismatch
        checks = [
            "L898902C3",
            "740812",
            "120415",
            "ZE184226B<<<<<"
        ]

        checkdigits = ["0", "2", "9", "1"]

        self.assertFalse(
            MRTD.reportMismatch(checks, checkdigits)
        )
    
    @patch("MRTD.scanMRZ")
    def test_scanMRZ(self, mock_scan): #test for scan function using mocking
        mock_scan.return_value = ("MRZ_LINE_1", "MRZ_LINE_2")

        result = MRTD.scanMRZ()

        self.assertEqual(
            result,
            ("MRZ_LINE_1", "MRZ_LINE_2")
        )

        mock_scan.assert_called_once()

    @patch("MRTD.accessData")
    def test_generate_mrz(self, mock_database): #test for database access using mocking

        mock_database.return_value = SAMPLE_INFO

        result = MRTD.generate_mrz("12345")

        expected = MRTD.encode(SAMPLE_INFO)

        self.assertEqual(result, expected)

        mock_database.assert_called_once_with("12345")

    @patch("MRTD.accessData")
    def test_generate_mrz_not_found(self, mock_database): #more mocking test if there was an error

        mock_database.return_value = None

        with self.assertRaises(ValueError):
            MRTD.generate_mrz("99999")




if __name__ == '__main__':
    unittest.main()

