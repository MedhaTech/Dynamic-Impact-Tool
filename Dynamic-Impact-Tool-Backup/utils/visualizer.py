
# import plotly.express as px
# import plotly.graph_objects as go
# import pandas as pd

# def visualize_from_llm_response(df, query, llm_response):
#     try:
#         chart_type = llm_response.get("chart_type", "").lower()
#         group_by = llm_response.get("group_by", [])
#         title = llm_response.get("title", f"{chart_type.title()} Chart")

#         if chart_type == "correlation_heatmap":
#             corr = df.select_dtypes(include='number').corr()
#             fig = px.imshow(corr, text_auto=True, title="Correlation Heatmap")
#             return fig, "Heatmap of correlation between numerical columns."

#         if not group_by or not isinstance(group_by, list) or len(group_by) < 1:
#             return None, "Invalid `group_by` in model response."

#         x = group_by[0]
#         y = group_by[1] if len(group_by) > 1 else None

#         if x not in df.columns or (y and y not in df.columns):
#             return None, "Requested columns not found in dataset."

#         if chart_type == "bar":
#             fig = px.bar(df, x=x, y=y, title=title)
#         elif chart_type == "line":
#             fig = px.line(df, x=x, y=y, title=title)
#         elif chart_type == "scatter":
#             fig = px.scatter(df, x=x, y=y, title=title)
#         elif chart_type == "box":
#             fig = px.box(df, x=x, y=y, title=title)
#         elif chart_type == "histogram":
#             fig = px.histogram(df, x=x, title=title)
#         elif chart_type == "pie":
#             fig = px.pie(df, names=x, values=y if y else None, title=title)
#         elif chart_type == "violin":
#             fig = px.violin(df, x=x, y=y, box=True, points="all", title=title)
#         elif chart_type == "area":
#             fig = px.area(df, x=x, y=y, title=title)
#         else:
#             return None, f"Unsupported chart type: `{chart_type}`."

#         return fig, f"**{chart_type.title()} Chart** showing `{y}` by `{x}`."

#     except Exception as e:
#         print(f"Visualization error: {e}")
#         return None, "Error generating visualization."


# def visualize_comparison_side_by_side(df1, df2, x, y, chart_type="bar"):
#     try:
#         fig1, fig2 = None, None
#         if chart_type == "bar":
#             fig1 = px.bar(df1, x=x, y=y, title="Dataset 1")
#             fig2 = px.bar(df2, x=x, y=y, title="Dataset 2")
#         elif chart_type == "line":
#             fig1 = px.line(df1, x=x, y=y, title="Dataset 1")
#             fig2 = px.line(df2, x=x, y=y, title="Dataset 2")
#         elif chart_type == "scatter":
#             fig1 = px.scatter(df1, x=x, y=y, title="Dataset 1")
#             fig2 = px.scatter(df2, x=x, y=y, title="Dataset 2")
#         return fig1, fig2
#     except Exception as e:
#         print(f"Side-by-side visualization error: {e}")
#         return None, None


# def visualize_comparison_overlay(df1, df2, x, y, label1="Dataset 1", label2="Dataset 2", chart_type="line"):
#     try:
#         fig = go.Figure()
#         explanation = f"### Comparison Summary\n- **X-Axis:** {x}\n- **Y-Axis:** {y}\n\n"

#         if chart_type == "line":
#             fig.add_trace(go.Scatter(x=df1[x], y=df1[y], mode='lines+markers', name=label1))
#             fig.add_trace(go.Scatter(x=df2[x], y=df2[y], mode='lines+markers', name=label2))
#             explanation += "- A line chart helps visualize trends and differences over time or ordered categories.\n"
#         elif chart_type == "bar":
#             fig.add_trace(go.Bar(x=df1[x], y=df1[y], name=label1))
#             fig.add_trace(go.Bar(x=df2[x], y=df2[y], name=label2))
#             explanation += "- Bar charts are ideal for visualizing absolute differences between categories.\n"
#         elif chart_type == "scatter":
#             fig.add_trace(go.Scatter(x=df1[x], y=df1[y], mode='markers', name=label1))
#             fig.add_trace(go.Scatter(x=df2[x], y=df2[y], mode='markers', name=label2))
#             explanation += "- Scatter plots show correlation and distribution between two numeric fields across datasets.\n"

#         fig.update_layout(title=f"Overlay Comparison of {y} by {x}", barmode="group")
#         return fig, explanation
#     except Exception as e:
#         print(f"Overlay comparison error: {e}")
#         return None, "Error generating explanation."

# Updated visualize.py (Visualizer Logic + Summary)

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils.groq_handler import call_groq_model
from utils.ollama_handler import call_ollama_model
from utils.logger import logger

def render_chart(df, chart_type, x, y=None):
    if chart_type == "bar":
        return px.bar(df, x=x, y=y)
    elif chart_type == "line":
        return px.line(df, x=x, y=y)
    elif chart_type == "scatter":
        return px.scatter(df, x=x, y=y)
    elif chart_type == "histogram":
        return px.histogram(df, x=x)
    elif chart_type == "pie":
        return px.pie(df, names=x, values=y) if y else px.pie(df, names=x)
    else:
        raise ValueError(f"Unsupported chart type: {chart_type}")
def visualize_from_llm_response(df, query, llm_response, model_source="groq"):
    try:
        chart_type = llm_response.get("chart_type", "").lower()
        title = llm_response.get("title", f"{chart_type.title()} Chart")
        animation_col = llm_response.get("animation_frame")

        # Extract X and Y
        group_by = llm_response.get("group_by")
        x = llm_response.get("x")
        y = llm_response.get("y")

        # Fallback to group_by if x/y not provided
        if not x and group_by and isinstance(group_by, list) and len(group_by) >= 1:
            x = group_by[0]
            if len(group_by) > 1:
                y = group_by[1]

        if chart_type == "correlation_heatmap":
            corr = df.select_dtypes(include='number').corr()
            fig = px.imshow(corr, text_auto=True, title="Correlation Heatmap")
            summary = "Correlation heatmap shows pairwise correlation among numerical columns."
            return fig, summary

        if not x or x not in df.columns:
            return None, f"X-axis '{x}' not found in dataset."
        if y and y not in df.columns:
            return None, f"Y-axis '{y}' not found in dataset."

        # === Chart rendering ===
        fig = None
        if chart_type == "bar":
            fig = px.bar(df, x=x, y=y, title=title, animation_frame=animation_col)
        elif chart_type == "line":
            fig = px.line(df, x=x, y=y, title=title, animation_frame=animation_col)
        elif chart_type == "scatter":
            fig = px.scatter(df, x=x, y=y, title=title)
        elif chart_type == "box":
            fig = px.box(df, x=x, y=y, title=title)
        elif chart_type == "histogram":
            fig = px.histogram(df, x=x, title=title)
        elif chart_type == "pie":
            fig = px.pie(df, names=x, values=y if y else None, title=title)
        elif chart_type == "violin":
            fig = px.violin(df, x=x, y=y, box=True, points="all", title=title)
        elif chart_type == "area":
            fig = px.area(df, x=x, y=y, title=title)
        else:
            return None, f"Unsupported chart type: `{chart_type}`."

        # === Generate Summary ===
        if x and y:
            sample = df[[x, y]].dropna().head(50)
        else:
            sample = df[[x]].dropna().head(50)

        summary = summarize_chart(sample, chart_type, x, y, model_source)
        return fig, summary

    except Exception as e:
        logger.error(f"Visualization error: {e}")
        return None, "Error generating visualization."

def summarize_chart(sample_df, chart_type, x, y, model_source):
    system_prompt = """
You are a senior data analyst.
Given the chart type and a preview of the data (x and y), explain in 2-3 sentences what the chart reveals.
Do not describe the chart type — explain the **insight** behind it.
    """
    user_prompt = f"""
Chart type: {chart_type}
X-axis: {x}
Y-axis: {y}
Data Preview: {sample_df.to_dict(orient='records')[:5]}
"""

    try:
        if model_source == "groq":
            return call_groq_model(system_prompt, user_prompt)
        else:
            return call_ollama_model(system_prompt, user_prompt)
    except Exception as e:
        logger.warning(f"Chart summary generation failed: {e}")
        return "No summary available."

# ========== Comparison Chart Helpers ==========

def visualize_comparison_overlay(df1, df2, x, y, label1="Dataset 1", label2="Dataset 2", chart_type="line"):
    try:
        fig = go.Figure()

        if chart_type == "line":
            fig.add_trace(go.Scatter(x=df1[x], y=df1[y], mode='lines+markers', name=label1))
            fig.add_trace(go.Scatter(x=df2[x], y=df2[y], mode='lines+markers', name=label2))
        elif chart_type == "bar":
            fig.add_trace(go.Bar(x=df1[x], y=df1[y], name=label1))
            fig.add_trace(go.Bar(x=df2[x], y=df2[y], name=label2))
        elif chart_type == "scatter":
            fig.add_trace(go.Scatter(x=df1[x], y=df1[y], mode='markers', name=label1))
            fig.add_trace(go.Scatter(x=df2[x], y=df2[y], mode='markers', name=label2))
        else:
            return None, f"Chart type '{chart_type}' not supported for overlay visualization."

        fig.update_layout(title=f"Overlay Comparison of {y} by {x}", barmode="group")
        return fig, f"### Comparison Summary\n- **X-Axis:** {x}\n- **Y-Axis:** {y}\n- **Type:** {chart_type.title()}"
    except Exception as e:
        return None, f"Error generating comparison: {e}"

def visualize_comparison_side_by_side(df1, df2, x, y=None, chart_type="bar"):
    try:
        fig1, fig2 = None, None

        if chart_type == "bar":
            fig1 = px.bar(df1, x=x, y=y, title="Dataset 1")
            fig2 = px.bar(df2, x=x, y=y, title="Dataset 2")
        elif chart_type == "line":
            fig1 = px.line(df1, x=x, y=y, title="Dataset 1")
            fig2 = px.line(df2, x=x, y=y, title="Dataset 2")
        elif chart_type == "scatter":
            fig1 = px.scatter(df1, x=x, y=y, title="Dataset 1")
            fig2 = px.scatter(df2, x=x, y=y, title="Dataset 2")
        elif chart_type == "box":
            fig1 = px.box(df1, x=x, y=y, title="Dataset 1")
            fig2 = px.box(df2, x=x, y=y, title="Dataset 2")
        elif chart_type == "histogram":
            fig1 = px.histogram(df1, x=x, title="Dataset 1")
            fig2 = px.histogram(df2, x=x, title="Dataset 2")
        elif chart_type == "pie":
            fig1 = px.pie(df1, names=x, values=y, title="Dataset 1")
            fig2 = px.pie(df2, names=x, values=y, title="Dataset 2")
        elif chart_type == "violin":
            fig1 = px.violin(df1, x=x, y=y, box=True, points="all", title="Dataset 1")
            fig2 = px.violin(df2, x=x, y=y, box=True, points="all", title="Dataset 2")
        elif chart_type == "area":
            fig1 = px.area(df1, x=x, y=y, title="Dataset 1")
            fig2 = px.area(df2, x=x, y=y, title="Dataset 2")
        elif chart_type == "correlation_heatmap":
            corr1 = df1.select_dtypes(include='number').corr()
            corr2 = df2.select_dtypes(include='number').corr()
            fig1 = px.imshow(corr1, text_auto=True, title="Correlation Heatmap - Dataset 1")
            fig2 = px.imshow(corr2, text_auto=True, title="Correlation Heatmap - Dataset 2")
        else:
            return None, None

        return fig1, fig2
    except Exception as e:
        return None, None
