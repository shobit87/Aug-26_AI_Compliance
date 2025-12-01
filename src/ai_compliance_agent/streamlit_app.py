"""Streamlit UI to run the AI compliance workflow."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path
from typing import Optional

import html

import streamlit as st
from ai_compliance_agent.state import ensure_defaults
from ai_compliance_agent.workflow import build_workflow_app

workflow_app = build_workflow_app()

CARD_STYLES = """
<style>
.stApp {
    background-color: #f7f9fc;
}
.block-container {
    padding-top: 1rem;
}
.hero {
    padding: 1.5rem;
    border-radius: 16px;
    background: linear-gradient(135deg, #1f3b83, #4e8fde);
    color: #fff;
}
.hero h1 {
    margin-bottom: 0.5rem;
}
.info-card {
    border: 1px solid #e4e8f1;
    border-radius: 12px;
    padding: 1rem 1.25rem;
    background-color: #fff;
    box-shadow: 0 5px 18px rgba(31, 59, 131, 0.08);
    margin-bottom: 1rem;
}
.info-card h4 {
    margin-bottom: 0.25rem;
}
.doc-block {
    white-space: pre-wrap;
    font-family: "Segoe UI", "Inter", sans-serif;
    line-height: 1.5;
    padding: 1rem 1.2rem;
    background-color: #ffffff;
    border-radius: 12px;
    border: 1px solid #e4e8f1;
    box-shadow: inset 0 1px 2px rgba(16, 24, 40, 0.04);
    width: 100%;
}
</style>
"""


def _persist_upload(upload) -> Optional[str]:
    if not upload:
        return None
    suffix = Path(upload.name or "").suffix or ".txt"
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    temp.write(upload.getvalue())
    temp.flush()
    temp.close()
    return temp.name


def _cleanup(path: Optional[str]) -> None:
    if path and os.path.exists(path):
        os.unlink(path)


def _render_results(result: dict) -> None:
    ensure_defaults(result)
    recommendations = result.get("document_recommendations", [])
    gaps = result.get("compliance_gaps", [])
    corrected = result.get("corrected_document")
    artifacts = result.get("artifacts", [])

    st.markdown("### Analysis Summary")
    metric_cols = st.columns(4)
    metric_cols[0].metric("Recommendations", len(recommendations))
    metric_cols[1].metric("Compliance Gaps", len(gaps))
    metric_cols[2].metric("Document Tone", result.get("document_tone") or "N/A")
    grammar_value = result.get("grammar_score")
    metric_cols[3].metric(
        "Grammar Score",
        f"{grammar_value:.2f}" if grammar_value is not None else "N/A",
    )

    main_col, sidebar_col = st.columns((2.2, 1))

    with main_col:
        template_cols = st.columns(2)
        original_text = result.get("document_text") or "No uploaded document."
        original_name = result.get("original_document_name") or "uploaded_document"
        original_bytes = result.get("original_document_bytes")
        with template_cols[0]:
            st.markdown("##### Original Template")
            st.markdown(
                f'<div class="doc-block">{html.escape(original_text)}</div>',
                unsafe_allow_html=True,
            )
            if original_bytes:
                st.download_button(
                    "Download original file",
                    data=original_bytes,
                    file_name=original_name,
                    use_container_width=True,
                )
            else:
                st.caption("No original file uploaded.")

        with template_cols[1]:
            st.markdown("##### AI Corrected Template")
            if corrected:
                st.markdown(
                    f'<div class="doc-block">{html.escape(corrected)}</div>',
                    unsafe_allow_html=True,
                )
                st.download_button(
                    "Download corrected draft",
                    corrected,
                    file_name="corrected_document.txt",
                    use_container_width=True,
                )
            else:
                st.info("No corrections were required for this document.")

        st.markdown("#### Generated Documentation")
        doc_text = result.get("documentation") or "No documentation produced."
        st.markdown(
            f'<div class="doc-block">{html.escape(doc_text)}</div>',
            unsafe_allow_html=True,
        )
        if doc_path := result.get("document_path"):
            st.caption(f"Document reviewed: {doc_path}")

    with sidebar_col:
        st.markdown("#### Reviewer Insights")
        if recommendations:
            for rec in recommendations:
                st.markdown(f"- {rec}")
        else:
            st.success("No document gaps identified.")

        st.markdown("#### Compliance Gaps")
        if gaps:
            for gap in gaps:
                st.write(f"- {gap}")
        else:
            st.write("No outstanding gaps.")

        st.markdown("#### Workflow History")
        history = result.get("history", [])
        if history:
            for entry in history:
                st.write(f"- {entry}")
        else:
            st.write("History not available.")


def main():
    st.set_page_config(page_title="AI Compliance Agent", layout="wide")
    st.markdown(CARD_STYLES, unsafe_allow_html=True)

    with st.container():
        st.markdown(
            """
            <div class="hero">
                <h1>AI Compliance Agent</h1>
                <p>Upload change-management artifacts and receive instant gap analysis, reviewer notes, and AI-corrected drafts.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    input_col, info_col = st.columns([2, 1])
    with input_col:
        st.markdown("### Submit a Request")
        with st.form("compliance-form", clear_on_submit=False):
            request_text = st.text_area(
                "Compliance Request",
                value="Review SOC2 change policy",
                help="Describe what you want the agent workflow to analyze or produce.",
            )
            uploaded_file = st.file_uploader(
                "Policy Document (PDF, DOCX, or text)",
                type=["pdf", "docx", "txt", "md"],
            )
            submitted = st.form_submit_button(
                "Run Analysis",
                type="primary",
                use_container_width=True,
            )
    with info_col:
        st.markdown("### Tips")
        st.markdown(
            """
            <div class="info-card">
                <h4>Best results</h4>
                <ul>
                    <li>Upload final or near-final drafts.</li>
                    <li>Include scope keywords (SOC2, GDPR, HIPAA).</li>
                    <li>Summaries under 50 lines may trigger recommendations for more detail.</li>
                </ul>
            </div>
            <div class="info-card">
                <h4>Outputs</h4>
                <p>Documentation summary, reviewer findings, corrected draft, and audit history.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    result_container = st.container()

    if submitted:
        if not request_text.strip():
            st.error("Please provide a compliance request.")
            return

        temp_path = _persist_upload(uploaded_file)
        state = {"request": request_text, "document_path": temp_path}
        with st.spinner("Running workflow..."):
            result = workflow_app.invoke(state)
        _cleanup(temp_path)
        with result_container:
            _render_results(result)


if __name__ == "__main__":
    main()
