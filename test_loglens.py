import unittest
from loglens import analyze

class LogLensTests(unittest.TestCase):
    def test_counts(self):
        r = analyze(["INFO Ready", "WARN Disk", "ERROR: Timeout", "ERROR: Timeout", "\n"])
        self.assertEqual(r["lines"], 4)
        self.assertEqual(r["levels"], {"ERROR": 2, "INFO": 1, "WARNING": 1})
        self.assertEqual(r["top_errors"], [{"message": "Timeout", "count": 2}])

    def test_unknown_and_empty(self):
        self.assertEqual(analyze(["plain text"])["levels"], {"UNKNOWN": 1})
        self.assertEqual(analyze([])["lines"], 0)

    def test_limit(self):
        self.assertEqual(len(analyze(["ERROR x", "ERROR y"], 1)["top_errors"]), 1)

if __name__ == "__main__": unittest.main()
