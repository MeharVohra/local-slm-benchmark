# import streamlit as st
# import ollama
# import time
# import pandas as pd

# st.set_page_config(page_title="SLM Benchmark Dashboard", layout="wide")

# st.title("Local SLM Benchmark Dashboard")

# models = ["llama3", "mistral", "phi3"]

# prompt = st.text_area(
#     "Enter your prompt",
#     "Explain what an AI model is in simple words"
# )

# run_all = st.button("Run Benchmark on All Models")

# results = []

# if run_all:
#     st.info("Running models... please wait ⏳")

#     for model in models:
#         start = time.time()

#         response = ollama.chat(
#             model=model,
#             messages=[{"role": "user", "content": prompt}]
#         )

#         end = time.time()

#         output = response["message"]["content"]
#         duration = end - start

#         tokens = len(output.split())
#         tokens_per_sec = tokens / duration if duration > 0 else 0

#         results.append({
#             "model": model,
#             "time_sec": round(duration, 2),
#             "tokens_est": tokens,
#             "tokens_per_sec": round(tokens_per_sec, 2),
#             "output": output
#         })

#     df = pd.DataFrame(results)

#     st.subheader("📊 Benchmark Results")
#     st.dataframe(df[["model", "time_sec", "tokens_est", "tokens_per_sec"]])

#     st.subheader("⚡ Speed Comparison")

#     chart_df = df.set_index("model")[["tokens_per_sec"]]
#     st.bar_chart(chart_df)

#     st.subheader("⏱ Latency Comparison")

#     latency_df = df.set_index("model")[["time_sec"]]
#     st.bar_chart(latency_df)

#     st.subheader("💬 Model Outputs")

#     for row in results:
#         st.markdown(f"### 🤖 {row['model']}")
#         st.write(row["output"])
#         st.divider()

import streamlit as st
import ollama
import time
import pandas as pd
import plotly.express as px

# ---------------- UI SETUP ----------------
st.set_page_config(page_title="SLM Benchmark Dashboard", layout="wide")

st.title("Local SLM Benchmark Dashboard")
st.caption("Compare latency, throughput, and outputs of local LLMs running via Ollama")

# ---------------- MODELS ----------------
models = ["llama3", "mistral", "phi3"]

# ---------------- INPUT ----------------
prompt = st.text_area(
    "Enter your prompt",
    "Explain what an AI model is in simple words"
)

run_all = st.button("Run Benchmark on All Models")

# ---------------- RESULTS ----------------
results = []

if run_all:
    st.info("Running all models... please wait ⏳")

    for model in models:
        start = time.time()

        response = ollama.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )

        end = time.time()

        output = response["message"]["content"]
        duration = end - start

        tokens = len(output.split())  # simple token estimate
        tokens_per_sec = tokens / duration if duration > 0 else 0

        results.append({
            "model": model,
            "time_sec": round(duration, 2),
            "tokens_est": tokens,
            "tokens_per_sec": round(tokens_per_sec, 2),
            "output": output
        })

    df = pd.DataFrame(results)

    # ---------------- TABLE ----------------
    st.subheader("Benchmark Results Table")
    st.dataframe(df[["model", "time_sec", "tokens_est", "tokens_per_sec"]])

    # ---------------- CHART 1: SPEED ----------------
    st.subheader("⚡ Tokens per Second Comparison")

    fig1 = px.bar(
        df,
        x="model",
        y="tokens_per_sec",
        text="tokens_per_sec",
        color="model",
        title="Model Speed (Tokens/sec)"
    )
    st.plotly_chart(fig1, use_container_width=True)

    # ---------------- CHART 2: LATENCY ----------------
    st.subheader("⏱ Response Time Comparison")

    fig2 = px.bar(
        df,
        x="model",
        y="time_sec",
        text="time_sec",
        color="model",
        title="Model Latency (Seconds)"
    )
    st.plotly_chart(fig2, use_container_width=True)

    # ---------------- OUTPUTS ----------------
    st.subheader("💬 Model Outputs")

    for row in results:
        st.markdown(f"### 🤖 {row['model']}")
        st.write(row["output"])
        st.divider()