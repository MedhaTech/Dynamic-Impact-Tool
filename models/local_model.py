import subprocess

OLLAMA_PATH = "/usr/local/bin/ollama"  
MODEL_NAME = "gemma:2b"

def generate_response(prompt):
    try:
        process = subprocess.run(
            [OLLAMA_PATH, "run", MODEL_NAME],
            input=prompt,
            capture_output=True,
            text=True,
            check=True
        )
        return process.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"LLM Error: {e.stderr}"
    except FileNotFoundError:
        return "OLLAMA executable not found. Please check your path and installation."
