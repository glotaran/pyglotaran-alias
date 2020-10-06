import re
import subprocess


def test_cli_raises_proper_exeption():
    """Test that cli Raises proper exception when pyglotaran isn't installed."""
    output = subprocess.run(
        "pyglotaran", shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE
    )
    assert re.search(b"'pip install pyglotaran'", output.stderr) is not None
