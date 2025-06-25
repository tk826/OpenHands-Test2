import os
import subprocess
import tempfile
import pytest

SCRIPT_PATH = os.path.join(os.path.dirname(__file__), '../modules/box_upload.sh')


def test_script_exists():
    assert os.path.exists(SCRIPT_PATH)
    assert os.path.isfile(SCRIPT_PATH)


def test_usage_message():
    # No arguments should print usage and exit 1
    result = subprocess.run(['bash', SCRIPT_PATH], capture_output=True, text=True)
    assert result.returncode == 1
    assert 'Usage:' in result.stdout or 'Usage:' in result.stderr


def test_missing_file():
    # Should error if file does not exist
    result = subprocess.run(['bash', SCRIPT_PATH, '/no/such/file', '12345'], capture_output=True, text=True)
    assert result.returncode == 3
    assert 'does not exist' in result.stdout or 'does not exist' in result.stderr


def test_missing_box_cli(monkeypatch):
    # Simulate missing box CLI
    with tempfile.NamedTemporaryFile() as tmp:
        monkeypatch.setenv('PATH', '')
        result = subprocess.run(['bash', SCRIPT_PATH, tmp.name, '12345'], capture_output=True, text=True)
        assert result.returncode == 2
        assert 'not installed' in result.stdout or 'not installed' in result.stderr
