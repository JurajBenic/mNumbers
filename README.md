# mNumbers

## Project Description

`mNumbers` is a Python library for working with m-numbers (MNumber). It supports representation and operations with m-numbers, including:
- Serial operations (s)
- Parallel operations (p)
- Configurable alphabets and continuums

## Requirements

- Python 3.12 or higher

## Literature

The theory of m-numbers (jorbs) was developed by Miroslav Šare within the theory of electric circuits. The following literature describes the theory implemented in this library:

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
