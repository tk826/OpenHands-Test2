import os
import tempfile
import shutil
import pytest
from collections import defaultdict

def mock_load_column_types(columns_file):
    return {'col1': str}

def mock_check_values(df, column_types):
    return df, []

def test_grouping_with_prefix_in(monkeypatch):
    # Setup
    import script
    monkeypatch.setattr('script.load_column_types', mock_load_column_types)
    monkeypatch.setattr('script.check_values', mock_check_values)
    prefix_in = 'test_data'
    monkeypatch.setattr('script.zip_csv_files', lambda files, outpath: outpath)
    monkeypatch.setattr('script.upload_csv', lambda bucket, key, file_path: None)
    monkeypatch.setattr('script.list_csv_files', lambda bucket, prefix, date_str: [f'{prefix_in}/test1/2025-06-13_0959.csv'])
    monkeypatch.setattr('script.download_csv', lambda bucket, key, local_s3_dir, prefix_in: file1)
    local_s3_dir = tempfile.mkdtemp()
    try:
        # Create files with prefix_in in their path
        os.makedirs(os.path.join(local_s3_dir, prefix_in, 'test1'), exist_ok=True)
        file1 = os.path.join(local_s3_dir, prefix_in, 'test1', '2025-06-13_0959.csv')
        with open(file1, 'w') as f:
            f.write('col1\nval1')
        # Patch environment variables
        monkeypatch.setenv('S3_PREFIX_IN', prefix_in)
        monkeypatch.setenv('LOCAL_S3_DIR', local_s3_dir)
        monkeypatch.setenv('LOCAL_CHECK_DIR', tempfile.mkdtemp())
        monkeypatch.setenv('COLUMNS_FILE', 'dummy')
        monkeypatch.setenv('TARGET_YMD', '2025-06-13')
        # Patch S3 download/list to return our file
        monkeypatch.setattr('modules.s3_download.list_csv_files', lambda bucket, prefix, date_str: [f'{prefix_in}/test1/2025-06-13_0959.csv'])
        monkeypatch.setattr('modules.s3_download.download_csv', lambda bucket, key, local_s3_dir, prefix_in: file1)
        # Patch bucket to dummy value
        monkeypatch.setenv('S3_BUCKET', 'dummy-bucket')
        # Run main and capture output
        import io, sys
        captured = io.StringIO()
        sys.stdout = captured
        script.main()
        sys.stdout = sys.__stdout__
        output = captured.getvalue()
        # Should not print "ファイル名形式不正"
        assert 'ファイル名形式不正' not in output
    finally:
        shutil.rmtree(local_s3_dir)
