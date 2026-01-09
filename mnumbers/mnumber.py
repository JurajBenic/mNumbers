

class MNumberError(Exception):
    """Exception class for MNumber errors."""
    pass


class MNumber:
    """
    Klasa za reprezentaciju m-broja.
    Podržava serijske (s) i paralelne (p) operacije.
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


    def __init__(self, data: str):
        """
        Initialize an m-number.
        data: string representing the m-number (e.g., 'abac').
        """
        if isinstance(data, MNumber):
            self.m_word = self._upper2lowwer(data.m_word)
        else:
            self.__check_if_in_alfabet(data)
            self.m_word = self._upper2lowwer(str(data))

    def __str__(self):
        return self.m_word

    def __repr__(self):
        return f"MNumber('{self.m_word}'), ({self.val[self.l]}, {self.lmb_s}, {self.lmb_p} {self.val[self.r]})"

    # ----------------------------------------------------
    # ------------------ Helper methods ------------------
    # ----------------------------------------------------
    def __check_if_in_alfabet(self, m_word: str):
        for ch in m_word:
            if ch.lower() not in self.ABC:
                raise MNumberError(f"Character '{ch}' not in alphabet.")

    def _distance(self, a1, a2):
        return abs(self.val[a1] - self.val[a2])

    def _lowwer2upper(self, m_word: str):
        """
        Convert two lowercase letters to uppercase.

        Examples:
            >>> MNumber.set_alphabet('abc')
            >>> m = MNumber('a')
            >>> m._lowwer2upper('aaaaabbb')
            'AAaBb'
        """
        res = []
        i = 0
        n = len(m_word)
        while i < n:
            if i < n - 1 and m_word[i] == m_word[i+1] and m_word[i].islower():
                res.append(m_word[i].upper())
                i += 2
            else:
                res.append(m_word[i])
                i += 1
        return "".join(res)

    def _upper2lowwer(self, m_word: str):
        """
        Convert uppercase letters to two lowercase letters.

        Examples:
            >>> MNumber.set_alphabet('abc')
            >>> m = MNumber('a')
            >>> m._upper2lowwer('AAaBb')
            'aaaaabbb'
        """
        res = []
        for ch in m_word:
            if ch.isupper():
                res.append(ch.lower())
                res.append(ch.lower())
            else:
                res.append(ch)
        return "".join(res)

    # ----------------------------------------------------
    # ------------------ Properties ------------------
    # ----------------------------------------------------
    @property
    def l(self):
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
    def r(self):
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
    def q(self):
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
    def lmb(self):
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
            lam += sign * self._distance(self.m_word[i], self.m_word[i+1])
            sign = -sign
        return lam

    @property
    def lmb_s(self):
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
    def lmb_p(self):
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
    def defect(self):
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

    # ----------------------------------------------------
    # ----------------- Unary operators ------------------
    # ----------------------------------------------------
    @property
    def D(self):
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
            >>> m = MNumber('baba')
            >>> m.D.m_word
            'bcbc'
            >>> m = MNumber('ABC')
            >>> m.D.m_word
            'ccbbaa'
            >>> m = MNumber('abcba')
            >>> m.D.m_word
            'cbabc'
        """
        dual_word = ''.join(self.dual_map[ch] for ch in self.m_word)
        return MNumber(dual_word)

    @property
    def E(self):
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
            >>> m = MNumber('baba')
            >>> m.E.m_word
            'abab'
            >>> m = MNumber('ABC')
            >>> m.E.m_word
            'ccbbaa'
            >>> m = MNumber('abcba')
            >>> m.E.m_word
            'abcba'
        """
        return MNumber(self.m_word[::-1])
    
    @property
    def F(self):
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
            >>> m = MNumber('baba')
            >>> m.F.m_word
            'cbcb'
            >>> m = MNumber('ABAB')
            >>> m.F.m_word
            'bbccbbcc'
            >>> m = MNumber('abcba')
            >>> m.F.m_word
            'cbabc'
        """
        return self.D.E
    
    # ----------------------------------------------------
    # --------------- Logical operations -----------------
    # ----------------------------------------------------    
    def __or__(self, m_number: 'MNumber'):
        """
        Parallel connection (OR logical function).

        Formula:
        """
        _prefix = max(self.l, m_number.l) + max(self.l, m_number.l)
        _infix = min(self.r, m_number.l) + max(self.r, m_number.l)
        _sufix = min(self.r, m_number.r) + min(self.r, m_number.r)
        
        return MNumber(_prefix + self.m_word + _infix + m_number.m_word + _sufix)

    def __and__(self, m_number: 'MNumber'):
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
    
    def zip(self, **kwargs):
        """
        Performs the zip operation on the M-number.
        Reduces the m-word based on distance properties.
        
        Returns:
            MNumber: A new MNumber instance with the zipped m-word.
            
        Examples:
            >>> MNumber.set_alphabet('abc')
            >>> m = MNumber('abac')
            >>> m.zip().m_word
            'ac'
            >>> m = MNumber('baba')
            >>> m.zip().m_word
            'ba'
            >>> m = MNumber('aaaababbbb')
            >>> m.zip().m_word
            'aabb'
            >>> m = MNumber('bcbaac')
            >>> m.zip().m_word
            'baac'
            >>> m = MNumber('ABC')
            >>> m.zip().m_word
            'aacc'
        """
        jorb = self.m_word

        def dlt(c1, c2):
            return abs(self.val[c1] - self.val[c2])

        def ext(x):
            res = list(x)
            kol = 0
            char_map = {ch: i for i, ch in enumerate(self.ABC)}
            
            for i in range(len(x) - 1):
                idx1 = char_map[x[i]]
                idx2 = char_map[x[i+1]]
                
                ub = ''
                if idx1 + 1 < idx2: # ascending gap
                    for k in range(idx1 + 1, idx2):
                        ub += self.ABC[k] * 2
                    res.insert(i + 1 + kol, ub)
                    kol += 1
                elif idx1 > idx2 + 1: # descending gap
                    for k in range(idx1 - 1, idx2, -1):
                        ub += self.ABC[k] * 2
                    res.insert(i + 1 + kol, ub)
                    kol += 1
            return "".join(res)

        def zip4(x):
            go1 = 0
            while go1 == 0:
                dulj = len(x)
                if dulj == 2:
                    return x
                i = 0
                while i < dulj - 3:
                    lijevo = dlt(x[i], x[i+1]) - dlt(x[i+1], x[i+2]) + dlt(x[i+2], x[i+3])
                    desno = dlt(x[i], x[i+3])
                    if lijevo == desno:
                        if i == 0:
                            x = x[i] + x[i+3:]
                        else:
                            x = x[:i+1] + x[i+3:]
                        dulj = len(x)
                        i -= 1
                    i += 1
                go1 = 1
            return x

        def zip3(x):
            go2 = 0
            while go2 == 0:
                dulj = len(x)
                if dulj == 2:
                    return x
                i = 0
                while i < dulj - 2:
                    if x[i] == x[i+2]:
                        x = x[:i] + x[i+2:]
                        dulj = len(x)
                    else:
                        i += 1
                go2 = 1
            return x

        def rvs(x):
            rez = []
            for i in range(len(x) - 1):
                for j in range(len(x) - 1, i + 1, -1):
                    if (j - i) % 2 == 1 and (x[i] == x[j]):
                        novi_slc = x[i+1:j]
                        if novi_slc != novi_slc[::-1]:
                            novi = x[:i+1] + novi_slc[::-1] + x[j:]
                            rez.append(novi)
            return rez

        while True:
            temp_j = zip3(zip4(ext(jorb)))
            jorb = temp_j
            temps = rvs(temp_j)
            manji = False
            for j in temps:
                temps_j = zip3(zip4(j))
                if len(temps_j) == len(temp_j):
                    continue
                else:
                    jorb = temps_j
                    manji = True
                    break
            if not manji:
                break
                
        return MNumber(jorb)



# Primjer korištenja (ako se pokrene kao skripta)
if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)

    # ((((AsB)pC)sB)pC)
    
    # print("\n--- Manual Tests ---")
    # MNumber.set_alphabet("abc", m_continuum=True)
    # m1 = MNumber('A')
    # m2 = MNumber('B')
    # m3 = MNumber('C')


    # n = (((m1 | m2) & m3) | m2 ) & m3
    # n = n.zip()

    # print(f"Expression: {n}")
    # print(f"Zipped: {n._lowwer2upper(n.m_word)}")

    # print(f"Alphabet: {MNumber.ABC}")
    # print(f"Values: {MNumber.val}")

    # # Test 1: baba -> ba
    # m1 = MNumber("baba")
    # print(f"\nOriginal: {m1}")
    # print(f"m1.zip(): {m1.zip()}")
    
    # # Test 2: aaaababbbb -> aabb
    # m2 = MNumber("aaaababbbb")
    # print(f"\nOriginal: {m2}")
    # print(f"m2.zip(): {m2.zip()}")

    # # Test 3: bcbaac -> baac
    # m3 = MNumber("bcbaac")
    # print(f"\nOriginal: {m3}")
    # print(f"m3.zip(): {m3.zip()}")

    # # Test 4: ABC -> aacc
    # m4 = MNumber("ABC")
    # print(f"\nOriginal: {m4}")
    # print(f"m4.zip(): {m4.zip()}")
