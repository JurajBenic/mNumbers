import unittest

from mnumbers.mnumber import MNumber, MNumberError


class TestZip_3letter_alphabet(unittest.TestCase):

    def test_zip_3letters_alphabet(self):
        MNumber.set_alphabet('abc')

        _inputs = [
            ('abac', 'ac'),
            ('baba', 'ba'),
            ('aaaababbbb', 'aabb'),
            ('bcbaac', 'baac'),
            ('ABC', 'aacc'),
        ]

        for inp, expected in _inputs:
            with self.subTest(f"Input m_numbers: {inp}"):
                m_number = MNumber(inp)
                self.assertEqual(m_number.zip().m_word, expected)

