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
        return pd.read_csv(uploaded_file)
    elif file_name.endswith('.xlsx'):
        return pd.read_excel(uploaded_file)
    elif file_name.endswith('.json'):
        return pd.json_normalize(json.load(uploaded_file))
    elif file_name.endswith('.xml'):
        return pd.read_xml(uploaded_file)
    else:
        raise ValueError("Unsupported file format.")
   