from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL_NAME = "llama-3.1-8b-instant"


def build_context(pages, question, max_chars=6000):
    """
    Select relevant page text instead of sending the whole PDF.
    Simple keyword matching is used so the project stays easy to explain in interview.
    """
    question_words = set(question.lower().split())
    scored_pages = []

    for page in pages:
        text = page["text"]
        text_words = set(text.lower().split())
        score = len(question_words.intersection(text_words))
        scored_pages.append((score, page))

    scored_pages.sort(key=lambda x: x[0], reverse=True)

    selected_context = ""
    selected_pages = []

    for score, page in scored_pages:
        if score == 0 and selected_context:
            continue

        page_text = f"\n\n[Page {page['page_number']}]\n{page['text']}"
        if len(selected_context) + len(page_text) > max_chars:
            break

        selected_context += page_text
        selected_pages.append(page["page_number"])

    if not selected_context:
        selected_context = "\n\n".join(
            [f"[Page {p['page_number']}]\n{p['text']}" for p in pages[:2]]
        )
        selected_pages = [p["page_number"] for p in pages[:2]]

    return selected_context, selected_pages


def ask_document(pages, user_question):
    context, source_pages = build_context(pages, user_question)

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": """
You are an AI-powered PDF document question-answering assistant.

Rules:
1. Answer ONLY from the provided document context.
2. If the answer is not available in the document, say: "Answer not found in the document."
3. Keep the answer clear, short, and professional.
4. Mention the source page number when possible.
"""
            },
            {
                "role": "user",
                "content": f"""
Document Context:
{context}

Question:
{user_question}
"""
            }
        ],
        temperature=0.2
    )

    answer = response.choices[0].message.content
    return answer, source_pages
