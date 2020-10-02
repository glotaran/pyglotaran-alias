import importlib.util
import sys

import pytest


def test_exception_if_glotaran_is_missing(monkeypatch):
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
def test_pyglotaran_alias_local_variables_leeking_out(pyglotaran_alias_local_variable):
    assert pyglotaran_alias_local_variable not in locals().keys()
    assert pyglotaran_alias_local_variable not in globals().keys()
    with pytest.raises(ImportError):
        exec(f"from pyglotaran import {pyglotaran_alias_local_variable}")


def test_import_works():
    """Check that 'import pyglotaran' works and 'pyglotaran' is an actual alias to 'glotaran'."""
    import glotaran  # noqa:  F401

    import pyglotaran  # noqa:  F401

    assert hasattr(pyglotaran, "__version__")

    assert glotaran.__version__ == pyglotaran.__version__

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

    assert glotaran.read_model_from_yml.__code__ == pyglotaran.read_model_from_yml.__code__


def test_from_import_works():
    import glotaran  # noqa:  F401

    from pyglotaran import read_model_from_yml

    assert glotaran.read_model_from_yml.__code__ == read_model_from_yml.__code__
