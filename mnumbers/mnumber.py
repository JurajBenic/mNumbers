from typing import Union


class MNumberError(Exception):
    """Exception class for MNumber errors."""
    pass


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
        - Duality: x.D
        - Reversal: x.E
        - Dual-reversal: x.F
        - Zip: x.zip()
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
            m_continuum (bool): If True, values are centered around 0.

        Examples:
            >>> MNumber.set_alphabet('abc')
            >>> MNumber.val['a']
            1
            >>> MNumber.set_alphabet('abcde', m_continuum=True)
            >>> MNumber.val['c']
            0
        """
        
        if not alphabet:
            raise MNumberError("Alphabet can't be empty.")
        if not isinstance(alphabet, str):
            raise MNumberError("Alphabet must be a string.")
        
        if cls.ABC:
            cls.ABC.clear()
            cls.val.clear()
            cls.dual_map.clear()

        seen = set()
        for ch in alphabet.lower():
            if ch not in seen:
                cls.ABC.append(ch)
                seen.add(ch)

        # Create dual map
        cls.dual_map = {ch: cls.ABC[-(i + 1)] for i, ch in enumerate(cls.ABC)}
        
        if m_continuum:
            # arrange numbers from -x to +x
            # if len(cls.ABC) odd then 0 included
            n = len(cls.ABC)
            cls.val = {}
            current = -(n // 2)
            is_even = (n % 2 == 0)
            for ch in cls.ABC:
                if current == 0 and is_even:
                    current += 1
                cls.val[ch] = current
                current += 1
        
        else:
            cls.val = {ch: i + 1 for i, ch in enumerate(cls.ABC)}


    def __init__(self, data: Union['MNumber', str]):
        """
        Initialize an m-number.
            data: string representing the m-number (e.g., 'abac').
        """
        if isinstance(data, MNumber):
            self.m_word = data.U2l
        else:
            self.__check_if_in_alphabet(data)
            self.m_word = data
            self.m_word = self.U2l

    def __str__(self):
        return self.m_word

    def __repr__(self):
        return f"MNumber('{self.m_word}'), quadruple{self.quadruple}"

    # ----------------------------------------------------
    # ------------------ Helper methods ------------------
    # ----------------------------------------------------
    def __check_if_in_alphabet(self, m_word: str):
        for ch in m_word:
            if ch.lower() not in self.ABC:
                raise MNumberError(f"Character '{ch}' not in alphabet.")

    def __distance(self, a1: str, a2: str) -> int:
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
        res = []
        i = 0
        n = len(self.m_word)
        while i < n:
            if i < n - 1 and self.m_word[i] == self.m_word[i+1] and self.m_word[i].islower():
                res.append(self.m_word[i].upper())
                i += 2
            else:
                res.append(self.m_word[i])
                i += 1
        return "".join(res)
    
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
        res = []
        for ch in self.m_word:
            if ch.isupper():
                res.append(ch.lower())
                res.append(ch.lower())
            else:
                res.append(ch)
        return "".join(res)


    @property
    def l(self) -> str:
        """
        Returns the starting symbol (left) of the M-number.

        Returns:
            str: The first character of the M-number.

        Examples:
            >>> MNumber.set_alphabet('abc')
            >>> m = MNumber('abac')
            >>> m.l
            'a'
        """
        return self.m_word[0]

    @property
    def r(self) -> str:
        """
        Returns the ending symbol (right) of the M-number.

        Returns:
            str: The last character of the M-number.

        Examples:
            >>> MNumber.set_alphabet('abc')
            >>> m = MNumber('abac')
            >>> m.r
            'c'
        """
        return self.m_word[-1]
    
    @property
    def q(self) -> str:
        """
        Returns the shell (first + last symbol) of the M-number.

        Returns:
            str: A string containing the first and last characters.

        Examples:
            >>> MNumber.set_alphabet('abc')
            >>> m = MNumber('abac')
            >>> m.q
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

        Returns:
            int: The calculated length.

        Examples:
            >>> MNumber.set_alphabet('abc', m_continuum=True)
            >>> w = MNumber('abcabc')
            >>> w.lmb
            -2
        """
        lam = 0
        sign = -1
        for i in range(len(self.m_word) - 1):
            lam += sign * self.__distance(self.m_word[i], self.m_word[i+1])
            sign = -sign
        return lam

    @property
    def lmb_s(self) -> int:
        """
        Calculates lambda_s (serial component of length).
        Formula: (lambda - defect) / 2

        Returns:
            int: The calculated value.

        Examples:
            >>> MNumber.set_alphabet('abc')
            >>> m = MNumber('abac')
            >>> m.lmb_s
            -2
        """
        return (self.lmb - self.defect) // 2

    @property
    def lmb_p(self) -> int:
        """
        Calculates lambda_p (parallel component of length).
        Formula: (lambda + defect) / 2

        Returns:
            int: The calculated value.

        Examples:
            >>> MNumber.set_alphabet('abc')
            >>> m = MNumber('abac')
            >>> m.lmb_p
            0
        """
        return (self.lmb + self.defect) // 2
    

    @property
    def defect(self) -> int:
        """
        Returns the defect of the M-number.
        Defect is defined as the difference between the values of the starting and ending symbols.

        Returns:
            int: The defect value.

        Examples:
            >>> MNumber.set_alphabet('abc', m_continuum=True)
            >>> m = MNumber('abac')
            >>> m.defect
            2

            >>> MNumber.set_alphabet('abcd')
            >>> m = MNumber('abad')
            >>> m.defect
            3

            >>> MNumber.set_alphabet('abcd', m_continuum=True)
            >>> m = MNumber('abad')
            >>> m.defect
            4
        """
        return self.val[self.r] - self.val[self.l]

    @property
    def quadruple(self) -> tuple[int, int, int, int]:
        """
        Returns the quadruple representation of the M-number.
        The quadruple consists of (value of left symbol, lambda_s, lambda_p, value of right symbol).

        Returns:
            tuple: A tuple containing (val(l), lambda_s, lambda_p, val(r)).

        Examples:
            >>> MNumber.set_alphabet('abc', m_continuum=True)
            >>> m = MNumber('abac')
            >>> m.quadruple
            (-1, -2, 0, 1)
        """
        return (self.val[self.l], self.lmb_s, self.lmb_p, self.val[self.r])

    # ----------------------------------------------------
    # ----------------- Unary operators ------------------
    # ----------------------------------------------------
    @property
    def D(self) -> 'MNumber':
        """
        Returns the dual M-number (duality operator).
        Creates a new MNumber with the m_word transformed to its dual.

        Returns:
            MNumber: A new MNumber instance with dual m_word.

        Examples:
            >>> MNumber.set_alphabet('abc')
            >>> m = MNumber('abac')
            >>> m.D.m_word
            'cbca'
        """
        dual_word = ''.join(self.dual_map[ch] for ch in self.m_word)
        return MNumber(dual_word)

    @property
    def E(self) -> 'MNumber':
        """
        Returns the reversed M-number (reversal operator).
        Creates a new MNumber with the m_word reversed.

        Returns:
            MNumber: A new MNumber instance with reversed m_word.

        Examples:
            >>> MNumber.set_alphabet('abc')
            >>> m = MNumber('abac')
            >>> m.E.m_word
            'caba'
        """
        return MNumber(self.m_word[::-1])
    
    @property
    def F(self) -> 'MNumber':
        """
        Returns the dual-reversed M-number (duality + reversal operator).
        Creates a new MNumber with the m_word transformed to its dual and then reversed.

        Returns:
            MNumber: A new MNumber instance with dual-reversed m_word.

        Examples:
            >>> MNumber.set_alphabet('abc')
            >>> m = MNumber('abac')
            >>> m.F.m_word
            'acbc'
        """
        return self.D.E
    

    # ----------------------------------------------------
    # ------------------- Permutations -------------------
    # ----------------------------------------------------
    @property
    def I(self) -> 'MNumber':
        """
        Returns the invertibility permutation of the M-number.
        Prepends the left symbol and appends the right symbol to create a new M-number.

        Returns:
            MNumber: A new MNumber instance with boundary symbols added.

        Examples:
            >>> MNumber.set_alphabet('abc')
            >>> m = MNumber('ab')
            >>> m.I.m_word
            'aabb'
        """
        return MNumber(self.l + self.m_word + self.r)
    
    @property
    def K(self) -> 'MNumber':
        """
        Returns the complement M-number (complement operator).
        Creates a new MNumber with the m_word transformed to its complement.

        Returns:
            MNumber: A new MNumber instance with complement m_word.
        
        Examples:
            >>> MNumber.set_alphabet('abcdef')
            >>> m = MNumber('ab')
            >>> m.K.m_word
            'fabe'
        """
        return MNumber(self.dual_map[self.l] + self.m_word + self.dual_map[self.r])
    
    # ----------------------------------------------------
    # --------------- Logical operations -----------------
    # ----------------------------------------------------    
    def __or__(self, m_number: 'MNumber') -> 'MNumber':
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
        _prefix = max(self.l, m_number.l) + max(self.l, m_number.l)
        _infix = min(self.r, m_number.l) + max(self.r, m_number.l)
        _sufix = min(self.r, m_number.r) + min(self.r, m_number.r)
        
        return MNumber(_prefix + self.m_word + _infix + m_number.m_word + _sufix)

    def __and__(self, m_number: 'MNumber') -> 'MNumber':
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
        _prefix = min(self.l, m_number.l) + min(self.l, m_number.l)
        _infix = max(self.r, m_number.l) + min(self.r, m_number.l)
        _sufix = max(self.r, m_number.r) + max(self.r, m_number.r)

        return MNumber(_prefix + self.m_word + _infix + m_number.m_word + _sufix)

    def __invert__(self) -> 'MNumber':
        """
        Negation operation (NOT logical function).
        Returns the dual of the M-number.

        Examples:
            >>> MNumber.set_alphabet('abcdef')
            >>> m = MNumber('ab')
            >>> (~m).m_word
            'fabe'
        """
        return self.K

    # ----------------------------------------------------
    # ------------------ Zip helpers ---------------------
    # ----------------------------------------------------
    def _lambda_word(self, w: str) -> int:
        """
        λ(a1...ak) = -d12 + d23 - d34 + ...
        """
        if len(w) < 2:
            return 0

        total = 0
        sign = -1

        for i in range(len(w) - 1):
            total += sign * self.__distance(w[i], w[i + 1])
            sign *= -1

        return total

    @property
    def zip(self) -> 'MNumber':
        """
        Performs the zip operation on the M-number.
        Reduces the m-word based on distance properties.
        
        Returns:
            MNumber: A new MNumber instance with the zipped m-word.
            
        Examples:
            >>> MNumber.set_alphabet('abc')
            >>> m = MNumber('abac')
            >>> m.zip.m_word
            'ac'
            >>> m = MNumber('baba')
            >>> m.zip.m_word
            'ba'
            >>> m = MNumber('aaaababbbb')
            >>> m.zip.m_word
            'aabb'
            >>> m = MNumber('bcbaac')
            >>> m.zip.m_word
            'baac'
            >>> m = MNumber('ABC')
            >>> m.zip.m_word
            'aacc'
        """
        jorb = self.m_word

        pos = {ch: i for i, ch in enumerate(self.ABC)}                 # slovo -> pozicija u alfabetu
        val_by_pos = [self.val[ch] for ch in self.ABC]                 # pozicija -> numerička valuacija (za δ)

        def delta(p1: int, p2: int) -> int:
            return abs(val_by_pos[p1] - val_by_pos[p2])

        def reduce_stack(st: list[int]) -> None:
            # ponavljaj zip3 / zip4 dok god se nešto može smanjiti na repu
            while True:
                changed = False

                # zip3: a b a -> a
                if len(st) >= 3 and st[-3] == st[-1]:
                    st.pop()
                    st.pop()
                    changed = True

                # zip4: a b c d -> a d ako vrijedi Šare uvjet (Theorem 1 / pravilo (6))
                if len(st) >= 4:
                    A, B, C, D = st[-4], st[-3], st[-2], st[-1]
                    left = delta(A, B) - delta(B, C) + delta(C, D)
                    right = delta(A, D)
                    if left == right:
                        # izbaci B i C
                        del st[-3:-1]
                        changed = True

                if not changed:
                    break

        def compress(word: str, do_ext: bool) -> str:
            if len(word) <= 2:
                return word

            st: list[int] = []

            p_prev = pos[word[0]]
            st.append(p_prev)

            for ch in word[1:]:
                p_cur = pos[ch]

                if do_ext:
                    # lazy ext: emitira međuslove kao "xx" (dva puta isti)
                    if p_prev + 1 < p_cur:  # rastući gap
                        for k in range(p_prev + 1, p_cur):
                            st.append(k); st.append(k)
                            reduce_stack(st)
                    elif p_prev > p_cur + 1:  # padajući gap
                        for k in range(p_prev - 1, p_cur, -1):
                            st.append(k); st.append(k)
                            reduce_stack(st)

                st.append(p_cur)
                reduce_stack(st)
                p_prev = p_cur

            return "".join(self.ABC[p] for p in st)

        def rvs(word: str) -> list[str]:
            n = len(word)
            out = []
            seen = set()
            for i in range(n - 1):
                for j in range(n - 1, i + 1, -1):
                    if ((j - i) % 2 == 1) and (word[i] == word[j]):
                        mid = word[i+1:j]
                        if mid and mid != mid[::-1]:
                            cand = word[:i+1] + mid[::-1] + word[j:]
                            if cand not in seen:
                                seen.add(cand)
                                out.append(cand)
            return out

        # Glavna petlja kao u Algoritmu 2: ext→zip4→zip3, pa rvs, pa zip4→zip3
        while True:
            w1 = compress(jorb, do_ext=True)        # zip3(zip4(ext()))
            jorb = w1

            candidates = rvs(w1)
            smaller = False
            for w2 in candidates:
                w3 = compress(w2, do_ext=False)     # zip3(zip4()) (bez ext), kao u pdf-u
                if len(w3) == len(w1):
                    continue
                jorb = w3
                smaller = True
                break

            if not smaller:
                break

        return MNumber(jorb)


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)