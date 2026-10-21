# mNumbers

`mNumbers` is a Python library for computing with **m-numbers** (m-words), the objects of the m-system: an algebraic theory developed by Miroslav Šare within the theory of electric circuits.

## About the theory

M-numbers are represented by **m-words**: finite words over an ordered alphabet (a chain of letters). An alphabet with *n* letters generates an *n*-generator m-system.

Every m-system has two dual operations, **s-addition** and **p-addition**. Under each of them the set of m-words forms an infinite commutative generalized group homomorphic to the additive group of integers, and the two operations are linked by a modular distributive law. Three symmetries (isomorphisms) between the two operations form, together with the identity, the Klein four-group. The resulting m-structure is a physically motivated unification and generalization of the algebraic structure of the integers, the constants of logic and graph theory [1].

The theory originates in circuit theory. In the three-generator m-system the letters are interpreted as the three basic elements of linear networks (capacitance, resistance and inductance), and s- and p-addition correspond to the **serial and parallel connection** of two-terminal elements. M-words assigned to electrical networks thus act as new network constants that reflect their physical, algebraic, topological and logical properties [1]. A modern perspective on this connection is given in [3]. In this library, s-addition is written `&` and p-addition `|`.

Different m-words can be equivalent. The algebraic structure behind this, including the equivalence of m-words and their compression to incompressible m-words, is studied in [2]. In this library, compression is available as `zip`.

## What is in the package

The package currently provides one class, `MNumber`, together with the exception `MNumberError`.

| Feature | API |
|---|---|
| Alphabet with numerical values: `1..n`, or centred around 0 (m-continuum) | `MNumber.set_alphabet("abc")`, `MNumber.set_alphabet("abc", m_continuum=True)` |
| m-words in lowercase notation, or in the short uppercase notation where `A` stands for `aa` | `MNumber("aab")`, `MNumber("Ab")`, `x.l2U`, `x.U2l` |
| Ends and shell of an m-word | `x.l`, `x.r`, `x.q` |
| Length λ, its serial and parallel components, defect | `x.lmb`, `x.lmb_s`, `x.lmb_p`, `x.defect` |
| Quadruple (val(l), λs, λp, val(r)) | `x.quadruple` |
| s-addition (serial connection) and p-addition (parallel connection) | `x & y`, `x \| y` |
| Duality, reversal, dual-reversal | `x.D`, `x.E`, `x.F` |
| Invertibility and complement | `x.I`, `x.K` (also `~x`) |
| Compression to an incompressible m-word | `x.zip` |

## Installation

Requires Python 3.12 or higher. The package is not yet on PyPI; install it from GitHub:

```bash
pip install git+https://github.com/JurajBenic/mNumbers.git
```

or, in a uv project:

```bash
uv add git+https://github.com/JurajBenic/mNumbers.git
```

## Quick example

```python
from mnumbers import MNumber

# Three-generator m-system with letters a < b < c
MNumber.set_alphabet("abc")

x = MNumber("ab")
y = MNumber("Bc")        # uppercase notation: "Bc" is the m-word "bbc"

s = x & y                # s-addition (serial connection)
p = x | y                # p-addition (parallel connection)

print(s, s.l2U)          # aaabbbbbccc AaBBbCc
print(p)                 # bbabbbbbcbb
print(s.zip, p.zip)      # abc b

print(x.D, x.E, x.F)     # cb ba bc
print(x.quadruple)       # (1, -1, 0, 2)
```

## Literature

The following literature describes the theory implemented in this library:

1. Šare, M. *Jorbologija* [book]. Available at https://www.nofrx.org/jorbologija/english.html
2. Essert, M., & Žubrinić, D. (2022). Šare's algebraic systems. *Acta Mathematica Spalatensia*, 2, 1–28. https://doi.org/10.32817/ams.2.1
3. Orešković, M., Kuzmanović Ivičić, I., Benić, J., & Essert, M. (2026). A Perspective on the Algebra, Topology, and Logic of Electrical Networks. *International Journal of Circuit Theory and Applications*, 54(9), 4588–4604. https://doi.org/10.1002/cta.70359

## Development and Testing

Contributions are welcome. The project uses [uv](https://docs.astral.sh/uv/) for development and [pytest](https://docs.pytest.org/) for testing.

### Setup

```bash
git clone https://github.com/JurajBenic/mNumbers.git
cd mNumbers
uv sync
```

`uv sync` creates a virtual environment in `.venv` and installs the package in editable mode together with the development tools (`pytest`, `pytest-cov`).

### Running the tests

```bash
uv run pytest
```

This runs both the unit tests in `tests/` and the doctests, i.e. the examples in the docstrings of the `mnumbers` package. When you change the behaviour of a method, update its docstring examples as well, because they are part of the test suite.

To measure test coverage:

```bash
uv run pytest --cov                      # report in the terminal, with missing lines
uv run pytest --cov --cov-report=html    # HTML report in htmlcov/index.html
```

### Contributing

1. Create a new branch for your change.
2. Add tests for new functionality, either in `tests/` or as docstring examples.
3. Make sure `uv run pytest` passes.
4. Open a pull request with a short description of the change.

## Citation

If you use `mNumbers` in your research, please cite it as:

> Benić, J., & Kuzmanović Ivičić, I. (2026). *mNumbers: A Python library for working with m-numbers* (Version 0.1.0) [Computer software]. https://github.com/JurajBenic/mNumbers

BibTeX:

```bibtex
@software{mnumbers,
  author  = {Beni{\'c}, Juraj and Kuzmanovi{\'c} Ivi{\v{c}}i{\'c}, Ivana},
  title   = {{mNumbers}: A Python library for working with m-numbers},
  year    = {2026},
  version = {0.1.0},
  url     = {https://github.com/JurajBenic/mNumbers}
}
```

Citation metadata is also available in [`CITATION.cff`](CITATION.cff); on GitHub, use the *Cite this repository* button.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
