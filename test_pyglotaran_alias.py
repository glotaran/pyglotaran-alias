import importlib.util
import sys

import pytest


def test_no_initial_pyglotaran():
    """Without 'import pyglotaran_alias' pyglotaran can't be imported."""
    with pytest.raises(ImportError):
        import pyglotaran  # noqa:  F401


def test_exception_if_glotaran_is_missing(monkeypatch):
    """Raise Exception if glotaran isn't installed."""

    def mock_find_spec(*args, **kwargs):
        pass

    monkeypatch.setattr(importlib.util, "find_spec", mock_find_spec)
    with pytest.raises(ImportError, match=r"you need to install pyglotaran"):
        import pyglotaran_alias  # noqa:  F401


def test_glotaran_import_not_leeking_out():
    """Glotaran isn't imported normally and thus not in globals."""
    import pyglotaran_alias  # noqa:  F401

    assert "glotaran" not in globals().keys()


def test_import_works():
    """Check that 'import pyglotaran' works and 'pyglotaran' is an actual alias to 'glotaran'."""
    import pyglotaran_alias  # noqa: F401 isort:skip
    import glotaran  # noqa:  F401
    import pyglotaran  # noqa:  F401

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
