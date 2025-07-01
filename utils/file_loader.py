import pandas as pd
<<<<<<< HEAD
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
=======
import os
import io

def load_data(file, sample_rows=None):
    if hasattr(file, "read"):
        name = file.name
        ext = name.split(".")[-1].lower()
    elif isinstance(file, str):
        name = file
        ext = file.split(".")[-1].lower()
    else:
        raise ValueError("Unsupported file type")

    if ext == "csv":
        df = pd.read_csv(file)
    elif ext in ["xlsx", "xls"]:
        df = pd.read_excel(file)
    elif ext == "json":
        df = pd.read_json(file)
    elif ext == "txt":
        df = pd.read_csv(file, delimiter="\t")
    else:
        raise ValueError("Unsupported file extension")

    if sample_rows:
        df = df.sample(n=sample_rows, random_state=42)

    return df, name
>>>>>>> e1bab98 (Modified the code)
