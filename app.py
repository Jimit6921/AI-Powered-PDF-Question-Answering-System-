import streamlit as st
from utils import extract_pages_from_pdf
from agent import ask_document

st.set_page_config(
    page_title="AI PDF Q&A Agent",
    page_icon="📄",
    layout="centered"
)

st.title("📄 AI-Powered PDF Question Answering System")
st.caption("Upload a PDF and ask questions based on its content.")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

uploaded_file = st.file_uploader("Upload PDF Document", type=["pdf"])

if uploaded_file:
    with st.spinner("Extracting text from PDF..."):
        pages = extract_pages_from_pdf(uploaded_file)

    total_text = " ".join([page["text"] for page in pages]).strip()

    if not total_text:
        st.error("No readable text found in this PDF.")
    else:
        st.success(f"Document loaded successfully! Total pages: {len(pages)}")

        question = st.text_input("Ask a question from the PDF:")

        if st.button("Get Answer") and question:
            with st.spinner("Generating answer..."):
                answer, source_pages = ask_document(pages, question)

            st.session_state.chat_history.append({
                "question": question,
                "answer": answer,
                "source_pages": source_pages
            })

        if st.session_state.chat_history:
            st.subheader("Chat History")

            for chat in reversed(st.session_state.chat_history):
                st.markdown(f"**Question:** {chat['question']}")
                st.markdown(f"**Answer:** {chat['answer']}")
                st.caption(f"Source page(s): {', '.join(map(str, chat['source_pages']))}")
                st.divider()

        if st.button("Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()
else:
    st.info("Please upload a PDF document to start.")
