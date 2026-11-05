import unittest

from mwords.mword import MWord, MWordError


class TestCompress_3letter_alphabet(unittest.TestCase):

    def test_compress_3letters_alphabet(self):
        MWord.set_alphabet('abc')

        _inputs = [
            ('abac', 'ac'),
            ('baba', 'ba'),
            ('aaaababbbb', 'aabb'),
            ('bcbaac', 'baac'),
            ('ABC', 'aacc'),
        ]

        for inp, expected in _inputs:
            with self.subTest(f"Input m-word: {inp}"):
                w = MWord(inp)
                self.assertEqual(w.compress().m_word, expected)

