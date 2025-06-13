import pandas as pd
import tempfile
from modules.check_process import load_column_types, check_values

def test_load_column_types():
    with tempfile.NamedTemporaryFile('w+', delete=False) as f:
        f.write('datetime:datetime\nname:str\nvalue1:int\nvalue2:int\nvalue3:int\nvalue4:int\nvalue5:int\nvalue6:int\nvalue7:int\nvalue8:int\nvalue9:int\nvalue10:float\nvalue11:float\nvalue12:float\n')
        f.flush()
        types = load_column_types(f.name)
        assert types == {
            'datetime': 'datetime',
            'name': 'str',
            'value1': 'int',
            'value2': 'int',
            'value3': 'int',
            'value4': 'int',
            'value5': 'int',
            'value6': 'int',
            'value7': 'int',
            'value8': 'int',
            'value9': 'int',
            'value10': 'float',
            'value11': 'float',
            'value12': 'float',
        }

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
