import pandas as pd
import io

import pandas as pd
import os


def load_data(file, file_name=None):
    try:
        if isinstance(file, str):
            if file.endswith('.csv'):
                df = pd.read_csv(file)
            elif file.endswith('.xlsx'):
                df = pd.read_excel(file)
            elif file.endswith('.json'):
                df = pd.read_json(file)
            else:
                raise ValueError("Unsupported file type.")
        else:
            # When loading from BytesIO, use the provided file name to determine type
            if file_name and file_name.endswith('.csv'):
                df = pd.read_csv(file)
            elif file_name and file_name.endswith('.xlsx'):
                df = pd.read_excel(file)
            elif file_name and file_name.endswith('.json'):
                df = pd.read_json(file)
            else:
                raise ValueError("Unsupported file type.")
        return df, None
    except Exception as e:
        raise RuntimeError(f"Failed to load data: {str(e)}")
    
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Basic data cleaning: trims spaces in column names and drops fully null columns.
    """
    df.columns = [col.strip().lower() for col in df.columns]
    df = df.dropna(axis=1, how="all")
    return df
