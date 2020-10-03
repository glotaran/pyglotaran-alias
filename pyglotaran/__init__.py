"""Enables 'import pyglotaran' as well as the default 'import glotaran'."""
import sys
from importlib.util import find_spec

if find_spec("glotaran") and "pyglotaran" not in globals().keys():
    __import__("glotaran")

    modules_to_update = {}
    for fullname, glotaran_module in sys.modules.items():
        if fullname == "glotaran" or fullname.startswith("glotaran."):
            modules_to_update[f"py{fullname}"] = glotaran_module
    sys.modules.update(modules_to_update)
    pyglotaran = sys.modules["glotaran"]
    # ensure that variables used here aren't visible in autocomplete
    del locals()["sys"]
    del locals()["find_spec"]
    del locals()["fullname"]
    del locals()["glotaran_module"]
    del locals()["modules_to_update"]
else:
    raise ImportError(
        """'pyglotaran_alias' only provides an alias to 'import glotaran' with 'import pyglotaran'.
        In order for this to work you need to install pyglotaran in you current environment.
        i.e. 'pip install pyglotaran' or 'conda install pyglotaran'"""
    )
