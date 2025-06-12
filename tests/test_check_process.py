import pandas as pd
import tempfile
from modules.check_process import load_column_types, check_values

def test_load_column_types():
    with tempfile.NamedTemporaryFile('w+', delete=False) as f:
        f.write('a:int\nb:float\nc:datetime\n')
        f.flush()
        types = load_column_types(f.name)
        assert types == {'a': 'int', 'b': 'float', 'c': 'datetime'}

def test_check_values():
    column_types = {'a': 'int', 'b': 'float', 'c': 'datetime', 'd': 'str'}
    df = pd.DataFrame({
        'a': ['1', 'x', '3'],
        'b': ['1.1', 'bad', '3.3'],
        'c': ['2020-01-01', '2020-13-01', ''],
        'd': [None, 'abc', 'def'],
        'e': [1, 2, 3]  # 余分なカラム

    })
    df2, warnings = check_values(df, column_types)
    assert 'Invalid int in a at row 1: x' in warnings
    assert 'Invalid float in b at row 1: bad' in warnings
    assert 'Invalid datetime in c at row 1: 2020-13-01' in warnings
    assert 'e' not in df2.columns
    assert df2['a'][1] == ''
    assert df2['b'][1] == ''
    assert df2['c'][1] == ''
    assert df2['d'][0] == ''
