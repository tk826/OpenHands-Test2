import pandas as pd
import numpy as np
from datetime import datetime
import os

def load_column_types(columns_file):
    types = {}
    with open(columns_file, 'r') as f:
        for line in f:
            name, typ = line.strip().split(':')
            types[name] = typ
    return types

def check_values(df, column_types):
    warnings = []
    for col, typ in column_types.items():
        if col not in df.columns:
            continue
        if typ == 'datetime':
            for i, v in df[col].items():
                try:
                    if pd.isnull(v) or v == '':
                        continue
                    datetime.strptime(str(v), '%Y-%m-%d')
                except Exception:
                    warnings.append(f"Invalid datetime in {col} at row {i}: {v}")
                    df.at[i, col] = ''
        elif typ == 'float':
            for i, v in df[col].items():
                try:
                    if pd.isnull(v) or v == '':
                        continue
                    float(v)
                except Exception:
                    warnings.append(f"Invalid float in {col} at row {i}: {v}")
                    df.at[i, col] = ''
        elif typ == 'int':
            for i, v in df[col].items():
                try:
                    if pd.isnull(v) or v == '':
                        continue
                    int(float(v))
                except Exception:
                    warnings.append(f"Invalid int in {col} at row {i}: {v}")
                    df.at[i, col] = ''
        elif typ == 'str':
            df[col] = df[col].replace({None: ''}).astype(str).fillna('')
    # 欠損値補完
    df.fillna('', inplace=True)
    # 不要カラム削除
    for col in df.columns:
        if col not in column_types:
            df.drop(col, axis=1, inplace=True)
    return df, warnings
