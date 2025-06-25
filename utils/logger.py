import logging
import os

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

logger = logging.getLogger("GenAI-Logger")
logger.setLevel(logging.INFO)

formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s')

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

file_handler = logging.FileHandler(f"{log_dir}/app.log", mode='a')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

if not logger.hasHandlers():
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
