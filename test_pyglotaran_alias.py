import sys

import pytest


def test_no_initial_pyglotaran():
    with pytest.raises(ImportError):
        import pyglotaran  # noqa:  F401


def test_import_works():
    import pyglotaran_alias  # noqa:  F401 isort:skip
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
