import pytest
import pandas as pd
import tempfile
import os
from modules import check_process

# --- load_column_types tests ---
@pytest.mark.parametrize(
    "file_content,expected,raises",
    [
        ("a:int\nb:float\nc:datetime\n", {'a': 'int', 'b': 'float', 'c': 'datetime'}, None),
        ("a:int\nb\nc:datetime\n", None, ValueError),
        ("", None, ValueError),
        (None, None, ValueError),
    ]
)
def test_load_column_types(file_content, expected, raises):
    if file_content is None:
        # Simulate None input
        with pytest.raises(ValueError):
            check_process.load_column_types(None)
        return
    with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as f:
        fpath = f.name
        f.write(file_content)
    try:
        if raises:
            with pytest.raises(ValueError):
                check_process.load_column_types(fpath)
        else:
            result = check_process.load_column_types(fpath)
            assert result == expected
    finally:
        os.remove(fpath)

# --- check_values tests (merged No9 & No10) ---
@pytest.mark.parametrize(
    "df_dict,column_types,expected_df,expected_warnings",
    [
        # 1 標準ケース(1件)
        (
            {'a': ['1'], 'b': ['1.1'], 'c': ['2020-01-01 12:00:00'], 'd': ['x']},
            {'a': 'int', 'b': 'float', 'c': 'datetime', 'd': 'str'},
            [{'a': 1, 'b': 1.1, 'c': '2020-01-01 12:00:00', 'd': 'x'}],
            []
        ),
        # 2 標準ケース(複数件)
        (
            {'a': ['1', '2'], 'b': ['1.1', '2.2'], 'c': ['2020-01-01 12:00:00', '2020-01-02 00:00:00'], 'd': ['x', 'y']},
            {'a': 'int', 'b': 'float', 'c': 'datetime', 'd': 'str'},
            [
                {'a': 1, 'b': 1.1, 'c': '2020-01-01 12:00:00', 'd': 'x'},
                {'a': 2, 'b': 2.2, 'c': '2020-01-02 00:00:00', 'd': 'y'}
            ],
            []
        ),
        # 3 余分なカラム
        (
            {'a': ['1', '3'], 'b': ['1.1', '3.3'], 'c': ['2020-01-01 12:00:00', '2020-01-02 00:00:00'], 'd': ['x', 'y'], 'e': [1,2]},
            {'a': 'int', 'b': 'float', 'c': 'datetime', 'd': 'str'},
            [
                {'a': 1, 'b': 1.1, 'c': '2020-01-01 12:00:00', 'd': 'x'},
                {'a': 3, 'b': 3.3, 'c': '2020-01-02 00:00:00', 'd': 'y'}
            ],
            []
        ),
        # 4 型不正値
        (
            {'a': ['1', 'x'], 'b': ['1.1', 'bad'], 'c': ['2020-01-01 12:00:00', '2020-13-01 00:00:00'], 'd': [None, 'abc']},
            {'a': 'int', 'b': 'float', 'c': 'datetime', 'd': 'str'},
            [
                {'a': 1, 'b': 1.1, 'c': '2020-01-01 12:00:00', 'd': ''},
                {'a': '', 'b': '', 'c': '', 'd': 'abc'}
            ],
            [
                {'col': 'a', 'row': 1, 'value': 'x', 'error': 'invalid int'},
                {'col': 'b', 'row': 1, 'value': 'bad', 'error': 'invalid float'},
                {'col': 'c', 'row': 1, 'value': '2020-13-01 00:00:00', 'error': 'invalid datetime'}
            ]
        ),
        # 5 欠損値
        (
            {'a': ['', None], 'b': ['', None], 'c': ['', None], 'd': ['', None]},
            {'a': 'int', 'b': 'float', 'c': 'datetime', 'd': 'str'},
            [
                {'a': '', 'b': '', 'c': '', 'd': ''},
                {'a': '', 'b': '', 'c': '', 'd': ''}
            ],
            []
        ),
        # 6 境界値
        (
            {'a': ['0', '-1'], 'b': ['0.0', '-1.1'], 'c': ['1999-12-31 23:59:59', '2100-01-01 00:00:00'], 'd': ['', '']},
            {'a': 'int', 'b': 'float', 'c': 'datetime', 'd': 'str'},
            [
                {'a': 0, 'b': 0.0, 'c': '1999-12-31 23:59:59', 'd': ''},
                {'a': -1, 'b': -1.1, 'c': '2100-01-01 00:00:00', 'd': ''}
            ],
            []
        ),
        # 7 複数件
        (
            {'a': ['1', '2'], 'b': ['1.1', '2.2'], 'c': ['2020-01-01 12:00:00', '2020-01-02 00:00:00'], 'd': ['x', 'y']},
            {'a': 'int', 'b': 'float', 'c': 'datetime', 'd': 'str'},
            [
                {'a': 1, 'b': 1.1, 'c': '2020-01-01 12:00:00', 'd': 'x'},
                {'a': 2, 'b': 2.2, 'c': '2020-01-02 00:00:00', 'd': 'y'}
            ],
            []
        ),
        # 8 全不正値
        (
            {'a': ['a', 'b'], 'b': ['b', 'c'], 'c': ['c', 'd'], 'd': [None, None]},
            {'a': 'int', 'b': 'float', 'c': 'datetime', 'd': 'str'},
            [
                {'a': '', 'b': '', 'c': '', 'd': ''},
                {'a': '', 'b': '', 'c': '', 'd': ''}
            ],
            [
                {'col': 'a', 'row': 0, 'value': 'a', 'error': 'invalid int'},
                {'col': 'a', 'row': 1, 'value': 'b', 'error': 'invalid int'},
                {'col': 'b', 'row': 0, 'value': 'b', 'error': 'invalid float'},
                {'col': 'b', 'row': 1, 'value': 'c', 'error': 'invalid float'},
                {'col': 'c', 'row': 0, 'value': 'c', 'error': 'invalid datetime'},
                {'col': 'c', 'row': 1, 'value': 'd', 'error': 'invalid datetime'}
            ]
        ),
        # 9 空DataFrame, column_typesあり
        (
            {},
            {'a': 'int'},
            [],
            []
        ),
        # 10 column_types空
        (
            {'a': [1, 2]},
            {},
            [],
            []
        ),
    ]
)
def test_check_values(df_dict, column_types, expected_df, expected_warnings):
    df = pd.DataFrame(df_dict)
    result_df, warnings = check_process.check_values(df, column_types)
    # 型変換
    for col, typ in column_types.items():
        if col in result_df.columns:
            if typ == 'int':
                result_df[col] = result_df[col].apply(lambda x: int(float(x)) if x != '' else x)
            elif typ == 'float':
                result_df[col] = result_df[col].apply(lambda x: float(x) if x != '' else x)
    # DataFrame内容比較
    assert result_df.to_dict(orient='records') == expected_df
    # ワーニング比較
    def parse_warning(w):
        import re
        m = re.match(r"Invalid (\w+) in (\w+) at row (\d+): (.*)", w)
        if not m:
            return w
        typ, col, row, value = m.groups()
        return {'col': col, 'row': int(row), 'value': value, 'error': f'invalid {typ}'}
    parsed = [parse_warning(w) for w in warnings]
    assert parsed == expected_warnings


