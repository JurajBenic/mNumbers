import unittest

from mwords.mword import MWord, MWordError


class TestUnarayOperators_3letter_alphabet(unittest.TestCase):
    def setUp(self):
        MWord.set_alphabet('abc')

    def test_D(self):
        _inputs = [
            ('abac', 'cbca'),
            ('baba', 'bcbc'),
            ('ABC', 'ccbbaa'),
            ('abcba', 'cbabc'),
        ]

        for inp, expected in _inputs:
            with self.subTest("Input m-word: {}".format(inp)):
                w = MWord(inp)
                self.assertEqual(w.D.m_word, expected)
        
        w = MWord('abac')
        self.assertEqual(w.D.m_word, 'cbca')

    def test_E(self):
        _inputs = [
            ('abac', 'caba'),
            ('baba', 'abab'),
            ('ABC', 'ccbbaa'),
            ('abcba', 'abcba'),
        ]

        for inp, expected in _inputs:
            with self.subTest("Input m-word: {}".format(inp)):
                w = MWord(inp)
                self.assertEqual(w.E.m_word, expected)

    def test_F(self):
        _inputs = [
            ('abac', 'acbc'),
            ('baba', 'cbcb'),
            ('ABAB', 'bbccbbcc'),
            ('abcba', 'cbabc'),
        ]

        for inp, expected in _inputs:
            with self.subTest("Input m-word: {}".format(inp)):
                w = MWord(inp)
                self.assertEqual(w.F.m_word, expected)


class TestUnarayOperators_5letter_alphabet(unittest.TestCase):
    def setUp(self):
        MWord.set_alphabet('abcde')

    def test_D(self):
        _inputs = [
            ('abacde', 'edecba'),
            ('babad', 'dedeb'),
            ('ABCDE', 'eeddccbbaa'),
            ('abcde', 'edcba'),
        ]

        for inp, expected in _inputs:
            with self.subTest("Input m-word: {}".format(inp)):
                w = MWord(inp)
                self.assertEqual(w.D.m_word, expected)

    def test_E(self):
        _inputs = [
            ('abacde', 'edcaba'),
            ('babad', 'dabab'),
            ('ABCDE', 'eeddccbbaa'),
            ('abcde', 'edcba'),
        ]

        for inp, expected in _inputs:
            with self.subTest("Input m-word: {}".format(inp)):
                w = MWord(inp)
                self.assertEqual(w.E.m_word, expected)

    def test_F(self):
        _inputs = [
            ('abacde', 'abcede'),
            ('babad', 'beded'),
            ('ABCDE', 'aabbccddee'),
            ('abcde', 'abcde'),
        ]

        for inp, expected in _inputs:
            with self.subTest("Input m-word: {}".format(inp)):
                w = MWord(inp)
                self.assertEqual(w.F.m_word, expected)
        


if __name__ == '__main__':
    unittest.main(verbosity=2)