
from typing import TypedDict, Optional, List, Union
import pandas as pd

class AppState(TypedDict, total=False):
    df: Optional[pd.DataFrame]
    df1: Optional[pd.DataFrame]
    df2: Optional[pd.DataFrame]
    selected_category: Optional[str]
    model_source: Optional[str]
    chat_prompt: Optional[str]
    chat_response: Optional[Union[str, dict]]
    chat_history: List[dict]
    compare_chat: List[dict]
    insights: Optional[dict]
    follow_ups: Optional[List[str]]
    visualization: Optional[dict]
    memory: Optional[dict]