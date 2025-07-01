import pytest
import pandas as pd
from modules import check_process

@pytest.mark.parametrize(
    "df_input, column_types, expected_df, expected_warnings",
    [
        # 1. 正常系: 全て正しい型
        (
            pd.DataFrame({
                'datetime': ['2025-07-01 12:00:00'],
                'name': ['Alice'],
                'value1': [1],
                'value11': [1.23],
            }),
            {'datetime': 'datetime', 'name': 'str', 'value1': 'int', 'value11': 'float'},
            pd.DataFrame({
                'datetime': ['2025-07-01 12:00:00'],
                'name': ['Alice'],
                'value1': [1],
                'value11': [1.23],
            }),
            [],
        ),
        # 2. 異常系: 日付不正
        (
            pd.DataFrame({
                'datetime': ['not-a-date'],
                'name': ['Bob'],
                'value1': [2],
                'value11': [2.34],
            }),
            {'datetime': 'datetime', 'name': 'str', 'value1': 'int', 'value11': 'float'},
            pd.DataFrame({
                'datetime': [''],
                'name': ['Bob'],
                'value1': [2],
                'value11': [2.34],
            }),
            ["Invalid datetime in datetime at row 0: not-a-date"],
        ),
        # 3. 異常系: float不正
        (
            pd.DataFrame({
                'datetime': ['2025-07-01 12:00:00'],
                'name': ['Carol'],
                'value1': [3],
                'value11': ['not-a-float'],
            }),
            {'datetime': 'datetime', 'name': 'str', 'value1': 'int', 'value11': 'float'},
            pd.DataFrame({
                'datetime': ['2025-07-01 12:00:00'],
                'name': ['Carol'],
                'value1': [3],
                'value11': [''],
            }),
            ["Invalid float in value11 at row 0: not-a-float"],
        ),
        # 4. 異常系: int不正
        (
            pd.DataFrame({
                'datetime': ['2025-07-01 12:00:00'],
                'name': ['Dave'],
                'value1': ['not-an-int'],
                'value11': [4.56],
            }),
            {'datetime': 'datetime', 'name': 'str', 'value1': 'int', 'value11': 'float'},
            pd.DataFrame({
                'datetime': ['2025-07-01 12:00:00'],
                'name': ['Dave'],
                'value1': [''],
                'value11': [4.56],
            }),
            ["Invalid int in value1 at row 0: not-an-int"],
        ),
        # 5. 異常系: 欠損値
        (
            pd.DataFrame({
                'datetime': [None],
                'name': [None],
                'value1': [None],
                'value11': [None],
            }),
            {'datetime': 'datetime', 'name': 'str', 'value1': 'int', 'value11': 'float'},
            pd.DataFrame({
                'datetime': [''],
                'name': [''],
                'value1': [''],
                'value11': [''],
            }),
            [],
        ),
        # 6. 境界値: 不要カラムがある
        (
            pd.DataFrame({
                'datetime': ['2025-07-01 12:00:00'],
                'name': ['Eve'],
                'value1': [5],
                'value11': [5.67],
                'extra': ['remove'],
            }),
            {'datetime': 'datetime', 'name': 'str', 'value1': 'int', 'value11': 'float'},
            pd.DataFrame({
                'datetime': ['2025-07-01 12:00:00'],
                'name': ['Eve'],
                'value1': [5],
                'value11': [5.67],
            }),
            [],
        ),
        # 7. 境界値: カラムが足りない
        (
            pd.DataFrame({
                'datetime': ['2025-07-01 12:00:00'],
                'name': ['Frank'],
            }),
            {'datetime': 'datetime', 'name': 'str', 'value1': 'int', 'value11': 'float'},
            pd.DataFrame({
                'datetime': ['2025-07-01 12:00:00'],
                'name': ['Frank'],
            }),
            [],
        ),
        # 8. str型: Noneや空文字
        (
            pd.DataFrame({
                'datetime': ['2025-07-01 12:00:00'],
                'name': [None],
                'value1': [8],
                'value11': [8.9],
            }),
            {'datetime': 'datetime', 'name': 'str', 'value1': 'int', 'value11': 'float'},
            pd.DataFrame({
                'datetime': ['2025-07-01 12:00:00'],
                'name': [''],
                'value1': [8],
                'value11': [8.9],
            }),
            [],
        ),
    ]
)
def test_check_values(df_input, column_types, expected_df, expected_warnings):
    result_df, warnings = check_process.check_values(df_input.copy(), column_types)
    # DataFrameの内容比較（dtypeをobjectに統一して比較）
    result_df = result_df.astype('object')
    expected_df = expected_df.astype('object')
    pd.testing.assert_frame_equal(result_df.reset_index(drop=True), expected_df.reset_index(drop=True), check_dtype=False)
    # 警告メッセージ比較
    assert warnings == expected_warnings
