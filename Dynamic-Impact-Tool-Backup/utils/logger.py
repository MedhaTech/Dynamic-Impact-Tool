# utils/logger.py

import os
import datetime
import logging

# ----- Logging Setup -----
logger = logging.getLogger("dynamic_impact_tool")
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# ----- Text Log Writers -----
def save_text_log(log_text, log_dir="logs", prefix="log"):
    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_path = os.path.join(log_dir, f"{timestamp}_{prefix}.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(log_text)
    return file_path

def save_chat_log(chat_text):
    return save_text_log(chat_text, log_dir="chat_logs", prefix="chat")

def save_insight_log(insight_text):
    return save_text_log(insight_text, log_dir="insight_logs", prefix="insights")

def save_comparison_log(comp_text):
    return save_text_log(comp_text, log_dir="comparison_logs", prefix="comparison")
