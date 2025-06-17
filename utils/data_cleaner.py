def clean_data(df):
    df = df.copy()
    df.drop_duplicates(inplace=True)
    df.fillna("N/A", inplace=True)
    return df
