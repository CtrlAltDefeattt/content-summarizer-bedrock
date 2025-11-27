import streamlit as st
import tempfile
from summarization_lib import summarize_text, summarize_pdf, SummaryStyle

st.set_page_config(
    page_title="AI Content Summarizer (Bedrock + Claude)",
    layout="wide"
)

st.title("Dual-Interface Content Summarizer")
st.caption("Powered by AWS Bedrock + Claude via Converse API")

with st.sidebar:
    st.header("Configuration")

    style: SummaryStyle = st.selectbox(
        "Summary Style",
        options=["brief", "detailed", "bullet_points", "executive"],
        index=0
    )  # type: ignore

    input_mode = st.radio(
        "Input Type",
        options=["Text", "PDF Upload"]
    )

    user_hint = st.text_area(
        "Optional context / instructions",
        help="E.g., 'Focus on financial risks and KPIs' or 'Simplify for students.'",
        height=80
    )

st.markdown("### Input Content")

summary_result = None

if input_mode == "Text":
    raw_text = st.text_area(
        "Paste your content here",
        height=250,
        placeholder="Paste article, research report, notes, etc..."
    )

    if st.button("Summarize Text", type="primary"):
        if not raw_text.strip():
            st.warning("Please enter some text.")
        else:
            with st.spinner("Summarizing with Claude via Bedrock..."):
                summary_result = summarize_text(raw_text, style=style)

else:
    uploaded_file = st.file_uploader(
        "Upload a PDF document",
        type=["pdf"]
    )

    if st.button("Summarize PDF", type="primary"):
        if uploaded_file is None:
            st.warning("Please upload a PDF file.")
        else:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name

            with st.spinner("Summarizing PDF with Claude via Bedrock..."):
                summary_result = summarize_pdf(
                    tmp_path,
                    style=style,
                    user_hint=user_hint or None
                )

if summary_result:
    st.markdown("### Summary")
    if style == "bullet_points":
        # Ensure bullet formatting
        bullet_lines = [
            f"- {line.strip()}"
            for line in summary_result.split("\n")
            if line.strip()
        ]
        st.markdown("\n".join(bullet_lines))
    else:
        st.write(summary_result)
