# Running Tests

To run all tests, navigate to the project root folder and execute the following command:

```bash
python -m unittest discover -s tests -v
```

This will discover and run all test files in the `tests` directory with verbose output.

## Available Tests

### alphabet_test.py
- `test_alphabet_3_letesr` - Tests 3-letter alphabet with standard numbering
- `test_alphabet_3_letters_m_continuum` - Tests 3-letter alphabet with M-continuum numbering
- `test_alphabet_4_letters` - Tests 4-letter alphabet with standard numbering
- `test_alphabet_4_letters_m_continuum` - Tests 4-letter alphabet with M-continuum numbering
- `test_alphabet_5_letters` - Tests 5-letter alphabet with standard numbering
- `test_alphabet_5_letters_m_continuum` - Tests 5-letter alphabet with M-continuum numbering
- `test_alphabet_10_letters` - Tests 10-character alphabet with standard numbering
- `test_alphabet_10_letters_m_continuum` - Tests 10-character alphabet with M-continuum numbering
- `test_empty_alphabet` - Tests error handling for empty alphabet
- `test_non_string_alphabet` - Tests error handling for non-string alphabet input