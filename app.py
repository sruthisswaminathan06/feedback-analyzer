import io
import streamlit as st
import pandas as pd
import requests
import database

API_URL = "http://127.0.0.1:8000/analyze"

st.set_page_config(page_title="Customer Feedback Analyzer", layout="wide")
st.title("📊 Customer Feedback Analyzer")

database.init_db()

if "results" not in st.session_state:
    st.session_state.results = []

st.subheader("1. Enter Feedback Reviews")
raw_reviews = st.text_area(
    "Paste customer reviews below (one review per line):",
    height=150,
    placeholder="The burgers were delicious and arrived very quickly!\nService was extremely slow and cold food."
)

if st.button("Analyze", type="primary"):
    lines = [line.strip() for line in raw_reviews.split("\n") if line.strip()]
    if not lines:
        st.warning("Please enter at least one review to analyze.")
    else:
        st.session_state.results = []
        progress_bar = st.progress(0)
        
        for idx, text in enumerate(lines):
            try:
                res = requests.post(API_URL, json={"text": text})
                if res.status_code == 200:
                    analysis = res.json()
                    st.session_state.results.append({
                        "review": text,
                        "label": analysis["label"],
                        "score": analysis["score"],
                        "theme": analysis["theme"]
                    })
                else:
                    st.error(f"Error on line {idx+1}: {res.json().get('detail', 'Unknown error')}")
            except Exception as e:
                st.error(f"Failed to connect to backend: {e}")
            
            progress_bar.progress((idx + 1) / len(lines))
        
        st.success("Analysis complete!")

if st.session_state.results:
    st.subheader("2. Analysis Results")
    df_results = pd.DataFrame(st.session_state.results)
    
    col1, col2, col3 = st.columns(3)
    total_reviews = len(df_results)
    avg_score = df_results["score"].mean()
    pos_count = (df_results["label"] == "positive").sum()
    pct_positive = (pos_count / total_reviews) * 100 if total_reviews > 0 else 0

    col1.metric("Total Reviews Analyzed", total_reviews)
    col2.metric("Average Rating Score", f"{avg_score:.2f} / 5")
    col3.metric("Positive Sentiment %", f"{pct_positive:.1f}%")

    st.dataframe(df_results, use_container_width=True)

    if st.button("Save Results to Database"):
        database.save_results(st.session_state.results)
        st.success("Results saved successfully to SQLite!")

st.markdown("---")

st.subheader("3. Saved History Database")

col_left, col_right = st.columns([1, 5])
with col_left:
    if st.button("Refresh History"):
        st.rerun()

history_data = database.load_history()
if history_data:
    df_history = pd.DataFrame(history_data)
    st.dataframe(df_history, use_container_width=True)

    # Convert DataFrame to Excel in memory
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
        df_history.to_excel(writer, index=False, sheet_name="Feedback History")
    excel_data = excel_buffer.getvalue()

    # Download button for Excel export
    st.download_button(
        label="📥 Download History as Excel (.xlsx)",
        data=excel_data,
        file_name="feedback_history.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        type="secondary"
    )
else:
    st.info("No saved history found in database.")