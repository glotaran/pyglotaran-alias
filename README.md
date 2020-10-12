# pyglotaran-alias

[![PyPi Version](https://img.shields.io/pypi/v/pyglotaran_alias.svg)](https://pypi.org/project/pyglotaran-alias/)
[![Conda Version](https://img.shields.io/conda/vn/conda-forge/pyglotaran-alias.svg)](https://anaconda.org/conda-forge/pyglotaran-alias)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/pyglotaran_alias.svg)](https://pypi.org/project/pyglotaran-alias/)

Convenience module which allows to use `pyglotaran` as an alias in the CLI and imports, when working with [pyglotaran](https://github.com/glotaran/pyglotaran).

Since the python implementation of glotaran was renamed to pyglotaran to prevent ambiguity, about which glotaran was used,
at times one might be tempted to use `import pyglotaran` instead of `import glotaran`.

## Usage

```python
import pyglotaran
```

Or

```python
from pyglotaran import ParameterGroup
```

For autocompletion to work in an interactive session (i.e. `python repl`, `jupyter-console` or `jupyter-notebooks`) you need to first import the `pyglotaran-alias` i.e. with `import pyglotaran`.
After this is done `glotaran` is registered under the alias `pyglotaran`, and autocomplete should work.

## How does it work?

When you use `import pyglotaran` the following happens:

- `pyglotaran-alias`'s [`__init__.py`](https://github.com/glotaran/pyglotaran-alias/blob/main/pyglotaran/__init__.py) is called.
- The module cache (`sys.modules`) is populated with all `glotaran` modules.
- For each `glotaran` module an additional corresponding entry with `pyglotaran` is added to the module cache.
- The local variables used to modify the module cache are deleted, so they won't pollute your globals.
- The `pyglotaran` global variable replaces [itself](https://github.com/glotaran/pyglotaran-alias/blob/main/pyglotaran/__init__.py) with the `glotaran` package.

## Known problems

### Linter shows error "No name '`<module or attribute name>`' in module '`pyglotaran`'", when using a text editor

Since most linters use a static file analysis, they won't understand the live swapping of modules at runtime and think that `pyglotaran` is defined in[`pyglotaran-alias`](https://github.com/glotaran/pyglotaran-alias/blob/main/pyglotaran/__init__.py), where `<module or attribute name>` most likely doesn't exist.
Thus you have a `Schrödinger-Linter`, which is right and wrong at the same time.

### Autocomplete doesn't work, when using a text editor

This is due to the fact that autocomplete engines (similar to linters) use a static file analysis and thus think that `pyglotaran` is defined in [`pyglotaran-alias`](https://github.com/glotaran/pyglotaran-alias/blob/main/pyglotaran/__init__.py). Sadly I didn't find a way to fix this issue yet, since it also strongly depends on the used autocomplete engine.

### Autocomplete in interactive session shows attributes on `pyglotaran` which aren't part of `glotaran`

When using an interactive session (i.e. `python repl`, `jupyter-console` or `jupyter-notebooks`), the autocomplete will pick up the replaced module and allow you to get autocompletion for modules and attributes defined in `glotaran`.
But due to static file analysis it will also pick up modules and attributes defined in [`pyglotaran-alias`](https://github.com/glotaran/pyglotaran-alias/blob/main/pyglotaran/__init__.py)
