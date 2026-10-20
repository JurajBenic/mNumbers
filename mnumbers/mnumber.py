import re
from typing import Union


class MNumberError(Exception):
    """Exception class for MNumber errors."""


class MNumber:
    """
    A class for representing M-numbers (mathematical objects with algebraic structure).

    M-numbers are sequences of symbols from a defined alphabet with associated operations
    including serial (&) and parallel (|) connections, as well as unary operators (D, E, F).

    Class Attributes:
        ABC (list): The alphabet used for all MNumber instances.
        val (dict): Maps each character in the alphabet to its numerical value.
        dual_map (dict): Maps each character to its dual in the alphabet.

    Instance Attributes:
        m_word (str): The internal lowercase representation of the M-number.

    Main Operations:
        - Serial connection: x & y
        - Parallel connection: x | y
        - Negation (complement): ~x
        - Duality: x.D
        - Reversal: x.E
        - Dual-reversal: x.F
        - Invertibility: x.I
        - Complement: x.K
        - Zip: x.zip
    """
    ABC = []
    val = {}
    dual_map = {}

    @classmethod
    def set_alphabet(cls, alphabet: str, m_continuum: bool = False):
        """
        Set the alphabet for all MNumber instances.

        Args:
            alphabet (str): A string containing the characters of the alphabet.
                Duplicates are ignored and letters are lowercased.
            m_continuum (bool): If True, values are centered around 0
                (0 is included only for an odd-sized alphabet).

        Examples:
            >>> MNumber.set_alphabet('abc')
            >>> MNumber.val['a']
            1
            >>> MNumber.set_alphabet('abcde', m_continuum=True)
            >>> MNumber.val['c']
            0
            >>> MNumber.set_alphabet('abcd', m_continuum=True)
            >>> MNumber.val
            {'a': -2, 'b': -1, 'c': 1, 'd': 2}
        """
        if not alphabet:
            raise MNumberError("Alphabet can't be empty.")
        if not isinstance(alphabet, str):
            raise MNumberError("Alphabet must be a string.")

        # Update the list in place so existing references to MNumber.ABC stay valid.
        cls.ABC[:] = dict.fromkeys(alphabet.lower())
        n = len(cls.ABC)

        if m_continuum:
            values = [v for v in range(-(n // 2), n // 2 + 1) if v != 0 or n % 2]
        else:
            values = range(1, n + 1)

        cls.val = dict(zip(cls.ABC, values))
        cls.dual_map = dict(zip(cls.ABC, reversed(cls.ABC)))

    def __init__(self, data: Union['MNumber', str]):
        """
        Initialize an M-number.

        Args:
            data: Another MNumber, or a string representing the M-number in
                lowercase or uppercase notation (e.g. 'abac' or 'AbC').
        """
        if isinstance(data, MNumber):
            self.m_word = data.m_word
        else:
            for ch in data:
                if ch.lower() not in self.ABC:
                    raise MNumberError(f"Character '{ch}' not in alphabet.")
            self.m_word = self._to_lowercase_notation(data)

    def __str__(self):
        return self.m_word

    def __repr__(self):
        return f"MNumber('{self.m_word}'), quadruple{self.quadruple}"

    # ----------------------------------------------------
    # ------------------ Helper methods ------------------
    # ----------------------------------------------------
    @staticmethod
    def _to_lowercase_notation(word: str) -> str:
        """Expand every uppercase letter into a pair of lowercase letters."""
        return "".join(ch.lower() * 2 if ch.isupper() else ch for ch in word)

    def _distance(self, a1: str, a2: str) -> int:
        """Distance δ between two letters of the alphabet."""
        return abs(self.val[a1] - self.val[a2])

    # ----------------------------------------------------
    # -------------------- Properties --------------------
    # ----------------------------------------------------
    @property
    def l2U(self) -> str:
        """
        Converts the M-number to uppercase notation.
        Transforms pairs of identical consecutive lowercase letters into a single uppercase letter.

        Returns:
            str: The M-number in uppercase notation.

        Examples:
            >>> MNumber.set_alphabet('abc')
            >>> m = MNumber('aaaaabbb')
            >>> m.l2U
            'AAaBb'
        """
        return re.sub(r"(.)\1",
                      lambda m: m[1].upper() if m[1].islower() else m[0],
                      self.m_word)

    @property
    def U2l(self) -> str:
        """
        Converts the M-number from uppercase notation to lowercase notation.
        Transforms uppercase letters into pairs of identical lowercase letters.

        Returns:
            str: The M-number in lowercase notation.

        Examples:
            >>> MNumber.set_alphabet('abc')
            >>> m = MNumber('AAaBb')
            >>> m.U2l
            'aaaaabbb'
        """
        return self._to_lowercase_notation(self.m_word)

    @property
    def l(self) -> str:
        """
        Returns the starting symbol (left) of the M-number.

        Examples:
            >>> MNumber.set_alphabet('abc')
            >>> MNumber('abac').l
            'a'
        """
        return self.m_word[0]

    @property
    def r(self) -> str:
        """
        Returns the ending symbol (right) of the M-number.

        Examples:
            >>> MNumber.set_alphabet('abc')
            >>> MNumber('abac').r
            'c'
        """
        return self.m_word[-1]

    @property
    def q(self) -> str:
        """
        Returns the shell (first + last symbol) of the M-number.

        Examples:
            >>> MNumber.set_alphabet('abc')
            >>> MNumber('abac').q
            'ac'
        """
        return self.l + self.r

    @property
    def lmb(self) -> int:
        """
        Calculates the length of the m-word (lambda), characterizing its "waviness".
        It is the alternating sum of distances between adjacent letters, starting with a negative sign.

        Formula:
            λ(w) = -δ(a1, a2) + δ(a2, a3) - ...

        Examples:
            >>> MNumber.set_alphabet('abc', m_continuum=True)
            >>> MNumber('abcabc').lmb
            -2
        """
        w = self.m_word
        return sum((-1) ** (i + 1) * self._distance(w[i], w[i + 1])
                   for i in range(len(w) - 1))

    @property
    def lmb_s(self) -> int:
        """
        Calculates lambda_s (serial component of length).
        Formula: (lambda - defect) / 2

        Examples:
            >>> MNumber.set_alphabet('abc')
            >>> MNumber('abac').lmb_s
            -2
        """
        return (self.lmb - self.defect) // 2

    @property
    def lmb_p(self) -> int:
        """
        Calculates lambda_p (parallel component of length).
        Formula: (lambda + defect) / 2

        Examples:
            >>> MNumber.set_alphabet('abc')
            >>> MNumber('abac').lmb_p
            0
        """
        return (self.lmb + self.defect) // 2

    @property
    def defect(self) -> int:
        """
        Returns the defect of the M-number: the value of the ending symbol
        minus the value of the starting symbol.

        Examples:
            >>> MNumber.set_alphabet('abc', m_continuum=True)
            >>> MNumber('abac').defect
            2

            >>> MNumber.set_alphabet('abcd')
            >>> MNumber('abad').defect
            3

            >>> MNumber.set_alphabet('abcd', m_continuum=True)
            >>> MNumber('abad').defect
            4
        """
        return self.val[self.r] - self.val[self.l]

    @property
    def quadruple(self) -> tuple[int, int, int, int]:
        """
        Returns the quadruple (val(l), lambda_s, lambda_p, val(r)) of the M-number.

        Examples:
            >>> MNumber.set_alphabet('abc', m_continuum=True)
            >>> MNumber('abac').quadruple
            (-1, -2, 0, 1)
        """
        return (self.val[self.l], self.lmb_s, self.lmb_p, self.val[self.r])

    # ----------------------------------------------------
    # ----------------- Unary operators ------------------
    # ----------------------------------------------------
    @property
    def D(self) -> 'MNumber':
        """
        Returns the dual M-number (duality operator):
        every letter is replaced by its dual.

        Examples:
            >>> MNumber.set_alphabet('abc')
            >>> MNumber('abac').D.m_word
            'cbca'
        """
        return MNumber(''.join(self.dual_map[ch] for ch in self.m_word))

    @property
    def E(self) -> 'MNumber':
        """
        Returns the reversed M-number (reversal operator).

        Examples:
            >>> MNumber.set_alphabet('abc')
            >>> MNumber('abac').E.m_word
            'caba'
        """
        return MNumber(self.m_word[::-1])

    @property
    def F(self) -> 'MNumber':
        """
        Returns the dual-reversed M-number (duality followed by reversal).

        Examples:
            >>> MNumber.set_alphabet('abc')
            >>> MNumber('abac').F.m_word
            'acbc'
        """
        return self.D.E

    # ----------------------------------------------------
    # ------------------- Permutations -------------------
    # ----------------------------------------------------
    @property
    def I(self) -> 'MNumber':
        """
        Returns the invertibility permutation of the M-number:
        the left symbol is prepended and the right symbol is appended.

        Examples:
            >>> MNumber.set_alphabet('abc')
            >>> MNumber('ab').I.m_word
            'aabb'
        """
        return MNumber(self.l + self.m_word + self.r)

    @property
    def K(self) -> 'MNumber':
        """
        Returns the complement M-number (complement operator):
        the dual of the left symbol is prepended and
        the dual of the right symbol is appended.

        Examples:
            >>> MNumber.set_alphabet('abcdef')
            >>> MNumber('ab').K.m_word
            'fabe'
        """
        return MNumber(self.dual_map[self.l] + self.m_word + self.dual_map[self.r])

    # ----------------------------------------------------
    # --------------- Logical operations -----------------
    # ----------------------------------------------------
    def __or__(self, y: 'MNumber') -> 'MNumber':
        """
        Parallel connection (OR logical function).

        Formula:
        max(l(x),l(y)) + max(l(x),l(y)) + x + min(d(x),l(y)) + max(d(x),l(y)) + y + min(d(x),d(y)) + min(d(x),d(y))

        Theory examples:
        aa | bb = b b aa a b bb a a = bbaaabbbaa
        bb | aa = b b bb a b aa a a = bbbbabaaaa

        Examples:
            >>> MNumber.set_alphabet('abc')
            >>> m1 = MNumber('aa')
            >>> m2 = MNumber('bb')
            >>> (m1 | m2).m_word
            'bbaaabbbaa'
            >>> (m2 | m1).m_word
            'bbbbabaaaa'
        """
        x = self
        return MNumber(2 * max(x.l, y.l) + x.m_word
                       + min(x.r, y.l) + max(x.r, y.l)
                       + y.m_word + 2 * min(x.r, y.r))

    def __and__(self, y: 'MNumber') -> 'MNumber':
        """
        Serial connection (AND logical function).

        Formula:
        min(l(x),l(y)) + min(l(x),l(y)) + x + max(d(x),l(y)) + min(d(x),l(y)) + y + max(d(x),d(y)) + max(d(x),d(y))

        Theory examples:
        aa & bb = a a aa b a bb b b = aaaababbbb
        bb & aa = a a bb b a aa b b = aabbbaaabb

        Examples:
            >>> MNumber.set_alphabet('abc')
            >>> m1 = MNumber('aa')
            >>> m2 = MNumber('bb')
            >>> (m1 & m2).m_word
            'aaaababbbb'
            >>> (m2 & m1).m_word
            'aabbbaaabb'
        """
        x = self
        return MNumber(2 * min(x.l, y.l) + x.m_word
                       + max(x.r, y.l) + min(x.r, y.l)
                       + y.m_word + 2 * max(x.r, y.r))

    def __invert__(self) -> 'MNumber':
        """
        Negation operation (NOT logical function).
        Returns the complement of the M-number (see K).

        Examples:
            >>> MNumber.set_alphabet('abcdef')
            >>> (~MNumber('ab')).m_word
            'fabe'
        """
        return self.K

    # ----------------------------------------------------
    # ----------------------- Zip ------------------------
    # ----------------------------------------------------
    @property
    def zip(self) -> 'MNumber':
        """
        Performs the zip operation on the M-number.
        Reduces the m-word to its shortest equivalent form (Algorithm 2):
        ext → zip4 → zip3, then rvs → zip4 → zip3, repeated until
        no reversal yields a shorter word.

        Returns:
            MNumber: A new MNumber instance with the zipped m-word.

        Examples:
            >>> MNumber.set_alphabet('abc')
            >>> MNumber('abac').zip.m_word
            'ac'
            >>> MNumber('baba').zip.m_word
            'ba'
            >>> MNumber('aaaababbbb').zip.m_word
            'aabb'
            >>> MNumber('bcbaac').zip.m_word
            'baac'
            >>> MNumber('ABC').zip.m_word
            'aacc'
        """
        # Letters are handled by their position in the alphabet.
        pos = {ch: i for i, ch in enumerate(self.ABC)}
        val_by_pos = [self.val[ch] for ch in self.ABC]

        def delta(p1: int, p2: int) -> int:
            return abs(val_by_pos[p1] - val_by_pos[p2])

        def reduce_stack(st: list[int]) -> None:
            """Apply zip3 / zip4 to the end of the stack while possible."""
            while True:
                if len(st) >= 3 and st[-3] == st[-1]:
                    # zip3: a b a -> a
                    del st[-2:]
                elif len(st) >= 4 and (delta(st[-4], st[-3]) - delta(st[-3], st[-2])
                                       + delta(st[-2], st[-1]) == delta(st[-4], st[-1])):
                    # zip4: a b c d -> a d (Šare condition, Theorem 1 / rule (6))
                    del st[-3:-1]
                else:
                    break

        def compress(word: str, do_ext: bool) -> str:
            """zip3(zip4(word)), optionally preceded by ext."""
            if len(word) <= 2:
                return word

            st = [pos[word[0]]]
            for ch in word[1:]:
                p_prev, p_cur = st[-1], pos[ch]
                if do_ext:
                    # Lazy ext: fill every gap in the alphabet with doubled
                    # intermediate letters ("xx").
                    step = 1 if p_cur > p_prev else -1
                    for k in range(p_prev + step, p_cur, step):
                        st += [k, k]
                        reduce_stack(st)
                st.append(p_cur)
                reduce_stack(st)

            return "".join(self.ABC[p] for p in st)

        def rvs(word: str):
            """Yield distinct words obtained by reversing a non-palindromic
            infix of even length that lies between two equal letters."""
            n = len(word)
            seen = set()
            for i in range(n - 1):
                for j in range(n - 1, i + 1, -1):
                    if (j - i) % 2 == 1 and word[i] == word[j]:
                        mid = word[i + 1:j]
                        if mid != mid[::-1]:
                            cand = word[:i + 1] + mid[::-1] + word[j:]
                            if cand not in seen:
                                seen.add(cand)
                                yield cand

        word = self.m_word
        while True:
            word = compress(word, do_ext=True)
            for cand in rvs(word):
                shorter = compress(cand, do_ext=False)
                if len(shorter) != len(word):
                    word = shorter
                    break
            else:
                return MNumber(word)


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
