# import pandas as pd
# import json
# import xmltodict
# import io

# def load_data(file) -> pd.DataFrame:
#     filename = file.name.lower()

#     try:
#         if filename.endswith('.csv'):
#             return pd.read_csv(file)
#         elif filename.endswith('.json'):
#             content = json.load(file)
#             if isinstance(content,dict):
#                 return pd.json_normalize(content)
#             elif isinstance(content,list):
#                 return pd.DataFrame(content)
#             else:
#                 raise ValueError("Unsupported json structure bro...")
#         elif filename.endswith('.xlsx'):
#             return pd.read_excel(file)
#         elif filename.endswith('.xml'):
#             content = file.read()
#             parsed = xmltodict.parse(content)
#             df = pd.json_normalize(parsed)
#             return df

#         else:
#             raise ValueError("Unsupported file format")

#     except Exception as e:
#         raise RuntimeError(f"Error while reading file: {e}")

import pandas as pd
import json

def load_data(uploaded_file):
    file_name = uploaded_file.name

    if file_name.endswith('.csv'):
        uploaded_file.seek(0)
        try:
            df = pd.read_csv(uploaded_file, encoding='utf-8')
            if df.empty or df.columns.size == 0:
                raise ValueError("No columns found in CSV (UTF-8).")
            return df
        except Exception:
            uploaded_file.seek(0)
            try:
                df = pd.read_csv(uploaded_file, encoding='latin1')
                if df.empty or df.columns.size == 0:
                    raise ValueError("No columns found in CSV (Latin-1).")
                return df
            except Exception as e:
                raise ValueError(f"Failed to load CSV file: {e}")

    elif file_name.endswith('.xlsx'):
        return pd.read_excel(uploaded_file)

    elif file_name.endswith('.json'):
        return pd.json_normalize(json.load(uploaded_file))

    elif file_name.endswith('.xml'):
        return pd.read_xml(uploaded_file)

    else:
        raise ValueError("Unsupported file format.")
