import streamlit as st

from agent import generate_response
from pdf_utils import extract_text_from_pdf, build_pdf_context
from image_utils import extract_text_from_image
from groq_client import query_llm


# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="CMDAProfAgent",
    page_icon="📘",
    layout="wide"
)

st.title("📘 CMDAProfAgent")
st.caption("AI Professor for Computational Methods and Data Analysis (CMDA)")


# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------
if "conversation" not in st.session_state:
    st.session_state.conversation = []


# -------------------------------------------------
# SIDEBAR: FILE UPLOADS
# -------------------------------------------------
st.sidebar.header("📂 Upload Reference Material")

uploaded_pdf = st.sidebar.file_uploader(
    "Upload PDF (Lecture notes / Question paper)",
    type=["pdf"]
)

uploaded_image = st.sidebar.file_uploader(
    "Upload Image (Classroom notes / Numerical questions)",
    type=["png", "jpg", "jpeg"]
)


# -------------------------------------------------
# EXTRACT CONTEXT
# -------------------------------------------------
context = ""

if uploaded_pdf:
    with st.sidebar.spinner("Reading PDF..."):
        pdf_text = extract_text_from_pdf(uploaded_pdf)
        context = build_pdf_context(pdf_text)

if uploaded_image:
    with st.sidebar.spinner("Reading Image..."):
        image_text = extract_text_from_image(uploaded_image)
        context += "\n\nIMAGE CONTENT START\n" + image_text + "\nIMAGE CONTENT END"


# -------------------------------------------------
# USER INPUT
# -------------------------------------------------
st.subheader("📚 Ask a CMDA Question")

user_question = st.text_area(
    "Enter your question (mention marks if needed, e.g., 5 marks / 8 marks / 15 marks):",
    height=120
)

submit = st.button("🧠 Generate Answer")


# -------------------------------------------------
# RESPONSE GENERATION
# -------------------------------------------------
if submit and user_question.strip():

    with st.spinner("CMDAProfAgent is thinking..."):
        prompts = generate_response(user_question, context)

        answer = query_llm(
            prompts["system_prompt"],
            prompts["user_prompt"]
        )

    st.session_state.conversation.append({
        "question": user_question,
        "answer": answer
    })


# -------------------------------------------------
# DISPLAY CONVERSATION
# -------------------------------------------------
st.divider()
st.subheader("📖 Conversation")

for i, turn in enumerate(st.session_state.conversation, start=1):
    st.markdown(f"### ❓ Question {i}")
    st.markdown(turn["question"])

    st.markdown("### 📘 Answer")
    st.markdown(turn["answer"])
