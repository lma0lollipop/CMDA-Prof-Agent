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
# CONSTANTS (GROQ SAFETY LIMITS)
# -------------------------------------------------
MAX_CONTEXT_CHARS = 6000     # Prevent Groq BadRequest
MAX_DISPLAY_CHARS = 12000   # UI safety


# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------
if "conversation" not in st.session_state:
    st.session_state.conversation = []


# -------------------------------------------------
# SIDEBAR: FILE UPLOADS (UI ONLY)
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
# EXTRACT CONTEXT (PROCESSING IN MAIN AREA ONLY)
# -------------------------------------------------
context = ""

if uploaded_pdf:
    with st.spinner("📄 Reading PDF..."):
        try:
            pdf_text = extract_text_from_pdf(uploaded_pdf)
            context = build_pdf_context(pdf_text)
        except Exception as e:
            context += f"\nPDF READ ERROR: {e}"

if uploaded_image:
    with st.spinner("🖼 Reading image..."):
        try:
            image_text = extract_text_from_image(uploaded_image)
            context += "\n\nIMAGE CONTENT START\n"
            context += image_text
            context += "\nIMAGE CONTENT END"
        except Exception as e:
            context += f"\nIMAGE OCR ERROR: {e}"

# HARD LIMIT CONTEXT SIZE (CRITICAL FOR GROQ)
if len(context) > MAX_CONTEXT_CHARS:
    context = context[:MAX_CONTEXT_CHARS]


# -------------------------------------------------
# USER INPUT
# -------------------------------------------------
st.subheader("📚 Ask a CMDA Question")

user_question = st.text_area(
    "Enter your question (mention marks if needed: 5 / 8 / 15 marks):",
    height=120
)

submit = st.button("🧠 Generate Answer")


# -------------------------------------------------
# RESPONSE GENERATION
# -------------------------------------------------
if submit and user_question.strip():

    with st.spinner("CMDAProfAgent is generating an exam-ready answer..."):
        prompts = generate_response(user_question, context)

        answer = query_llm(
            prompts["system_prompt"],
            prompts["user_prompt"]
        )

    # Safety limit for UI rendering
    if len(answer) > MAX_DISPLAY_CHARS:
        answer = answer[:MAX_DISPLAY_CHARS] + "\n\n⚠️ Output truncated for display."

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