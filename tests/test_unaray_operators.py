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

    def test_E(self):
        _inputs = [
            ('abac', 'caba'),
            ('baba', 'abab'),
            ('ABC', 'ccbbaa'),
            ('abcba', 'abcba'),
        ]

        with self.subTest():
            for inp, expected in _inputs:
                m_number = MNumber(inp)
                self.assertEqual(m_number.E.m_word, expected)

    def test_F(self):
        _inputs = [
            ('abac', 'acbc'),
            ('baba', 'cbcb'),
            ('ABAB', 'bbccbbcc'),
            ('abcba', 'cbabc'),
        ]

        with self.subTest():
            for inp, expected in _inputs:
                m_number = MNumber(inp)
                self.assertEqual(m_number.F.m_word, expected)
        


if __name__ == '__main__':
    unittest.main(verbosity=2)