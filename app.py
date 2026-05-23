import streamlit as st
import ollama
import time

st.title("Local SLM Benchmark Dashboard")

models = ["llama3", "mistral", "phi3"]

model = st.selectbox("Choose Model", models)

prompt = st.text_area("Enter your prompt", "Explain what an AI model is in simple words")

if st.button("Run Model"):
    start = time.time()

    response = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )

    end = time.time()

    output = response["message"]["content"]
    duration = end - start

    st.subheader("Response")
    st.write(output)

    st.subheader("Metrics")
    st.write(f"Time taken: {duration:.2f} seconds")