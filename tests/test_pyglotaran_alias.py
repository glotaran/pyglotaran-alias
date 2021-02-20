import importlib.util
import re
import subprocess
import sys

import pytest
from _pytest.monkeypatch import MonkeyPatch


def test_exception_if_glotaran_is_missing(monkeypatch: MonkeyPatch):
    """Raise Exception if glotaran isn't installed."""

    def mock_find_spec(*args, **kwargs):
        pass

    monkeypatch.setattr(importlib.util, "find_spec", mock_find_spec)
    with pytest.raises(ImportError, match=r"you need to install pyglotaran"):
        import pyglotaran  # noqa:  F401


def test_glotaran_import_not_leeking_out():
    """Glotaran isn't imported normally and thus not in globals."""
    import pyglotaran  # noqa:  F401

    assert "glotaran" not in globals().keys()


@pytest.mark.parametrize(
    "pyglotaran_alias_local_variable",
    [
        "find_spec",
        "fullname",
        "glotaran_module",
        "modules_to_update",
    ],
)
def test_pyglotaran_alias_local_variables_leeking_out(pyglotaran_alias_local_variable: str):
    """Test that local variables are removed."""
    assert pyglotaran_alias_local_variable not in locals().keys()
    assert pyglotaran_alias_local_variable not in globals().keys()
    with pytest.raises(ImportError):
        exec(f"from pyglotaran import {pyglotaran_alias_local_variable}")


def test_import_works():
    """Check that 'import pyglotaran' works and 'pyglotaran' is an actual alias to 'glotaran'."""
    # pylint: disable=no-member
    import glotaran  # noqa:  F401

    import pyglotaran  # noqa:  F401

    assert hasattr(pyglotaran, "__version__")

    assert glotaran.__version__ == pyglotaran.__version__  # type:ignore

    loaded_module_names = sys.modules.keys()

    glotaran_modules = tuple(
        filter(
            lambda name: name == "glotaran" or name.startswith("glotaran."),
            loaded_module_names,
        )
    )

    pyglotaran_modules = tuple(
        filter(
            lambda name: name == "pyglotaran" or name.startswith("pyglotaran."),
            loaded_module_names,
        )
    )
    assert len(glotaran_modules) == len(pyglotaran_modules)
    for glotaran_module in glotaran_modules:
        assert f"py{glotaran_module}" in pyglotaran_modules

    assert (
        glotaran.read_model_from_yml.__code__
        == pyglotaran.read_model_from_yml.__code__  # type:ignore
    )


def test_from_import_works():
    """Test that from imports work."""
    # pylint: disable=no-name-in-module
    import glotaran  # noqa:  F401

    from pyglotaran import read_model_from_yml  # type:ignore

    assert glotaran.read_model_from_yml.__code__ == read_model_from_yml.__code__


def test_cli_raises_proper_exeption():
    """Test that the cli alias works properly."""
    output = subprocess.run(
        "pyglotaran", shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE
    )
    assert (
        re.search(br"Usage\: pyglotaran \[OPTIONS\] COMMAND \[ARGS\]", output.stdout) is not None
    )
    assert output.stderr == b""
