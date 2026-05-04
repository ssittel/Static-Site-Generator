import unittest
from gencontents import extract_title

class TestExtractTitle(unittest.TestCase):

    def test_header(self):
        md ="""# This is a h1 header
while this is just some regular text
## and this is an h2"""
        self.assertEqual(extract_title(md), "This is a h1 header")

    def test_2headers(self):
        md ="""# This is a h1 header
while this is just some regular text
# and this is also an h1"""
        self.assertEqual(extract_title(md), "This is a h1 header")

    def test_no_headers(self):
        md = "no headers in this one"
        with self.assertRaises(Exception):
            extract_title(md)

    

