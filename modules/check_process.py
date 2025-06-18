import pandas as pd  # データ操作用ライブラリ
import numpy as np  # 数値計算用
from datetime import datetime  # 日付解析用
import os  # OS操作用




def load_column_types(columns_file):
    """
    カラム型情報をファイルから読み込む。
    引数:
        columns_file (str): カラム情報ファイルへのパス。各行は 'column:type' 形式。
    戻り値:
        dict: カラム名と型のマッピング。
    """
    types = {}
    with open(columns_file, 'r') as f:
        for line in f:
            name, typ = line.strip().split(':')
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
                if pd.isnull(v) or v == '':
                    warnings.append(f"Empty or NULL in {col} at row {i}")
                    df.at[i, col] = ''
                    continue
                try:
                    datetime.strptime(str(v), '%Y-%m-%d %H:%M:%S')
                except Exception:
                    warnings.append(f"Invalid datetime in {col} at row {i}: {v}")
                    df.at[i, col] = ''
        elif typ == 'float':
            # float値かどうかをチェック
            for i, v in df[col].items():
                if pd.isnull(v) or v == '':
                    warnings.append(f"Empty or NULL in {col} at row {i}")
                    df.at[i, col] = ''
                    continue
                try:
                    float(v)
                except Exception:
                    warnings.append(f"Invalid float in {col} at row {i}: {v}")
                    df.at[i, col] = ''
        elif typ == 'int':
            # int値かどうかをチェック
            for i, v in df[col].items():
                if pd.isnull(v) or v == '':
                    warnings.append(f"Empty or NULL in {col} at row {i}")
                    df.at[i, col] = ''
                    continue
                try:
                    int(float(v))
                except Exception:
                    warnings.append(f"Invalid int in {col} at row {i}: {v}")
                    df.at[i, col] = ''
        elif typ == 'str':
            # 文字列型に変換し、欠損値（Noneなど）を空文字で補完
            for i, v in df[col].items():
                if pd.isnull(v) or v == '' or v is None:
                    warnings.append(f"Empty or NULL in {col} at row {i}")
                    df.at[i, col] = ''
            df[col] = df[col].replace({None: ''}).astype(str).fillna('')
    # 欠損値（NaNなど）を空文字で補完
    df = df.astype('object')
    df.fillna('', inplace=True)
    # column_typesに含まれない不要カラムを削除
    for col in df.columns:
        if col not in column_types:
            df.drop(col, axis=1, inplace=True)
    return df, warnings
