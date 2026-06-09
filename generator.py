from groq import Groq

from config import GROQ_API_KEY, GROQ_MODEL

_client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """You are a knowledgeable assistant for the game Travian: Legends.

Answer the user's question strictly using the context chunks provided in the user message. 
Do not use your training data or any outside knowledge under any circumstances.

For every factual point in your response, annotate it with its source document in this format:
(Official: <source>) or (Unofficial: <source>). Strip the .md extension from the source name.
If the answer is fully contained within one document, cite only that document. Only expand citations
to multiple sources when the answer genuinely spans across documents.

If the provided context chunks do not contain information relevant to the question, 
say that the available guides don't cover that topic and ask the user to rephrase or 
ask something more specific about Travian: Legends.
"""

NO_CONTEXT_RESPONSE = (
    "I don't have enough information in my knowledge base to answer that question. "
    "Could you try rephrasing it or ask something more specific about Travian: Legends?"
)


def generate_response(query: str, retrieved_chunks: list[dict]) -> str:
    """Assemble a grounded prompt from retrieved chunks and call Groq to generate a response."""
    if not retrieved_chunks:
        return NO_CONTEXT_RESPONSE

    context_parts = []
    for chunk in retrieved_chunks:
        source = chunk["metadata"]["source"]
        doc_type = chunk["metadata"]["type"]
        distance = chunk["distance"]
        context_parts.append(
            f"(source: {source}, type: {doc_type}, distance: {distance:.4f}) - {chunk['text']}"
        )
    context = "\n\n---\n\n".join(context_parts)

    user_message = f"Context:\n{context}\n\nQuestion: {query}"

    response = _client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
    )

    return response.choices[0].message.content
