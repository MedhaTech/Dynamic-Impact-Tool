# import streamlit as st

# def init_session_state():
#     defaults = {
#         # Dataset objects
#         "df1": None,
#         "df2": None,
#         "df1_cols": [],
#         "df2_cols": [],
#         "selected_cols_1": [],
#         "selected_cols_2": [],

#         # Tab selector
#         "selected_tab": "Summary",

#         # Summary / Insights output
#         "summary_output_1": "",
#         "summary_output_2": "",
#         "insight_output_1": "",
#         "insight_output_2": "",

#         # Insight categories & results
#         "insight_categories_1": [],
#         "insight_categories_2": [],
#         "selected_category_1": None,
#         "selected_category_2": None,
#         "category_insights_1": {},
#         "category_insights_2": {},

#         # Visualizations / final outputs
#         "visual_output_1": [],
#         "visual_output_2": [],

#         # Comparison
#         "comparison_result": "",
#         "comparison_visual": None
#     }

#     for key, value in defaults.items():
#         if key not in st.session_state:
#             st.session_state[key] = value

# def reset_dataset_a_state():
#     for key in [
#         "df1", "df1_cols", "selected_cols_1",
#         "summary_output_1", "insight_output_1",
#         "insight_categories_1", "selected_category_1",
#         "category_insights_1", "visual_output_1"
#     ]:
#         if key in st.session_state:
#             st.session_state[key] = None if "df" in key else ""


# def reset_dataset_b_state():
#     for key in [
#         "df2", "df2_cols", "selected_cols_2",
#         "summary_output_2", "insight_output_2",
#         "insight_categories_2", "selected_category_2",
#         "category_insights_2", "visual_output_2"
#     ]:
#         if key in st.session_state:
#             st.session_state[key] = None if "df" in key else ""

import streamlit as st

def init_session_state():
    defaults = {
        # Dataset A
        "df1": None,
        "df1_cols": [],
        "selected_cols_1": [],
        "df1_loaded": False,

        # Dataset B
        "df2": None,
        "df2_cols": [],
        "selected_cols_2": [],
        "df2_loaded": False,

        # Summary
        "summary_output_1": "",
        "summary_output_2": "",

        # Insights
        "insight_output_1": "",
        "insight_output_2": "",
        "insight_categories_1": [],
        "insight_categories_2": [],
        "selected_category_1": None,
        "selected_category_2": None,
        "category_insights_1": {},
        "category_insights_2": {},

        # Comparison
        "comparison_result": "",
        "comparison_visual": None,

        # UI
        "selected_tab": "Summary",

        "file1_hash": None,
        "file2_hash": None
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def reset_dataset_a_state():
    for key in [
        "df1", "df1_cols", "selected_cols_1", "summary_output_1",
        "insight_output_1", "insight_categories_1", "selected_category_1",
        "category_insights_1", "visual_output_1", "df1_loaded"
    ]:
        st.session_state[key] = {} if "category" in key else None if "df" in key else "" if "output" in key else False
    st.session_state["file1_hash"] = None


def reset_dataset_b_state():
    for key in [
        "df2", "df2_cols", "selected_cols_2", "summary_output_2",
        "insight_output_2", "insight_categories_2", "selected_category_2",
        "category_insights_2", "visual_output_2", "df2_loaded"
    ]:
        st.session_state[key] = {} if "category" in key else None if "df" in key else "" if "output" in key else False
    st.session_state["file2_hash"] = None

