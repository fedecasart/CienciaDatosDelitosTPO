"""
Module containing reusable functions for cleaning and preprocessing raw crime data.
"""

import pandas as pd
import numpy as np

def standardize_headers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardizes dataframe column names by stripping whitespace, 
    replacing spaces/punctuation with underscores, and converting to lowercase.
    """
    df_clean = df.copy()
    df_clean.columns = (
        df_clean.columns
        .str.strip()
        .str.lower()
        .str.replace(r'[^\w\s]', '', regex=True)
        .str.replace(r'\s+', '_', regex=True)
    )
    return df_clean

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Identifies and removes duplicate records from the dataset, 
    logging the count of dropped rows.
    """
    initial_rows = len(df)
    df_clean = df.drop_duplicates()
    dropped_rows = initial_rows - len(df_clean)
    print(f"Removed {dropped_rows} duplicate records out of {initial_rows} total rows.")
    return df_clean

def parse_dates(df: pd.DataFrame, date_column: str, date_format: str = None) -> pd.DataFrame:
    """
    Converts a column to datetime format, handling errors gracefully, 
    and extracts basic temporal features (year, month, day, hour, day_of_week).
    """
    df_clean = df.copy()
    df_clean[date_column] = pd.to_datetime(df_clean[date_column], format=date_format, errors='coerce')
    
    # Feature extraction (extracting time attributes is standard practice in crime mining)
    df_clean['year'] = df_clean[date_column].dt.year
    df_clean['month'] = df_clean[date_column].dt.month
    df_clean['day'] = df_clean[date_column].dt.day
    df_clean['hour'] = df_clean[date_column].dt.hour
    df_clean['day_of_week'] = df_clean[date_column].dt.day_name()
    
    return df_clean

def impute_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Imputes or flags missing data depending on the column type.
    Must be customized once data schema is known.
    """
    df_clean = df.copy()
    # Placeholder implementation: fill NaNs in object columns with 'UNKNOWN'
    object_cols = df_clean.select_dtypes(include=['object']).columns
    df_clean[object_cols] = df_clean[object_cols].fillna('UNKNOWN')
    
    return df_clean
