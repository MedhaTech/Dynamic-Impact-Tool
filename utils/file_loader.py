import pandas as pd
import tempfile
import os

def load_data(uploaded_file):
    """Load data from uploaded CSV, Excel, or JSON files."""
    file_type = uploaded_file.name.lower()

    suffix = ".csv" if file_type.endswith(".csv") else ".xlsx" if file_type.endswith(".xlsx") else ".json"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.getbuffer())
        temp_path = tmp.name

    try:
        if file_type.endswith(".csv"):
            df = pd.read_csv(temp_path)
        elif file_type.endswith(".xlsx") or file_type.endswith(".xls"):
            df = pd.read_excel(temp_path)
        elif file_type.endswith(".json"):
            df = pd.read_json(temp_path)
        else:
            raise ValueError("Unsupported file format. Use CSV, Excel, or JSON.")
    finally:
        os.remove(temp_path)

    return df
