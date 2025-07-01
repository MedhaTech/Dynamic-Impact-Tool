import pandas as pd

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.dropna(axis=1, how="all")
    df = df.drop_duplicates()
    df.columns = [col.strip().replace("\n", " ") for col in df.columns]
    return df
