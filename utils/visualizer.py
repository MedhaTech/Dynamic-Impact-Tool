import plotly.express as px

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
