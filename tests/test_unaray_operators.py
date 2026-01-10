import unittest

from mnumbers.mnumber import MNumber, MNumberError


class TestUnarayOperators_3letter_alphabet(unittest.TestCase):
    def setUp(self):
        MNumber.set_alphabet('abc')

    def test_D(self):
        _inputs = [
            ('abac', 'cbca'),
            ('baba', 'bcbc'),
            ('ABC', 'ccbbaa'),
            ('abcba', 'cbabc'),
        ]

        with self.subTest():
            for inp, expected in _inputs:
                m_number = MNumber(inp)
                self.assertEqual(m_number.D.m_word, expected)
        
        m_number = MNumber('abac')
        self.assertEqual(m_number.D.m_word, 'cbca')
        


if __name__ == '__main__':
    unittest.main(verbosity=2)