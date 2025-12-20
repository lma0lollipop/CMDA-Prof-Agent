"""
app.py

Streamlit application for CMDAProfAgent.
Supports:
- Marks-based answer modes (5 / 8 / 15)
- Stable non-streaming Ollama calls
- PDF + classroom image reference
"""

import streamlit as st

from agent import generate_response
from pdf_utils import extract_text_from_pdf, build_pdf_context
from image_utils import extract_text_from_image, build_image_context
from ollama_client import query_ollama

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="CMDAProfAgent",
    page_icon="📘",
    layout="wide"
)

st.title("📘 CMDAProfAgent")
st.subheader("Exam-Oriented • Marks-Aware • Reliable Output")

# =========================
# SESSION STATE
# =========================

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "pdf_context" not in st.session_state:
    st.session_state.pdf_context = ""

if "pdf_uploaded" not in st.session_state:
    st.session_state.pdf_uploaded = False

# =========================
# SIDEBAR: UPLOADS
# =========================

st.sidebar.header("📂 Upload Reference Material")

uploaded_pdf = st.sidebar.file_uploader(
    "Upload PDF (Notes / Book / Scanned)",
    type=["pdf"]
)

if uploaded_pdf:
    pdf_text = extract_text_from_pdf(uploaded_pdf)
    st.session_state.pdf_context = build_pdf_context(pdf_text)
    st.session_state.pdf_uploaded = True
    st.sidebar.success("PDF uploaded and loaded as reference.")

uploaded_image = st.sidebar.file_uploader(
    "Upload Classroom Notes / Question Image",
    type=["png", "jpg", "jpeg"]
)

image_context = ""
if uploaded_image:
    image_text = extract_text_from_image(uploaded_image)
    image_context = build_image_context(image_text)
    st.sidebar.success("Image uploaded and OCR processed.")

# =========================
# MARKS MODE SELECTOR
# =========================

st.markdown("### 🎯 Select Answer Length (Marks Mode)")

marks_mode = st.selectbox(
    "Choose exam answer type:",
    ["Auto (Default)", "5 Marks", "8 Marks", "15 Marks"]
)

marks_instruction = ""
if marks_mode != "Auto (Default)":
    marks_instruction = f"Answer strictly as a {marks_mode} university examination question."

# =========================
# USER INPUT
# =========================

st.markdown("### 📝 Ask Your Question")

user_question = st.text_area(
    "Theory / Numerical / Follow-up question:",
    height=120
)

submit = st.button("📖 Get Answer")

# =========================
# RESPONSE HANDLING
# =========================

if submit:

    if not user_question.strip() and st.session_state.pdf_uploaded:
        user_question = "Explain the uploaded material in detail."

    combined_context = ""

    if st.session_state.pdf_uploaded:
        combined_context += st.session_state.pdf_context

    if image_context:
        combined_context += image_context

    # Inject marks instruction into question
    final_question = user_question
    if marks_instruction:
        final_question = f"{marks_instruction}\n\n{user_question}"

    response_payload = generate_response(
        question=final_question,
        context=combined_context
    )

    with st.spinner("CMDAProfAgent is generating the answer..."):
        answer = query_ollama(
            system_prompt=response_payload["system_prompt"],
            user_prompt=response_payload["user_prompt"]
        )

    st.session_state.chat_history.append({
        "question": user_question,
        "answer": answer,
        "marks_mode": marks_mode
    })

# =========================
# DISPLAY CHAT HISTORY
# =========================

if st.session_state.chat_history:
    st.markdown("## 📚 Conversation")

    for i, chat in enumerate(st.session_state.chat_history):
        st.markdown(f"### ❓ Question {i+1}")
        st.write(chat["question"])

        if chat.get("marks_mode") and chat["marks_mode"] != "Auto (Default)":
            st.markdown(f"**Marks Mode:** {chat['marks_mode']}")

        st.markdown("### 📘 Answer")
        st.write(chat["answer"])
        st.markdown("---")
