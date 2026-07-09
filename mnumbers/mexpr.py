"""
Structural m-expressions, ideal atoms and boundary reductions
(Morelli-type classification computed purely from m-numbers).

This module builds ON TOP of the MNumber class and delegates all
m-word mechanics to it: atoms of an expression ARE MNumber objects,
boundary letters come from MNumber.l / MNumber.r, valuations from
MNumber.val, letter inversion from MNumber.D, raw jorbs from the
serial/parallel operators & and |, and the reactive-pair theta from
MNumber.zip. MExpr itself adds only what MNumber does not have: the
series/parallel TREE, the ideal atoms K and P with their absorption
rules, the boundary reductions delta0 / deltainf and the comparison
of the reductions as functions of the surviving element values.
"""

import random as _random
from .mnumber import MNumber, MNumberError


class MExprError(Exception):
    """Exception class for MExpr errors."""
    pass


class MExpr:
    """
    A structural m-expression: a series/parallel formula over m-atoms,
    e.g. 'B s (C p (B s A))'. Atoms are anything MNumber accepts
    ('A', 'B', 'CA', 'ba', ...); operators are the reserved lowercase
    tokens 's' (serial) and 'p' (parallel).

    Ideal atoms (units of the m-structure, cf. D47):
        K ... short circuit (s-unit, Z = 0):   x s K = x,  x p K = K
        P ... open  circuit (p-unit, Z = inf): x p P = x,  x s P = P

    Boundary reductions (behaviour of the network at s=0 and s=inf):
        delta0  : every atom is replaced by K/P/itself according to
                  the centered valuation of its FIRST letter (MNumber.l):
                  nu < 0 -> P, nu > 0 -> K, nu = 0 -> atom survives
        deltainf: the same with the LAST letter (MNumber.r) and
                  K/P exchanged.

    Surviving atoms keep an instance label (B1, B2, ...) because the
    classification must remember WHICH resistor survives.

    Examples:
        >>> MNumber.set_alphabet('abc', m_continuum=True)
        >>> e63 = MExpr.parse('B s (C p (B s A))')     # network #63
        >>> str(e63.delta0()), str(e63.deltainf())
        ('B1', 'B1 s B2')
        >>> e71 = MExpr.parse('B s (B p (C s A))')     # network #71
        >>> str(e71.delta0()), str(e71.deltainf())
        ('B1 s B2', 'B1 s B2')
        >>> e63.morelli()['relation']
        '<'
        >>> e71.morelli()['group']
        'IV_D1 (notch)'
    """

    _OPS = ('s', 'p')

    def __init__(self, kind, op=None, children=None, atom=None,
                 label=None):
        self.kind = kind              # 'op' | 'atom' | 'ideal'
        self.op = op                  # 's' | 'p'            (kind == 'op')
        self.children = children or []
        self.atom = atom              # MNumber              (kind == 'atom')
        self.label = label            # 'B1', 'ba1' | 'K', 'P'

    # ------------------------- construction -------------------------
    @classmethod
    def _make_atom(cls, token, counters):
        m = MNumber(token)                       # MNumber validira abecedu
        key = m.l2U
        counters[key] = counters.get(key, 0) + 1
        return cls('atom', atom=m, label=f"{key}{counters[key]}")

    @classmethod
    def _ideal(cls, which):
        return cls('ideal', label=which)          # 'K' ili 'P'

    @classmethod
    def parse(cls, text: str) -> 'MExpr':
        """
        Parse a series/parallel formula over m-atoms.

        Examples:
            >>> MNumber.set_alphabet('abc', m_continuum=True)
            >>> MExpr.parse('B p (B s C s A)').source()
            'B p (B s C s A)'
            >>> str(MExpr.parse('B p (B s C s A)'))
            'B1 p (B2 s C1 s A1)'
            >>> MExpr.parse('ba s ((CA s B) p (cb s B))').kind
            'op'
        """
        toks = text.replace('(', ' ( ').replace(')', ' ) ').split()
        pos = [0]
        counters = {}

        def atom():
            t = toks[pos[0]]; pos[0] += 1
            if t == '(':
                e = chain()
                if pos[0] >= len(toks) or toks[pos[0]] != ')':
                    raise MExprError("Missing ')'.")
                pos[0] += 1
                return e
            if t in cls._OPS or t == ')':
                raise MExprError(f"Unexpected token '{t}'.")
            return cls._make_atom(t, counters)

        def chain():
            e = atom()
            while pos[0] < len(toks) and toks[pos[0]] in cls._OPS:
                o = toks[pos[0]]; pos[0] += 1
                f = atom()
                if e.kind == 'op' and e.op == o:
                    e.children.append(f)          # izravnavanje asocijativnosti
                else:
                    e = cls('op', op=o, children=[e, f])
            return e

        e = chain()
        if pos[0] != len(toks):
            raise MExprError("Trailing tokens in expression.")
        return e

    # --------------------------- display ----------------------------
    def __str__(self):
        if self.kind != 'op':
            return self.label
        parts = [f"({ch})" if ch.kind == 'op' else str(ch)
                 for ch in self.children]
        return f" {self.op} ".join(parts)

    def source(self) -> str:
        """The expression with original tokens (MNumber.l2U, no labels).

        Examples:
            >>> MNumber.set_alphabet('abc', m_continuum=True)
            >>> MExpr.parse('ba s (CA p B)').source()
            'ba s (CA p B)'
        """
        if self.kind == 'ideal':
            return self.label
        if self.kind == 'atom':
            return self.atom.l2U
        parts = [f"({ch.source()})" if ch.kind == 'op' else ch.source()
                 for ch in self.children]
        return f" {self.op} ".join(parts)

    # -------------------- valuation of a letter ---------------------
    @staticmethod
    def _nu(ch: str) -> int:
        """Centered valuation: MNumber.val, centriran oko srednjeg
        slova ako abeceda nije m_continuum."""
        if min(MNumber.val.values()) < 0:
            return MNumber.val[ch]
        mid = MNumber.ABC[(len(MNumber.ABC) - 1) // 2]
        return MNumber.val[ch] - MNumber.val[mid]

    def _is_resistive(self) -> bool:
        return self.kind == 'atom' and all(self._nu(c) == 0
                                           for c in self.atom.m_word)

    # --------------------- boundary reductions ----------------------
    def _delta(self, side: str) -> 'MExpr':
        if self.kind == 'ideal':
            return self
        if self.kind == 'atom':
            nu = self._nu(self.atom.l if side == '0' else self.atom.r)
            if nu == 0:
                a = MExpr('atom', atom=self.atom, label=self.label)
                a._side = None if self._is_resistive() else side
                return a
            if side == '0':
                return self._ideal('P' if nu < 0 else 'K')
            return self._ideal('K' if nu < 0 else 'P')

        kids = [c._delta(side) for c in self.children]
        killer, unit = ('P', 'K') if self.op == 's' else ('K', 'P')
        if any(k.kind == 'ideal' and k.label == killer for k in kids):
            return self._ideal(killer)
        kids = [k for k in kids if not (k.kind == 'ideal'
                                        and k.label == unit)]
        if not kids:
            return self._ideal(unit)
        if len(kids) == 1:
            return kids[0]
        flat = []
        for k in kids:                             # zadrzi ravni n-arni oblik
            if k.kind == 'op' and k.op == self.op:
                flat.extend(k.children)
            else:
                flat.append(k)
        return MExpr('op', op=self.op, children=flat)

    def delta0(self) -> 'MExpr':
        """Boundary reduction at s = 0 (DC behaviour)."""
        return self._delta('0')

    def deltainf(self) -> 'MExpr':
        """Boundary reduction at s = infinity."""
        return self._delta('inf')

    # ------------------ comparison of the reductions ----------------
    @staticmethod
    def _eval(e: 'MExpr', values: dict) -> float:
        if e.kind == 'ideal':
            return 0.0 if e.label == 'K' else float('inf')
        if e.kind == 'atom':
            return values[(e.label, getattr(e, '_side', None))]
        vals = [MExpr._eval(c, values) for c in e.children]
        if e.op == 's':
            return float('inf') if any(v == float('inf') for v in vals) \
                else sum(vals)
        r = None                                   # paralela
        for v in vals:
            if v == 0.0:
                return 0.0
            if r is None:
                r = v
            elif v != float('inf'):
                r = v if r == float('inf') else r * v / (r + v)
        return r

    @staticmethod
    def _collect_keys(e: 'MExpr', keys: set):
        if e.kind == 'atom':
            keys.add((e.label, getattr(e, '_side', None)))
        for c in e.children:
            MExpr._collect_keys(c, keys)

    @staticmethod
    def compare(d0: 'MExpr', dinf: 'MExpr', trials: int = 96,
                seed: int = 0) -> str:
        """
        Compare two boundary reductions AS FUNCTIONS of the surviving
        element values. Returns '=', '<', '>' or '||' (incomparable).

        Examples:
            >>> MNumber.set_alphabet('abc', m_continuum=True)
            >>> e = MExpr.parse('B p (C s (B p A))')       # network #62
            >>> MExpr.compare(e.delta0(), e.deltainf())
            '<'
            >>> e = MExpr.parse('(B p A) s (B p C)')       # network #96
            >>> MExpr.compare(e.delta0(), e.deltainf())
            '||'
        """
        keys = set()
        MExpr._collect_keys(d0, keys)
        MExpr._collect_keys(dinf, keys)
        rng = _random.Random(seed)
        lo = hi = False
        for _ in range(trials):
            values = {k: rng.lognormvariate(0.0, 1.0) for k in keys}
            v0, vi = MExpr._eval(d0, values), MExpr._eval(dinf, values)
            if v0 == vi:
                continue
            if v0 == float('inf') or (vi != float('inf') and v0 > vi):
                hi = True
            else:
                lo = True
        if lo and hi:
            return '||'
        if lo:
            return '<'
        if hi:
            return '>'
        return '='

    # -------------------- reactive pair and theta -------------------
    def _reactive_leaves(self, out):
        if self.kind == 'atom':
            if any(self._nu(c) != 0 for c in self.atom.m_word):
                out.append(self)
        for c in self.children:
            c._reactive_leaves(out)

    def reactive_theta(self) -> str | None:
        """
        If the expression contains exactly two reactive atoms and they
        are siblings (direct children of the same flattened node), the
        theta of their pair is returned, computed with MNumber's own
        machinery: (x & y).zip resp. (x | y).zip; otherwise None.

        Examples:
            >>> MNumber.set_alphabet('abc', m_continuum=True)
            >>> MExpr.parse('B p (B s C s A)').reactive_theta()
            'AC'
            >>> MExpr.parse('B s (B p C p A)').reactive_theta()
            'CA'
            >>> print(MExpr.parse('B s (C p (B s A))').reactive_theta())
            None
        """
        leaves = []
        self._reactive_leaves(leaves)
        if len(leaves) != 2:
            return None

        def parent_of(node):
            if node.kind == 'op':
                if sum(1 for c in node.children if c in leaves) == 2:
                    return node
                for c in node.children:
                    r = parent_of(c)
                    if r is not None:
                        return r
            return None

        par = parent_of(self)
        if par is None:
            return None
        x, y = leaves[0].atom, leaves[1].atom
        pair = (x & y) if par.op == 's' else (x | y)
        return pair.zip.l2U

    # ---------------------- group transformations -------------------
    def _map(self, f_atom, f_op):
        if self.kind == 'ideal':
            return MExpr('ideal', label=self.label)
        if self.kind == 'atom':
            return MExpr('atom', atom=f_atom(self.atom))
        return MExpr('op', op=f_op(self.op),
                     children=[c._map(f_atom, f_op)
                               for c in self.children])

    def letters_inverted(self) -> 'MExpr':
        """Morelli s-transformation: invert letters via MNumber.D.

        Examples:
            >>> MNumber.set_alphabet('abc', m_continuum=True)
            >>> MExpr.parse('B s (C p (B s A))').letters_inverted().source()
            'B s (A p (B s C))'
        """
        return self._map(lambda a: a.D, lambda o: o)

    def ops_swapped(self) -> 'MExpr':
        """Morelli p-transformation: swap series <-> parallel.

        Examples:
            >>> MNumber.set_alphabet('abc', m_continuum=True)
            >>> MExpr.parse('B s (C p (B s A))').ops_swapped().source()
            'B p (C s (B p A))'
        """
        return self._map(lambda a: a, lambda o: 'p' if o == 's' else 's')

    def dualled(self) -> 'MExpr':
        """Morelli d-transformation: both inversions."""
        return self.letters_inverted().ops_swapped()

    # ----------------------- raw jorb of the network ----------------
    def to_mnumber(self) -> 'MNumber':
        """
        Evaluate the expression with MNumber's & and | operators,
        producing the raw (uncompressed) jorb of the network.

        Examples:
            >>> MNumber.set_alphabet('abc', m_continuum=True)
            >>> MExpr.parse('B s (B p (C s A))').to_mnumber().l2U
            'BBBBBabACcAaCBB'
        """
        if self.kind == 'ideal':
            raise MExprError("Ideal atoms have no m-number.")
        if self.kind == 'atom':
            return self.atom
        acc = self.children[0].to_mnumber()
        for c in self.children[1:]:
            acc = (acc & c.to_mnumber()) if self.op == 's' \
                else (acc | c.to_mnumber())
        return acc

    # ------------------------ Morelli classifier --------------------
    def morelli(self) -> dict:
        """
        The full boundary-reduction classifier. Returns a dict with the
        reductions, their relation, the reactive-pair theta and, when
        the signature is recognised (biquadratic 2R+1L+1C family), the
        Morelli subgroup label.

        Examples:
            >>> MNumber.set_alphabet('abc', m_continuum=True)
            >>> MExpr.parse('B p (B s C s A)').morelli()['group']
            'IV_D1 (notch)'
            >>> MExpr.parse('B s (A p (B s C))').morelli()['group']
            'IV_E3 (#87-tip)'
        """
        d0, di = self.delta0(), self.deltainf()
        rel = self.compare(d0, di)
        theta = self.reactive_theta()

        def top(e):
            return e.op if e.kind == 'op' else \
                ('ideal' if e.kind == 'ideal' else 'atom')

        group = None
        if rel == '=':
            if theta == 'AC':
                group = 'IV_D1 (notch)'
            elif theta == 'CA':
                group = 'IV_D2 (peak)'
        elif rel == '<':
            if top(di) == 's':
                group = 'IV_E1 (#63-tip)'
            elif top(d0) == 'p':
                group = 'IV_E2 (#62-tip)'
        elif rel == '>':
            if top(d0) == 's':
                group = 'IV_E3 (#87-tip)'
            elif top(di) == 'p':
                group = 'IV_E4 (#88-tip)'
        elif rel == '||' and self.kind == 'op':
            group = 'IV_X1 (#96-tip)' if self.op == 's' \
                else 'IV_X2 (#97-tip)'

        sig = (rel, top(d0), top(di), theta)
        return {'delta0': str(d0), 'deltainf': str(di),
                'relation': rel, 'reactive_theta': theta,
                'signature': sig,
                'group': group if group else f"signatura {sig}"}


# --------------------------------------------------------------------
#  Self-test on all examples (18 rows of the (0,2,2,0) table and, if
#  available, the whole catalogue CSV).
# --------------------------------------------------------------------
def _run_examples(verbose: bool = True) -> bool:
    MNumber.set_alphabet('abc', m_continuum=True)

    TABLE = {
        24: ('A s (B p (B s C))',  'AAbaBBBBBcbCCBB'),
        25: ('B s A s (B p C)',    'AABbAaBcbCBbCcBB'),
        32: ('B s C s (B p A)',    'BBBcbCCcBBbabAAC'),
        33: ('C s (B p (B s A))',  'BCcBBbabABbAaBBC'),
        39: ('B p (B s A) p C',    'CBBabABbAaBBbCcB'),
        40: ('C p (B s (B p A))',  'CCbcBBBBBabAABB'),
        47: ('B p (B s C) p A',    'BBBBBBcbCCBabAA'),
        48: ('A p (B s (B p C))',  'BAaBBbcbCBbCcBBA'),
        62: ('B p (C s (B p A))',  'BBBBCcBBbabAACB'),
        63: ('B s (C p (B s A))',  'BBcbCCacABbAaBBB'),
        71: ('B s (B p (C s A))',  'BBBBBabACcAaCBB'),
        72: ('B p (B s C s A)',    'BBabABBcbCCcAaCB'),
        73: ('B s (B p C p A)',    'BBcbCCBbCcBabAAB'),
        74: ('B p (B s (C p A))',  'BBBBBcbCCacAABB'),
        87: ('B s (A p (B s C))',  'BBBBAaBBbcbCCAB'),
        88: ('B p (A s (B p C))',  'BBabAAcaCBbCcBBB'),
        96: ('(B p A) s (B p C)',  'BBBabAAcaCBbCcBB'),
        97: ('(B s A) p (B s C)',  'BABbAaBBBBcbCCB'),
    }
    EXPECTED_GROUP = {
        71: 'IV_D1 (notch)', 72: 'IV_D1 (notch)',
        73: 'IV_D2 (peak)',  74: 'IV_D2 (peak)',
        63: 'IV_E1 (#63-tip)', 62: 'IV_E2 (#62-tip)',
        87: 'IV_E3 (#87-tip)', 88: 'IV_E4 (#88-tip)',
        96: 'IV_X1 (#96-tip)', 97: 'IV_X2 (#97-tip)',
    }

    ok = True
    for n, (src, jorb) in sorted(TABLE.items()):
        raw = MExpr.parse(src).to_mnumber().m_word
        if raw != MNumber(jorb).m_word:
            ok = False
            print(f"  GRESKA #{n}: to_mnumber {MNumber(raw).l2U} != {jorb}")
    if verbose:
        print(f"to_mnumber == katalozni jorb: "
              f"{'OK' if ok else 'GRESKA'} ({len(TABLE)} redaka)")

    if verbose:
        print(f"\n{'mreza':>5}  {'delta0':<14}{'deltainf':<14}"
              f"{'odnos':<7}{'theta':<7}grupa")
    for n in (71, 72, 73, 74, 63, 62, 87, 88, 96, 97):
        m = MExpr.parse(TABLE[n][0]).morelli()
        good = (m['group'] == EXPECTED_GROUP[n])
        ok = ok and good
        if verbose:
            print(f"{n:>5}  {m['delta0']:<14}{m['deltainf']:<14}"
                  f"{m['relation']:<7}{str(m['reactive_theta']):<7}"
                  f"{m['group']}{'' if good else '   <-- GRESKA'}")

    # mosna #95 s idealnim m-atomima mora se barem cisto reducirati
    m95 = MExpr.parse('ba s ((CA s B) p (cb s B))').morelli()
    if verbose:
        print(f"\n#95 (mosna, idealni atomi): delta0 = {m95['delta0']}, "
              f"deltainf = {m95['deltainf']}, odnos = {m95['relation']}")

    # Morellijeva grupa reproducira IV_E kvadrat
    e63 = MExpr.parse(TABLE[63][0])
    acts = (e63.letters_inverted().source() == TABLE[87][0]
            and e63.ops_swapped().source() == TABLE[62][0]
            and e63.dualled().source() == TABLE[88][0])
    ok = ok and acts
    if verbose:
        print(f"grupa na m-brojevima (63 -> 87/62/88): "
              f"{'OK' if acts else 'GRESKA'}")

    # cijeli katalog, ako je CSV pri ruci
    import os, csv as _csv
    print("tu sam")
    for path in ('Katalog_jorb_2.csv',
                 '/home/juraj/MATHOS/mNumbers/Katalog_jorb_2.csv'):
        if os.path.exists(path):
            good = total = 0
            with open(path, encoding='utf-8-sig') as f:
                for row in _csv.DictReader(f):
                    src = row.get('mNumber_realistaion', '').strip()
                    if not src or 'ba' in src or 'cb' in src:
                        continue      # idealne atome jorb ne provjeravamo
                    total += 1
                    if MExpr.parse(src).to_mnumber().m_word \
                            == MNumber(row['jorb']).m_word:
                        good += 1
                    elif verbose:
                        print(f"  KATALOG GRESKA #{row['network']}")
            ok = ok and (good == total)
            if verbose:
                print(f"cijeli katalog, to_mnumber == jorb: {good}/{total}")
            break

    return ok


if __name__ == "__main__":
    import doctest
    rezultat = doctest.testmod(verbose=False)
    print(f"doctest: {rezultat.attempted} testova, "
          f"{rezultat.failed} gresaka")
    print("=" * 64)
    sve = _run_examples() and rezultat.failed == 0
    print("SVE PROSLO" if sve else "IMA GRESAKA")
