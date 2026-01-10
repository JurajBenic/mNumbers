

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
    # -------------------- Properties --------------------
    # ----------------------------------------------------
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
            lam += sign * self._distance(self.m_word[i], self.m_word[i+1])
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
    
    def zip(self, **kwargs) -> 'MNumber':
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

        ABC = self.ABC
        pos = {ch: i for i, ch in enumerate(ABC)}                 # slovo -> pozicija u alfabetu
        val_by_pos = [self.val[ch] for ch in ABC]                 # pozicija -> numerička valuacija (za δ)

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

            return "".join(ABC[p] for p in st)

        def rvs(word: str) -> list[str]:
            # ista semantika kao u tvojoj verziji (parity + “nije palindrom”)
            # :contentReference[oaicite:4]{index=4}
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

        # Glavna petlja kao u Algoritmu 2: ext→zip4→zip3, pa rvs, pa zip4→zip3 :contentReference[oaicite:5]{index=5}
        while True:
            w1 = compress(jorb, do_ext=True)        # zip3(zip4(ext()))
            jorb = w1

            candidates = rvs(w1)
            smaller = False
            for w2 in candidates:
                w3 = compress(w2, do_ext=False)     # zip3(zip4()) (bez ext), kao u pdf-u :contentReference[oaicite:6]{index=6}
                if len(w3) == len(w1):
                    continue
                jorb = w3
                smaller = True
                break

            if not smaller:
                break

        return MNumber(jorb)


    def zip_fast(self) -> "MNumber":
        """
        Performs the zip operation on the M-number.
        Reduces the m-word based on distance properties.
        
        Returns:
            MNumber: A new MNumber instance with the zipped m-word.
            
        Examples:
            >>> MNumber.set_alphabet('abc')
            >>> m = MNumber('abac')
            >>> m.zip_fast().m_word
            'ac'
            >>> m = MNumber('baba')
            >>> m.zip_fast().m_word
            'ba'
            >>> m = MNumber('aaaababbbb')
            >>> m.zip_fast().m_word
            'aabb'
            >>> m = MNumber('bcbaac')
            >>> m.zip_fast().m_word
            'baac'
            >>> m = MNumber('ABC')
            >>> m.zip_fast().m_word
            'aacc'
        """
        # map slovo -> indeks u totalno uređenom alfabetu
        idx = {ch: i for i, ch in enumerate(self.ABC)}
        inv = self.ABC  # indeks -> slovo

        w = self.m_word
        if len(w) <= 2:
            return MNumber(w)

        # radimo na indeksima (brže od dict val lookup + abs svaki put)
        a = [idx[ch] for ch in w]

        stack: list[int] = []

        def reduce_stack():
            # ponavljaj dok god možeš zip3/zip4 na repu
            while True:
                changed = False

                # zip3: a b a -> a  (u tvom kodu točno to radi)
                if len(stack) >= 3 and stack[-3] == stack[-1]:
                    # makni zadnja dva (b,a), ostaje prvi a
                    stack.pop()
                    stack.pop()
                    changed = True

                # zip4: a b c d -> a d ako vrijedi Šare uvjet (Theorem 1)
                if len(stack) >= 4:
                    A, B, C, D = stack[-4], stack[-3], stack[-2], stack[-1]
                    left = abs(A - B) - abs(B - C) + abs(C - D)
                    right = abs(A - D)
                    if left == right:
                        # izbaci B i C
                        del stack[-3:-1]
                        changed = True

                if not changed:
                    break

        # “lazy ext”: dok čitaš prijelaz prev->cur, emitiraš međukorake kao XX (dupliranje)
        prev = a[0]
        stack.append(prev)

        for cur in a[1:]:
            if cur > prev + 1:
                for k in range(prev + 1, cur):
                    stack.append(k); stack.append(k)
                    reduce_stack()
            elif cur < prev - 1:
                for k in range(prev - 1, cur, -1):
                    stack.append(k); stack.append(k)
                    reduce_stack()

            stack.append(cur)
            reduce_stack()
            prev = cur

        out = "".join(inv[i] for i in stack)
        return MNumber(out)



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