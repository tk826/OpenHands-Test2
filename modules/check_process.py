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
    if columns_file is None:
        raise ValueError("columns_file is None / カラム情報ファイルがNoneです")
    types = {}
    with open(columns_file, 'r') as f:
        lines = f.readlines()
        if not lines or all(line.strip() == '' for line in lines):
            raise ValueError("columns_file is empty / カラム情報ファイルが空です")
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if ':' not in line:
                raise ValueError("invalid format in columns_file / カラム情報ファイルの形式が不正です")
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
                    warnings.append(f"Invalid datetime in {col} at row {i}: {str(v).strip()} / {col}列の{i}行目の値が日付形式ではありません: {str(v).strip()}")
                    df.at[i, col] = ''
        elif typ == 'float':
            # float値かどうかをチェック
            for i, v in df[col].items():
                try:
                    if pd.isnull(v) or v == '':
                        continue
                    float(v)
                except Exception:
                    warnings.append(f"Invalid float in {col} at row {i}: {str(v).strip()} / {col}列の{i}行目の値が数値(float)ではありません: {str(v).strip()}")
                    df.at[i, col] = ''
        elif typ == 'int':
            # int値かどうかをチェック
            for i, v in df[col].items():
                try:
                    if pd.isnull(v) or v == '':
                        continue
                    int(float(v))
                except Exception:
                    warnings.append(f"Invalid int in {col} at row {i}: {str(v).strip()} / {col}列の{i}行目の値が整数(int)ではありません: {str(v).strip()}")
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
