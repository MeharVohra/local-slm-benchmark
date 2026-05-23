import ollama

response = ollama.chat(
    model='llama3',
    messages=[
        {'role': 'user', 'content': 'Explain what an AI model is in simple words'}
    ]
)

print(response['message']['content'])