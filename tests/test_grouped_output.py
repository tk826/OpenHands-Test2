import os
import tempfile
import pandas as pd
from modules.check_process import load_column_types, check_values
import re
from collections import defaultdict

# テスト用のダミー関数を用意（本番mainはinput()を使うため直接呼ばない）
def test_grouped_output():
    # テスト用ディレクトリとファイル作成
    with tempfile.TemporaryDirectory() as tmpdir:
        # columns.txt
        columns_path = os.path.join(tmpdir, 'columns.txt')
        with open(columns_path, 'w') as f:
            f.write('a:int\nb:str\n')
        # 入力ファイルを作成
        files = [
            (f'{tmpdir}/2025-06-12_9000_test.csv', 'a,b\n1,x\n'),
            (f'{tmpdir}/2025-06-12_9001_test.csv', 'a,b\n2,y\n'),
            (f'{tmpdir}/2025-06-12_9000_test1.csv', 'a,b\n3,z\n'),
            (f'{tmpdir}/2025-06-12_9001_test1.csv', 'a,b\n4,w\n'),
            (f'{tmpdir}/2025-06-12_9002_test1.csv', 'a,b\n5,v\n'),
        ]
        for path, content in files:
            with open(path, 'w') as f:
                f.write(content)
        # 疑似local_filesリストを作成
        pattern = re.compile(r'(\d{4}-\d{2}-\d{2})_(\d+)_([^.]+)\.csv$')
        grouped = defaultdict(list)
        for path, _ in files:
            m = pattern.search(os.path.basename(path))
            if m:
                date, time, group = m.group(1), m.group(2), m.group(3)
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

