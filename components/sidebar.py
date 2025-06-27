# import streamlit as st
# from utils.data_loader import load_dataset
# from state.session_manager import reset_dataset_a_state, reset_dataset_b_state
# import os

# def render_sidebar():
#     st.sidebar.header("📁 Upload & Select Datasets")

#     row_limit = st.sidebar.slider("Sample Rows", 100, 20000, 1000, step=100)

#     # Dataset A Upload Mode
#     st.sidebar.markdown("### Dataset A")
#     upload_mode_a = st.sidebar.radio("Upload Mode (A)", ["Browse", "Path (large files)"], key="upload_mode_a")

#     if upload_mode_a == "Browse":
#         uploaded_file1 = st.sidebar.file_uploader("Upload CSV/XLSX for Dataset A", type=["csv", "xlsx"], key="file1")
#         if uploaded_file1 and st.session_state.get("df1") is None:
#             try:
#                 reset_dataset_a_state()
#                 df1 = load_dataset(uploaded_file1, row_limit)
#                 st.session_state.df1 = df1
#                 st.session_state.df1_cols = df1.columns.tolist()
#                 st.sidebar.success(f"Loaded A: {df1.shape[0]} rows × {df1.shape[1]} cols")
#             except Exception as e:
#                 st.sidebar.error(f"Error loading A: {e}")
#     else:
#         file_path1 = st.sidebar.text_input("Enter file path for Dataset A", key="file_path_1")
#         if file_path1 and os.path.exists(file_path1) and st.session_state.get("df1") is None:
#             try:
#                 reset_dataset_a_state()
#                 df1 = load_dataset(file_path1, row_limit, is_path=True)
#                 st.session_state.df1 = df1
#                 st.session_state.df1_cols = df1.columns.tolist()
#                 st.sidebar.success(f"Loaded A: {df1.shape[0]} rows × {df1.shape[1]} cols")
#             except Exception as e:
#                 st.sidebar.error(f"Error loading A: {e}")

#     # Dataset B Upload Mode
#     st.sidebar.markdown("### Dataset B")
#     upload_mode_b = st.sidebar.radio("Upload Mode (B)", ["Browse", "Path (large files)"], key="upload_mode_b")

#     if upload_mode_b == "Browse":
#         uploaded_file2 = st.sidebar.file_uploader("Upload CSV/XLSX for Dataset B", type=["csv", "xlsx"], key="file2")
#         if uploaded_file2 and st.session_state.get("df2") is None:
#             try:
#                 reset_dataset_b_state()
#                 df2 = load_dataset(uploaded_file2, row_limit)
#                 st.session_state.df2 = df2
#                 st.session_state.df2_cols = df2.columns.tolist()
#                 st.sidebar.success(f"Loaded B: {df2.shape[0]} rows × {df2.shape[1]} cols")
#             except Exception as e:
#                 st.sidebar.error(f"Error loading B: {e}")
#     else:
#         file_path2 = st.sidebar.text_input("Enter file path for Dataset B", key="file_path_2")
#         if file_path2 and os.path.exists(file_path2) and st.session_state.get("df2") is None:
#             try:
#                 reset_dataset_b_state()
#                 df2 = load_dataset(file_path2, row_limit, is_path=True)
#                 st.session_state.df2 = df2
#                 st.session_state.df2_cols = df2.columns.tolist()
#                 st.sidebar.success(f"Loaded B: {df2.shape[0]} rows × {df2.shape[1]} cols")
#             except Exception as e:
#                 st.sidebar.error(f"Error loading B: {e}")

#     # Column selectors
#     if st.session_state.get("df1") is not None:
#         selected_cols_1 = st.sidebar.multiselect("Columns to analyze (Dataset A)", st.session_state.df1_cols, default=st.session_state.df1_cols[:5])
#         st.session_state.selected_cols_1 = selected_cols_1

#     if st.session_state.get("df2") is not None:
#         selected_cols_2 = st.sidebar.multiselect("Columns to analyze (Dataset B)", st.session_state.df2_cols, default=st.session_state.df2_cols[:5])
#         st.session_state.selected_cols_2 = selected_cols_2

#     # Tab Selector
#     st.sidebar.markdown("---")
#     selected_tab = st.sidebar.radio("Navigate", ["Summary", "Insights", "Comparison"], key="tab_selector")
#     st.session_state.selected_tab = selected_tab

  
    

# import streamlit as st
# import os
# from utils.data_loader import load_dataset
# from state.session_manager import reset_dataset_a_state, reset_dataset_b_state

# def render_sidebar():
#     st.sidebar.header("📁 Upload & Controls")

#     row_limit = st.sidebar.slider("Sample Rows", 100, 20000, 1000, step=100)

#     # ------------------- Dataset A ------------------- #
#     st.sidebar.markdown("### Dataset A")
#     upload_mode_a = st.sidebar.radio("Upload Mode (A)", ["Browse", "Path (large files)"], key="upload_mode_a")

#     if upload_mode_a == "Browse":
#         uploaded_file1 = st.sidebar.file_uploader("Upload CSV/XLSX for Dataset A", type=["csv", "xlsx"], key="file1")

#         if uploaded_file1:
#             reset_dataset_a_state()
#             try:
#                 df1 = load_dataset(uploaded_file1, row_limit)
#                 st.session_state.df1 = df1
#                 st.session_state.df1_cols = df1.columns.tolist()
#                 st.session_state.selected_cols_1 = df1.columns.tolist()[:5]
#                 st.sidebar.success(f"Dataset A Loaded: {df1.shape[0]} rows × {df1.shape[1]} cols")
#                 st.rerun()  # force update
#             except Exception as e:
#                 st.sidebar.error(f"Error loading Dataset A: {e}")

#     else:
#         file_path1 = st.sidebar.text_input("Enter file path for Dataset A", key="file_path_1")
#         if file_path1 and os.path.exists(file_path1):
#             reset_dataset_a_state()
#             try:
#                 df1 = load_dataset(file_path1, row_limit, is_path=True)
#                 st.session_state.df1 = df1
#                 st.session_state.df1_cols = df1.columns.tolist()
#                 st.session_state.selected_cols_1 = df1.columns.tolist()[:5]
#                 st.sidebar.success(f"Dataset A Loaded: {df1.shape[0]} rows × {df1.shape[1]} cols")
#                 st.rerun()
#             except Exception as e:
#                 st.sidebar.error(f"Error loading Dataset A: {e}")

#     if st.session_state.get("df1_cols"):
#         selected_cols_1 = st.sidebar.multiselect(
#             "Select columns for Dataset A",
#             st.session_state.df1_cols,
#             default=st.session_state.get("selected_cols_1", st.session_state.df1_cols[:5]),
#             key="select_cols_1"
#         )
#         st.session_state.selected_cols_1 = selected_cols_1

#     # ------------------- Dataset B ------------------- #
#     st.sidebar.markdown("### Dataset B")
#     upload_mode_b = st.sidebar.radio("Upload Mode (B)", ["Browse", "Path (large files)"], key="upload_mode_b")

#     if upload_mode_b == "Browse":
#         uploaded_file2 = st.sidebar.file_uploader("Upload CSV/XLSX for Dataset B", type=["csv", "xlsx"], key="file2")

#         if uploaded_file2:
#             reset_dataset_b_state()
#             try:
#                 df2 = load_dataset(uploaded_file2, row_limit)
#                 st.session_state.df2 = df2
#                 st.session_state.df2_cols = df2.columns.tolist()
#                 st.session_state.selected_cols_2 = df2.columns.tolist()[:5]
#                 st.sidebar.success(f"Dataset B Loaded: {df2.shape[0]} rows × {df2.shape[1]} cols")
#                 st.rerun()
#             except Exception as e:
#                 st.sidebar.error(f"Error loading Dataset B: {e}")

#     else:
#         file_path2 = st.sidebar.text_input("Enter file path for Dataset B", key="file_path_2")
#         if file_path2 and os.path.exists(file_path2):
#             reset_dataset_b_state()
#             try:
#                 df2 = load_dataset(file_path2, row_limit, is_path=True)
#                 st.session_state.df2 = df2
#                 st.session_state.df2_cols = df2.columns.tolist()
#                 st.session_state.selected_cols_2 = df2.columns.tolist()[:5]
#                 st.sidebar.success(f"Dataset B Loaded: {df2.shape[0]} rows × {df2.shape[1]} cols")
#                 st.rerun()
#             except Exception as e:
#                 st.sidebar.error(f"Error loading Dataset B: {e}")

#     if st.session_state.get("df2_cols"):
#         selected_cols_2 = st.sidebar.multiselect(
#             "Select columns for Dataset B",
#             st.session_state.df2_cols,
#             default=st.session_state.get("selected_cols_2", st.session_state.df2_cols[:5]),
#             key="select_cols_2"
#         )
#         st.session_state.selected_cols_2 = selected_cols_2

#     # ------------------- Tab Navigation ------------------- #
#     st.sidebar.markdown("---")
#     tab = st.sidebar.radio("Navigate", ["Summary", "Insights", "Comparison"], key="tab_selector")
#     st.session_state.selected_tab = tab

#     # ------------------- Debug Tools (Optional) ------------------- #
#     with st.sidebar.expander("⚙ Debug Info"):
#         st.write("df1:", type(st.session_state.get("df1")))
#         st.write("df2:", type(st.session_state.get("df2")))
#         st.write("selected_cols_1:", st.session_state.get("selected_cols_1"))
#         st.write("selected_cols_2:", st.session_state.get("selected_cols_2"))



# import streamlit as st
# import os
# from utils.data_loader import load_dataset
# from state.session_manager import reset_dataset_a_state, reset_dataset_b_state

# def render_sidebar():
#     st.sidebar.header("📁 Upload & Controls")

#     row_limit = st.sidebar.slider("Sample Rows", 100, 20000, 1000, step=100)

#     # --- Dataset A ---
#     st.sidebar.markdown("### Dataset A")
#     upload_mode_a = st.sidebar.radio("Upload Mode (A)", ["Browse", "Path (large files)"], key="upload_mode_a")

#     if upload_mode_a == "Browse":
#         uploaded_file1 = st.sidebar.file_uploader("Upload Dataset A", type=["csv", "xlsx"], key="file1")

#         if uploaded_file1 and not st.session_state.get("df1_loaded", False):
#             reset_dataset_a_state()
#             try:
#                 df1 = load_dataset(uploaded_file1, row_limit)
#                 st.session_state.df1 = df1
#                 st.session_state.df1_cols = df1.columns.tolist()
#                 st.session_state.selected_cols_1 = df1.columns.tolist()[:5]
#                 st.session_state.df1_loaded = True
#                 st.sidebar.success(f"Dataset A Loaded: {df1.shape[0]} rows × {df1.shape[1]} cols")
#                 st.rerun()
#             except Exception as e:
#                 st.sidebar.error(f"Error loading Dataset A: {e}")

#     else:
#         file_path1 = st.sidebar.text_input("Enter file path for Dataset A", key="file_path_1")
#         if file_path1 and os.path.exists(file_path1) and not st.session_state.get("df1_loaded", False):
#             reset_dataset_a_state()
#             try:
#                 df1 = load_dataset(file_path1, row_limit, is_path=True)
#                 st.session_state.df1 = df1
#                 st.session_state.df1_cols = df1.columns.tolist()
#                 st.session_state.selected_cols_1 = df1.columns.tolist()[:5]
#                 st.session_state.df1_loaded = True
#                 st.sidebar.success(f"Dataset A Loaded: {df1.shape[0]} rows × {df1.shape[1]} cols")
#                 st.rerun()
#             except Exception as e:
#                 st.sidebar.error(f"Error loading Dataset A: {e}")

#     if st.session_state.get("df1_cols"):
#         selected_cols_1 = st.sidebar.multiselect(
#             "Select columns for Dataset A",
#             st.session_state.df1_cols,
#             default=st.session_state.get("selected_cols_1", st.session_state.df1_cols[:5]),
#             key="select_cols_1"
#         )
#         st.session_state.selected_cols_1 = selected_cols_1

#     # --- Dataset B ---
#     st.sidebar.markdown("### Dataset B")
#     upload_mode_b = st.sidebar.radio("Upload Mode (B)", ["Browse", "Path (large files)"], key="upload_mode_b")

#     if upload_mode_b == "Browse":
#         uploaded_file2 = st.sidebar.file_uploader("Upload Dataset B", type=["csv", "xlsx"], key="file2")

#         if uploaded_file2 and not st.session_state.get("df2_loaded", False):
#             reset_dataset_b_state()
#             try:
#                 df2 = load_dataset(uploaded_file2, row_limit)
#                 st.session_state.df2 = df2
#                 st.session_state.df2_cols = df2.columns.tolist()
#                 st.session_state.selected_cols_2 = df2.columns.tolist()[:5]
#                 st.session_state.df2_loaded = True
#                 st.sidebar.success(f"Dataset B Loaded: {df2.shape[0]} rows × {df2.shape[1]} cols")
#                 st.rerun()
#             except Exception as e:
#                 st.sidebar.error(f"Error loading Dataset B: {e}")

#     else:
#         file_path2 = st.sidebar.text_input("Enter file path for Dataset B", key="file_path_2")
#         if file_path2 and os.path.exists(file_path2) and not st.session_state.get("df2_loaded", False):
#             reset_dataset_b_state()
#             try:
#                 df2 = load_dataset(file_path2, row_limit, is_path=True)
#                 st.session_state.df2 = df2
#                 st.session_state.df2_cols = df2.columns.tolist()
#                 st.session_state.selected_cols_2 = df2.columns.tolist()[:5]
#                 st.session_state.df2_loaded = True
#                 st.sidebar.success(f"Dataset B Loaded: {df2.shape[0]} rows × {df2.shape[1]} cols")
#                 st.rerun()
#             except Exception as e:
#                 st.sidebar.error(f"Error loading Dataset B: {e}")

#     if st.session_state.get("df2_cols"):
#         selected_cols_2 = st.sidebar.multiselect(
#             "Select columns for Dataset B",
#             st.session_state.df2_cols,
#             default=st.session_state.get("selected_cols_2", st.session_state.df2_cols[:5]),
#             key="select_cols_2"
#         )
#         st.session_state.selected_cols_2 = selected_cols_2

#     # --- Tab Navigation ---
#     st.sidebar.markdown("---")
#     tab = st.sidebar.radio("Navigate", ["Summary", "Insights", "Comparison"], key="tab_selector")
#     st.session_state.selected_tab = tab

#     # --- Reset Button (Optional Dev) ---
#     if st.sidebar.button("🔄 Reset All (Dev)", key="reset_all_btn"):
#         st.session_state.clear()
#         st.rerun()

#     with st.sidebar.expander("🛠 Debug Info"):
#         st.write("df1_loaded:", st.session_state.get("df1_loaded"))
#         st.write("df2_loaded:", st.session_state.get("df2_loaded"))
#         st.write("selected_cols_1:", st.session_state.get("selected_cols_1"))
#         st.write("selected_cols_2:", st.session_state.get("selected_cols_2"))


#4th code

import streamlit as st
import os
import hashlib
from utils.data_loader import load_dataset
from state.session_manager import reset_dataset_a_state, reset_dataset_b_state

def get_file_hash(uploaded_file):
    """Generate a unique hash for uploaded file to detect change."""
    return hashlib.md5(uploaded_file.getvalue()).hexdigest()

def render_sidebar():
    st.sidebar.header("📁 Upload & Controls")

    row_limit = st.sidebar.slider("Sample Rows", 100, 20000, 1000, step=100)

    # ------------------- Dataset A ------------------- #
    st.sidebar.markdown("### Dataset A")
    upload_mode_a = st.sidebar.radio("Upload Mode (A)", ["Browse", "Path (large files)"], key="upload_mode_a")

    if upload_mode_a == "Browse":
        uploaded_file1 = st.sidebar.file_uploader("Upload Dataset A", type=["csv", "xlsx"], key="file1")

        if uploaded_file1:
            file_hash = get_file_hash(uploaded_file1)
            current_hash = st.session_state.get("file1_hash")

            if file_hash != current_hash or not st.session_state.get("df1_loaded", False):
                reset_dataset_a_state()
                try:
                    df1 = load_dataset(uploaded_file1, row_limit)
                    st.session_state.df1 = df1
                    st.session_state.df1_cols = df1.columns.tolist()
                    st.session_state.selected_cols_1 = df1.columns.tolist()[:5]
                    st.session_state.df1_loaded = True
                    st.session_state.file1_hash = file_hash
                    st.sidebar.success(f"Dataset A Loaded: {df1.shape[0]} rows × {df1.shape[1]} cols")
                    st.rerun()
                except Exception as e:
                    st.sidebar.error(f"Error loading Dataset A: {e}")

    else:
        file_path1 = st.sidebar.text_input("Enter file path for Dataset A", key="file_path_1")
        if file_path1 and os.path.exists(file_path1):
            if st.sidebar.button("📥 Load Dataset A from Path"):
                reset_dataset_a_state()
                try:
                    df1 = load_dataset(file_path1, row_limit, is_path=True)
                    st.session_state.df1 = df1
                    st.session_state.df1_cols = df1.columns.tolist()
                    st.session_state.selected_cols_1 = df1.columns.tolist()[:5]
                    st.session_state.df1_loaded = True
                    st.sidebar.success(f"Dataset A Loaded: {df1.shape[0]} rows × {df1.shape[1]} cols")
                    st.rerun()
                except Exception as e:
                    st.sidebar.error(f"Error loading Dataset A: {e}")

    if st.session_state.get("df1_cols"):
        selected_cols_1 = st.sidebar.multiselect(
            "Select columns for Dataset A",
            st.session_state.df1_cols,
            default=st.session_state.get("selected_cols_1", st.session_state.df1_cols[:5]),
            key="select_cols_1"
        )
        st.session_state.selected_cols_1 = selected_cols_1

    # ------------------- Dataset B ------------------- #
    st.sidebar.markdown("### Dataset B")
    upload_mode_b = st.sidebar.radio("Upload Mode (B)", ["Browse", "Path (large files)"], key="upload_mode_b")

    if upload_mode_b == "Browse":
        uploaded_file2 = st.sidebar.file_uploader("Upload Dataset B", type=["csv", "xlsx"], key="file2")

        if uploaded_file2:
            file_hash = get_file_hash(uploaded_file2)
            current_hash = st.session_state.get("file2_hash")

            if file_hash != current_hash or not st.session_state.get("df2_loaded", False):
                reset_dataset_b_state()
                try:
                    df2 = load_dataset(uploaded_file2, row_limit)
                    st.session_state.df2 = df2
                    st.session_state.df2_cols = df2.columns.tolist()
                    st.session_state.selected_cols_2 = df2.columns.tolist()[:5]
                    st.session_state.df2_loaded = True
                    st.session_state.file2_hash = file_hash
                    st.sidebar.success(f"Dataset B Loaded: {df2.shape[0]} rows × {df2.shape[1]} cols")
                    st.rerun()
                except Exception as e:
                    st.sidebar.error(f"Error loading Dataset B: {e}")

    else:
        file_path2 = st.sidebar.text_input("Enter file path for Dataset B", key="file_path_2")
        if file_path2 and os.path.exists(file_path2):
            if st.sidebar.button("📥 Load Dataset B from Path"):
                reset_dataset_b_state()
                try:
                    df2 = load_dataset(file_path2, row_limit, is_path=True)
                    st.session_state.df2 = df2
                    st.session_state.df2_cols = df2.columns.tolist()
                    st.session_state.selected_cols_2 = df2.columns.tolist()[:5]
                    st.session_state.df2_loaded = True
                    st.sidebar.success(f"Dataset B Loaded: {df2.shape[0]} rows × {df2.shape[1]} cols")
                    st.rerun()
                except Exception as e:
                    st.sidebar.error(f"Error loading Dataset B: {e}")

    if st.session_state.get("df2_cols"):
        selected_cols_2 = st.sidebar.multiselect(
            "Select columns for Dataset B",
            st.session_state.df2_cols,
            default=st.session_state.get("selected_cols_2", st.session_state.df2_cols[:5]),
            key="select_cols_2"
        )
        st.session_state.selected_cols_2 = selected_cols_2

    # ------------------- Tab Navigation ------------------- #
    st.sidebar.markdown("---")
    tab = st.sidebar.radio("Navigate", ["Summary", "Insights", "Comparison", "Visualizations"], key="tab_selector")
    st.session_state.selected_tab = tab

    # ------------------- Reset Dev Button ------------------- #
    if st.sidebar.button("🔄 Reset All (Dev)", key="reset_all_btn"):
        st.session_state.clear()
        st.rerun()

    # ------------------- Debug Info ------------------- #
    with st.sidebar.expander("🛠 Debug Info"):
        st.write("df1_loaded:", st.session_state.get("df1_loaded"))
        st.write("df2_loaded:", st.session_state.get("df2_loaded"))
        st.write("selected_cols_1:", st.session_state.get("selected_cols_1"))
        st.write("selected_cols_2:", st.session_state.get("selected_cols_2"))
        st.write("file1_hash:", st.session_state.get("file1_hash"))
        st.write("file2_hash:", st.session_state.get("file2_hash"))

