import streamlit as st
import ollama
import time
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="SLM Benchmark Dashboard", layout="wide")

st.title("SLM Benchmark Dashboard")
st.caption("Live comparison of local LLM performance using Ollama")

models = ["llama3", "mistral", "phi3"]

prompt = st.text_area(
    "Enter your prompt",
    "Explain what an AI model is in simple words"
)

run = st.button("🚀 Start Benchmark")

results = []

if run:

    st.info("Benchmark running... watch models execute in real time ⚡")

    global_progress = st.progress(0)
    status = st.empty()

    table_placeholder = st.empty()
    chart_placeholder = st.empty()
    output_placeholder = st.container()

    for i, model in enumerate(models):

        status.markdown(f"### 🤖 Running: `{model}`")

        model_progress = st.progress(0)

        start = time.time()

        # small animation feel
        for p in range(0, 80, 20):
            time.sleep(0.05)
            model_progress.progress(p)

        response = ollama.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )

        model_progress.progress(100)

        end = time.time()

        output = response["message"]["content"]
        duration = end - start

        tokens = len(output.split())
        tokens_per_sec = tokens / duration if duration > 0 else 0

        results.append({
            "model": model,
            "tokens": tokens,
            "time_sec": round(duration, 2),
            "tokens_per_sec": round(tokens_per_sec, 2),
            "output": output
        })

        # update global progress
        global_progress.progress((i + 1) / len(models))

        # ---------------- LIVE TABLE ----------------
        df = pd.DataFrame(results)

        table_placeholder.dataframe(
            df[["model", "tokens", "time_sec", "tokens_per_sec"]]
        )

        # ---------------- LIVE CHART ----------------
        fig = px.bar(
            df,
            x="model",
            y="tokens_per_sec",
            color="model",
            title="Live Tokens/sec Comparison"
        )
        chart_placeholder.plotly_chart(fig, use_container_width=True)

        status.success(f"{model} completed ✅")

    # ---------------- FINAL OUTPUT SECTION ----------------
    st.success("🎉 Benchmark completed!")

    st.subheader("📊 Final Results")
    st.dataframe(df)

    # ---------------- DOWNLOAD BUTTON ----------------
    csv = df.to_csv(index=False)

    st.download_button(
        label="Download Results as CSV",
        data=csv,
        file_name="slm_benchmark_results.csv",
        mime="text/csv"
    )

    # ---------------- MODEL OUTPUTS ----------------
    st.subheader("💬 Model Outputs")

    for row in results:
        with st.expander(f"{row['model']} output"):
            st.write(row["output"])

    st.subheader("📄 Download Report")

    md_report = "# SLM Benchmark Report\n\n"

    for row in results:
        md_report += f"""
        ## 🤖 {row['model']}

        - Tokens: {row['tokens']}
        - Time: {row['time_sec']} sec
        - Tokens/sec: {row['tokens_per_sec']}

        ### Output:
        {row['output']}

        ---
        """

    st.download_button(
        label="📥 Download Markdown Report",
        data=md_report,
        file_name="slm_benchmark_report.md",
        mime="text/markdown"
    )        