import ollama
import time
import psutil
import pandas as pd

models = ["llama3", "mistral", "phi3"]

prompt = "Explain what an AI model is in simple words"

results = []

for model in models:
    print(f"\nRunning model: {model}")

    # CPU + RAM before
    process = psutil.Process()
    mem_before = process.memory_info().rss / (1024 * 1024)

    start = time.time()
    print("Getting response from the model ...")
    response = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )

    end = time.time()

    mem_after = process.memory_info().rss / (1024 * 1024)

    output = response["message"]["content"]

    # time taken
    duration = end - start

    # crude token estimate (simple approximation)
    tokens = len(output.split())
    tokens_per_sec = tokens / duration if duration > 0 else 0

    results.append({
        "model": model,
        "time_sec": duration,
        "tokens_est": tokens,
        "tokens_per_sec": tokens_per_sec,
        "ram_before_mb": mem_before,
        "ram_after_mb": mem_after,
        "output_preview": output[:100]
    })

print("Results appended.")
# converts the list of results into a table

df = pd.DataFrame(results)
print("\n=== BENCHMARK RESULTS ===\n")
print(df)

df.to_csv("results.csv", index=False)