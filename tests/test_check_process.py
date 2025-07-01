import pandas as pd
import pytest
from modules import check_process

@pytest.fixture
def column_types():
    return check_process.load_column_types('columns.txt')

def test_check_values_datetime_valid(column_types):
    df = pd.DataFrame({'datetime': ['2025-07-01 12:00:00', '2025-07-01 13:00:00']})
    cleaned, warnings = check_process.check_values(df.copy(), column_types)
    assert warnings == []
    assert cleaned['datetime'][0] == '2025-07-01 12:00:00'

def test_check_values_datetime_invalid(column_types):
    df = pd.DataFrame({'datetime': ['2025-07-01', 'not-a-date']})
    cleaned, warnings = check_process.check_values(df.copy(), column_types)
    assert len(warnings) == 2
    assert cleaned['datetime'][0] == ''
    assert cleaned['datetime'][1] == ''

def test_check_values_float_valid(column_types):
    df = pd.DataFrame({'value11': [1.23, '4.56']})
    cleaned, warnings = check_process.check_values(df.copy(), column_types)
    assert warnings == []
    assert cleaned['value11'][0] == 1.23 or cleaned['value11'][0] == '1.23'

def test_check_values_float_invalid(column_types):
    df = pd.DataFrame({'value11': ['abc', '']})
    cleaned, warnings = check_process.check_values(df.copy(), column_types)
    assert len(warnings) == 1
    assert cleaned['value11'][0] == ''

def test_check_values_int_valid(column_types):
    df = pd.DataFrame({'value1': [1, '2', 3.0]})
    cleaned, warnings = check_process.check_values(df.copy(), column_types)
    assert warnings == []
    assert cleaned['value1'][0] == 1 or cleaned['value1'][0] == '1'

def test_check_values_int_invalid(column_types):
    df = pd.DataFrame({'value1': ['abc', '1.5', '']})
    cleaned, warnings = check_process.check_values(df.copy(), column_types)
    assert len(warnings) == 1
    assert cleaned['value1'][0] == ''
    assert cleaned['value1'][1] == '1.5'

def test_check_values_str_and_missing(column_types):
    df = pd.DataFrame({'name': [None, 'abc', 123]})
    cleaned, warnings = check_process.check_values(df.copy(), column_types)
    assert warnings == []
    assert cleaned['name'][0] == ''
    assert cleaned['name'][1] == 'abc'
    assert cleaned['name'][2] == '123'

def test_check_values_extra_and_missing_columns(column_types):
    df = pd.DataFrame({'name': ['abc'], 'extra': [123]})
    cleaned, warnings = check_process.check_values(df.copy(), column_types)
    assert 'extra' not in cleaned.columns
    assert 'name' in cleaned.columns
    # missing columns should be filled with ''
    for col in column_types:
        if col not in cleaned.columns:
            continue
        assert cleaned[col].isnull().sum() == 0
