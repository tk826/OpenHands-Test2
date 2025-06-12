import pandas as pd  # データ操作用ライブラリ
import numpy as np  # 数値計算用
from datetime import datetime  # 日付解析用
import os  # OS操作用




def load_column_types(columns_file):
    """
    Load column types from a file.
    Args:
        columns_file (str): Path to the columns file. Each line should be 'column:type'.
    Returns:
        dict: Mapping of column names to types.
    """
    types = {}
    with open(columns_file, 'r') as f:
        for line in f:
            name, typ = line.strip().split(':')
            types[name] = typ
    return types

def check_values(df, column_types):
    """
    Check and clean values in the DataFrame according to column types.
    Args:
        df (pd.DataFrame): Input DataFrame.
        column_types (dict): Mapping of column names to types ('datetime', 'float', 'int', 'str').
    Returns:
        tuple: (Cleaned DataFrame, list of warning messages)
    """
    warnings = []
    for col, typ in column_types.items():
        if col not in df.columns:
            continue  # 存在しないカラムはスキップ
        if typ == 'datetime':
            # 日付フォーマットをチェック
            for i, v in df[col].items():
                try:
                    if pd.isnull(v) or v == '':
                        continue
                    datetime.strptime(str(v), '%Y-%m-%d')
                except Exception:
                    warnings.append(f"Invalid datetime in {col} at row {i}: {v}")
                    df.at[i, col] = ''
        elif typ == 'float':
            # float値をチェック
            for i, v in df[col].items():
                try:
                    if pd.isnull(v) or v == '':
                        continue
                    float(v)
                except Exception:
                    warnings.append(f"Invalid float in {col} at row {i}: {v}")
                    df.at[i, col] = ''
        elif typ == 'int':
            # int値をチェック
            for i, v in df[col].items():
                try:
                    if pd.isnull(v) or v == '':
                        continue
                    int(float(v))
                except Exception:
                    warnings.append(f"Invalid int in {col} at row {i}: {v}")
                    df.at[i, col] = ''
        elif typ == 'str':
            # 文字列型に変換し、欠損値を補完
            df[col] = df[col].replace({None: ''}).astype(str).fillna('')
    # 欠損値補完
    df.fillna('', inplace=True)
    # 不要カラム削除
    for col in df.columns:
        if col not in column_types:
            df.drop(col, axis=1, inplace=True)
    return df, warnings
