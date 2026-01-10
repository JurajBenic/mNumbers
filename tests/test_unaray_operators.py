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

        for inp, expected in _inputs:
            with self.subTest("Input m_number: {}".format(inp)):
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

        for inp, expected in _inputs:
            with self.subTest("Input m_number: {}".format(inp)):
                m_number = MNumber(inp)
                self.assertEqual(m_number.E.m_word, expected)

    def test_F(self):
        _inputs = [
            ('abac', 'acbc'),
            ('baba', 'cbcb'),
            ('ABAB', 'bbccbbcc'),
            ('abcba', 'cbabc'),
        ]

        for inp, expected in _inputs:
            with self.subTest("Input m_number: {}".format(inp)):
                m_number = MNumber(inp)
                self.assertEqual(m_number.F.m_word, expected)


class TestUnarayOperators_5letter_alphabet(unittest.TestCase):
    def setUp(self):
        MNumber.set_alphabet('abcde')

    def test_D(self):
        _inputs = [
            ('abacde', 'edecba'),
            ('babad', 'dedeb'),
            ('ABCDE', 'eeddccbbaa'),
            ('abcde', 'edcba'),
        ]

        for inp, expected in _inputs:
            with self.subTest("Input m_number: {}".format(inp)):
                m_number = MNumber(inp)
                self.assertEqual(m_number.D.m_word, expected)

    def test_E(self):
        _inputs = [
            ('abacde', 'edcaba'),
            ('babad', 'dabab'),
            ('ABCDE', 'eeddccbbaa'),
            ('abcde', 'edcba'),
        ]

        for inp, expected in _inputs:
            with self.subTest("Input m_number: {}".format(inp)):
                m_number = MNumber(inp)
                self.assertEqual(m_number.E.m_word, expected)

    def test_F(self):
        _inputs = [
            ('abacde', 'abcede'),
            ('babad', 'beded'),
            ('ABCDE', 'aabbccddee'),
            ('abcde', 'abcde'),
        ]

        for inp, expected in _inputs:
            with self.subTest("Input m_number: {}".format(inp)):
                m_number = MNumber(inp)
                self.assertEqual(m_number.F.m_word, expected)
        


if __name__ == '__main__':
    unittest.main(verbosity=2)