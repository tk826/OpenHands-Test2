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
