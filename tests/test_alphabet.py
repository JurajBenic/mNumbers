import unittest

from mnumbers.mnumber import MNumber, MNumberError


class TestAlphabet(unittest.TestCase):
    def test_alphabet_3_letesr(self):
        MNumber.set_alphabet('abc')
        self.assertDictEqual(MNumber.val, {"a": 1, "b": 2, "c": 3})
    
    def test_alphabet_3_letters_m_continuum(self):
        MNumber.set_alphabet('abc', m_continuum=True)
        self.assertDictEqual(MNumber.val, {"a": -1, "b": 0, "c": 1})

    def test_alphabet_4_letters(self):
        MNumber.set_alphabet('abcd')
        self.assertDictEqual(MNumber.val, {"a": 1, "b": 2, "c": 3, "d": 4})
    
    def test_alphabet_4_letters_m_continuum(self):
        MNumber.set_alphabet('abcd', m_continuum=True)
        self.assertDictEqual(MNumber.val, {"a": -2, "b": -1, "c": 1, "d": 2})

    def test_alphabet_5_letters(self):
        MNumber.set_alphabet('abcde')
        self.assertDictEqual(MNumber.val, {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5})
    
    def test_alphabet_5_letters_m_continuum(self):
        MNumber.set_alphabet('abcde', m_continuum=True)
        self.assertDictEqual(MNumber.val, {"a": -2, "b": -1, "c": 0, "d": 1, "e": 2})

    def test_alphabet_10_letters(self):
        MNumber.set_alphabet('12345abcde')
        self.assertDictEqual(MNumber.val, {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, "a": 6, "b": 7, "c": 8, "d": 9, "e": 10})

    def test_alphabet_10_letters_m_continuum(self):
        MNumber.set_alphabet('12345abcde', m_continuum=True)
        self.assertDictEqual(MNumber.val, {'1': -5, '2': -4, '3': -3, '4': -2, '5': -1, "a": 1, "b": 2, "c": 3, "d": 4, "e": 5})

    def test_empty_alphabet(self):
        with self.assertRaises(MNumberError):
            MNumber.set_alphabet('')

    def test_non_string_alphabet(self):
        with self.assertRaises(MNumberError):
            MNumber.set_alphabet(123)


if __name__ == '__main__':
    unittest.main(verbosity=2)