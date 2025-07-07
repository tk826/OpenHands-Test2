import pandas as pd  # データ操作用ライブラリ
import numpy as np  # 数値計算用
from datetime import datetime  # 日付解析用
import os  # OS操作用



# デシジョンテーブル（条件と動作の整理例）
# | 条件                | 規則1 | 規則2 | 規則3 | 規則4 | 規則5 |
# |---------------------|-------|-------|-------|-------|-------|
# | 大学生または高校生   | Y     | N     | N     | Y     | N     |
# | 中学生以下           | N     | Y     | N     | N     | N     |
# | 女性                | Y     | Y     | N     | N     | Y     |
# | 動作:学生割引(10%)   | X     | -     | -     | X     | -     |
# | 動作:子ども割引(50%) | -     | X     | -     | -     | -     |
# | 動作:レディース割引(5%)| -    | -     | -     | -     | X     |
#
# ポイント：
# - 条件が複数該当する場合、最も割引率が高いものが適用される
# - 「Y」は条件が真、「N」は偽、「X」はその動作が実行されることを示す
# - 規則1～5で足りなければ規則を追加して全パターンを網羅する

# --- デシジョンテーブル（check_process.py用） ---
# | 条件                   | 規則1 | 規則2 | 規則3 | 規則4 | 規則5 | 規則6 | 規則7 | 規則8 |
# |------------------------|-------|-------|-------|-------|-------|-------|-------|-------|
# | columns_file=None      | Y     | N     | N     | N     | N     | N     | N     | N     |
# | columns_file空         | N     | Y     | N     | N     | N     | N     | N     | N     |
# | columns_file形式不正   | N     | N     | Y     | N     | N     | N     | N     | N     |
# | columns_file正常       | N     | N     | N     | Y     | N     | N     | N     | N     |
# | dfに不要カラムあり     | N     | N     | N     | N     | Y     | N     | N     | N     |
# | df値型不正             | N     | N     | N     | N     | N     | Y     | N     | N     |
# | df値欠損               | N     | N     | N     | N     | N     | N     | Y     | N     |
# | column_types空         | N     | N     | N     | N     | N     | N     | N     | Y     |
# | 動作:ValueError        | X     | X     | X     | -     | -     | -     | -     | -     |
# | 動作:正常dict返却      | -     | -     | -     | X     | -     | -     | -     | -     |
# | 動作:不要カラム削除    | -     | -     | -     | -     | X     | -     | -     | -     |
# | 動作:型不正値警告      | -     | -     | -     | -     | -     | X     | -     | -     |
# | 動作:欠損値空文字      | -     | -     | -     | -     | -     | -     | X     | -     |
# | 動作:空DataFrame返却   | -     | -     | -     | -     | -     | -     | -     | X     |
#
# ポイント：
# - 条件が複数該当する場合、ValueErrorが最優先
# - それ以外は正常系、不要カラム削除、型不正警告、欠損値補完、空DataFrame返却の順で適用


def load_column_types(columns_file):
    """
    カラム型情報をファイルから読み込む。
    引数:
        columns_file (str): カラム情報ファイルへのパス。各行は 'column:type' 形式。
    戻り値:
        dict: カラム名と型のマッピング。
    """
    if columns_file is None:
        raise ValueError("columns_file is None")
    types = {}
    with open(columns_file, 'r') as f:
        lines = f.readlines()
        if not lines or all(line.strip() == '' for line in lines):
            raise ValueError("columns_file is empty")
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if ':' not in line:
                raise ValueError("invalid format in columns_file")
            name, typ = line.split(':', 1)
            types[name] = typ
    return types

def check_values(df, column_types):
    """
    DataFrame内の値をカラム型に従ってチェック・クリーニングする。
    引数:
        df (pd.DataFrame): 入力DataFrame。
        column_types (dict): カラム名と型（'datetime', 'float', 'int', 'str'）のマッピング。
    戻り値:
        tuple: (クリーニング済みDataFrame, 警告メッセージのリスト)
    """
    warnings = []
    for col, typ in column_types.items():
        if col not in df.columns:
            continue  # 存在しないカラムはスキップ
        if typ == 'datetime':
            # 日付フォーマットをチェック（YYYY-MM-DD形式）
            for i, v in df[col].items():
                try:
                    if pd.isnull(v) or v == '':
                        continue
                    datetime.strptime(str(v), '%Y-%m-%d %H:%M:%S')
                except Exception:
                    warnings.append(f"Invalid datetime in {col} at row {i}: {v}")
                    df.at[i, col] = ''
        elif typ == 'float':
            # float値かどうかをチェック
            for i, v in df[col].items():
                try:
                    if pd.isnull(v) or v == '':
                        continue
                    float(v)
                except Exception:
                    warnings.append(f"Invalid float in {col} at row {i}: {v}")
                    df.at[i, col] = ''
        elif typ == 'int':
            # int値かどうかをチェック
            for i, v in df[col].items():
                try:
                    if pd.isnull(v) or v == '':
                        continue
                    int(float(v))
                except Exception:
                    warnings.append(f"Invalid int in {col} at row {i}: {v}")
                    df.at[i, col] = ''
        elif typ == 'str':
            # 文字列型に変換し、欠損値（Noneなど）を空文字で補完
            df[col] = df[col].replace({None: ''}).astype(str).fillna('')
    # 欠損値（NaNなど）を空文字で補完
    df = df.astype('object')
    df.fillna('', inplace=True)
    # column_typesに含まれない不要カラムを削除
    for col in df.columns:
        if col not in column_types:
            df.drop(col, axis=1, inplace=True)
    return df, warnings
