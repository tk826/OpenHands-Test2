import os
import subprocess

def test_box_folders_upload_mock(monkeypatch, tmp_path):
    # Set the mock result
    mock_result = 'MOCKED_RESULT'
    monkeypatch.setenv('MOCK_BOX_RTESULT', mock_result)

    # Call the box mock script
    result = subprocess.run([
        '/workspace/bin/box', 'folders:upload', 'folder_id', 'file.txt'
    ], capture_output=True, text=True)

    # Should output the mock echo and the mock result
    assert '[MOCK] box folders:upload folder_id file.txt' in result.stdout
    assert mock_result in result.stdout
    assert result.returncode == 0

def test_box_passthrough_error():
    # This should fail with passthrough error since no real box CLI exists
    result = subprocess.run([
        '/workspace/bin/box', 'folders:list', 'folder_id'
    ], capture_output=True, text=True)
    assert 'box CLI not found for passthrough' in result.stderr
    assert result.returncode == 127
