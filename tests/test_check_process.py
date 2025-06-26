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
        'c': ['2020-01-01 12:00:00', '2020-13-01 00:00:00', ''],
        'd': [None, 'abc', 'def'],
        'e': [1, 2, 3]  # 余分なカラム

    })
    df2, warnings = check_values(df, column_types)
    assert 'Invalid int in a at row 1: x' in warnings
    assert 'Invalid float in b at row 1: bad' in warnings
    assert 'Invalid datetime in c at row 1: 2020-13-01 00:00:00' in warnings
    assert 'e' not in df2.columns
    assert df2['a'][1] == ''
    assert df2['b'][1] == ''
    assert df2['c'][1] == ''
    assert df2['d'][0] == ''

# テスト用のダミー関数を用意（本番mainはinput()を使うため直接呼ばない）
def test_grouped_output():
    import os
    import tempfile
    import pandas as pd
    import re
    from collections import defaultdict
    # テスト用ディレクトリとファイル作成
    with tempfile.TemporaryDirectory() as tmpdir:
        # columns.txt
        columns_path = os.path.join(tmpdir, 'columns.txt')
        with open(columns_path, 'w') as f:
            f.write('a:int\nb:str\n')
        # 入力ファイルを作成
        files = [
            (f'{tmpdir}/test/2025-06-12_9000.csv', 'a,b\n1,x\n'),
            (f'{tmpdir}/test/2025-06-12_9001.csv', 'a,b\n2,y\n'),
            (f'{tmpdir}/test1/2025-06-12_9000.csv', 'a,b\n3,z\n'),
            (f'{tmpdir}/test1/2025-06-12_9001.csv', 'a,b\n4,w\n'),
            (f'{tmpdir}/test1/2025-06-12_9002.csv', 'a,b\n5,v\n'),
        ]
        for path, content in files:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w') as f:
                f.write(content)
        # 疑似local_filesリストを作成
        # 新形式: グループ名/日付_時分.csv
        pattern = re.compile(r'([^/]+)/([0-9]{4}-[0-9]{2}-[0-9]{2})_([0-9]+)\.csv$')
        grouped = defaultdict(list)
        for path, _ in files:
            rel_path = os.path.relpath(path, tmpdir)
            m = pattern.match(rel_path)
            if m:
                group, date, time = m.group(1), m.group(2), m.group(3)
                grouped[(date, group)].append((int(time), path))
        # 本番同様にグループ化・ソート・出力
        column_types = {'a': 'int', 'b': 'str'}
        output_files = []
        for (date, group), filelist in grouped.items():
            filelist.sort()
            dfs = []
            for _, file in filelist:
                df = pd.read_csv(file)
                df, _ = check_values(df, column_types)
                dfs.append(df)
            if dfs:
                merged = pd.concat(dfs, ignore_index=True)
                outname = f"{date}_{group}.csv"
                outpath = os.path.join(tmpdir, outname)
                # --- 不要な.0を除去するための整形 ---
                def format_for_csv(df, column_types):
                    for col, typ in column_types.items():
                        if typ == 'float' and col in df.columns:
                            df[col] = df[col].apply(lambda x: '' if x == '' or pd.isnull(x) else (str(int(x)) if isinstance(x, (int, float)) and float(x).is_integer() else str(x)))
                    return df
                merged = format_for_csv(merged, column_types)
                merged.to_csv(outpath, index=False)
                output_files.append(outpath)
        # 検証: ファイル名と内容
        expected = {
            f'{tmpdir}/2025-06-12_test.csv': [(1, 'x'), (2, 'y')],
            f'{tmpdir}/2025-06-12_test1.csv': [(3, 'z'), (4, 'w'), (5, 'v')],
        }
        for outpath, rows in expected.items():
            assert os.path.exists(outpath)
            df = pd.read_csv(outpath)
            assert list(df['a']) == [r[0] for r in rows]
            assert list(df['b']) == [r[1] for r in rows]

        # float型の不要な.0が出力されていないことを検証するテスト
        # float型カラムで空文字や整数値が.0なしで出力されるか
        float_columns = {'a': 'float', 'b': 'str'}
        float_test_file = os.path.join(tmpdir, 'float_test.csv')
        pd.DataFrame({'a': ['42', '', '87.5'], 'b': ['x', 'y', 'z']}).to_csv(float_test_file, index=False)
        df = pd.read_csv(float_test_file)
        df, _ = check_values(df, float_columns)
        def format_for_csv(df, column_types):
            for col, typ in column_types.items():
                if typ == 'float' and col in df.columns:
                    df[col] = df[col].apply(lambda x: '' if x == '' or pd.isnull(x) else (str(int(x)) if isinstance(x, (int, float)) and float(x).is_integer() else str(x)))
            return df
        df = format_for_csv(df, float_columns)
        outpath = os.path.join(tmpdir, 'float_test_out.csv')
        df.to_csv(outpath, index=False)
        with open(outpath) as f:
            lines = f.read().splitlines()
        assert lines[1].startswith('42,'), f"Expected '42', got {lines[1]}"
        assert lines[2].startswith(','), f"Expected empty string, got {lines[2]}"
        assert lines[3].startswith('87.5,'), f"Expected '87.5', got {lines[3]}"



def test_unexpected_cases():
    import numpy as np
    import tempfile
    # 1. columns.txtに存在しないカラムが入力に含まれる場合
    column_types = {'a': 'int', 'b': 'float'}
    df = pd.DataFrame({'a': [1], 'b': [2.0], 'c': [3]})
    df2, warnings = check_values(df, column_types)
    assert 'c' not in df2.columns

    # 2. 型が全く異なる値（例: intカラムに"abc"や空リスト）が入っている場合
    df = pd.DataFrame({'a': ['abc', [], 5], 'b': [1.1, 2.2, 3.3]})
    df2, warnings = check_values(df, column_types)
    assert df2['a'][0] == ''
    assert df2['a'][1] == ''
    assert df2['a'][2] == 5 or df2['a'][2] == '5'

    # 3. 欠損値（None, NaN, 空文字, 空リスト, 空dict, 0, False, True, など）が各型でどう扱われるか
    df = pd.DataFrame({'a': [None, np.nan, '', [], {}, 0, False, True], 'b': [1.0]*8})
    df2, warnings = check_values(df, column_types)
    assert df2['a'][0] == ''
    assert df2['a'][1] == ''
    assert df2['a'][2] == ''
    assert df2['a'][3] == ''
    assert df2['a'][4] == ''
    # 0, False, Trueはint変換可能
    assert df2['a'][5] == 0 or df2['a'][5] == '0'
    assert df2['a'][6] == 0 or df2['a'][6] == '0'
    assert df2['a'][7] == 1 or df2['a'][7] == '1'

    # 4. 日付型カラムに不正な日付
    column_types2 = {'c': 'datetime'}
    df = pd.DataFrame({'c': ['2020-02-30 00:00:00', 'notadate', '2020-01-01 00:00:00']})
    df2, warnings = check_values(df, column_types2)
    assert df2['c'][0] == ''
    assert df2['c'][1] == ''
    assert df2['c'][2] == '2020-01-01 00:00:00'

    # 5. float/intカラムに極端な値
    df = pd.DataFrame({'a': ['1e1000', '-inf', 'nan', 1], 'b': [1.0]*4})
    df2, warnings = check_values(df, column_types)
    assert df2['a'][0] == ''  # 1e1000はfloat変換はできるがint変換はできない
    assert df2['a'][1] == ''
    assert df2['a'][2] == ''
    assert df2['a'][3] == 1 or df2['a'][3] == '1'

    # 6. strカラムに数値やNoneが入っている場合
    column_types3 = {'d': 'str'}
    df = pd.DataFrame({'d': [123, None, 4.56]})
    df2, warnings = check_values(df, column_types3)
    assert df2['d'][0] == '123'
    assert df2['d'][1] == ''
    assert df2['d'][2] == '4.56'

    # 7. DataFrame自体が空、カラムが空、全値が空文字/None/NaN
    df = pd.DataFrame({'a': [], 'b': []})
    df2, warnings = check_values(df, column_types)
    assert df2.empty
    df = pd.DataFrame({'a': [None, '', np.nan], 'b': [None, '', np.nan]})
    df2, warnings = check_values(df, column_types)
    assert all(x == '' for x in df2['a'])
    assert all(x == '' for x in df2['b'])

    # 8. columns.txtが空、または不正な形式
    with tempfile.NamedTemporaryFile('w+', delete=False) as f:
        f.write('')
        f.flush()
        types = load_column_types(f.name)
        assert types == {}
    with tempfile.NamedTemporaryFile('w+', delete=False) as f:
        f.write('badformatline\n')
        f.flush()
        try:
            load_column_types(f.name)
            assert False, 'Should raise ValueError for bad format'
        except ValueError:
            pass

    # 9. 入力ファイルが壊れている/パース不能
    # check_valuesはDataFrameを受け取るので、ファイルパース不能は上位層で例外となる想定
    # ここでは省略


