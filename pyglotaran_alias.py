"""Enables 'import pyglotaran' as well as the default 'import glotaran'."""

import sys

try:
    import glotaran  # noqa:  F401

    modules_to_update = {}
    for fullname, glotaran_module in sys.modules.items():
        if fullname == "glotaran" or fullname.startswith("glotaran."):
            modules_to_update[f"py{fullname}"] = glotaran_module
    sys.modules.update(modules_to_update)
except ImportError:
    raise ImportError(
        """'pyglotaran_alias' only provides an alias to 'import glotaran' with 'import pyglotaran'.
        In order for this to work you need to install pyglotaran in you current environment.
        i.e. 'pip install pyglotaran' or 'conda install pyglotaran'"""
    )
