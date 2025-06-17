import ollama

def query_ollama(prompt):
    response = ollama.chat(
        model="gemma:2b",  
        messages=[
            {"role": "system", "content": "You are a senior data scientist."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['message']['content'].strip()
