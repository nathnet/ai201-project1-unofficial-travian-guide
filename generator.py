from groq import Groq

from config import GROQ_API_KEY, GROQ_MODEL, HISTORY_TURNS

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

You will also receive prior conversation turns for context. Use them to understand follow-up
questions (e.g. resolving pronouns like "they" or "it" from the previous question), but all
factual claims must still be grounded in the context chunks provided — not the conversation history.
"""


NO_CONTEXT_RESPONSE = (
    "I don't have enough information in my knowledge base to answer that question. "
    "Could you try rephrasing it or ask something more specific about Travian: Legends?"
)


def generate_response(query: str, retrieved_chunks: list[dict], history: list | None = None) -> str:
    """Assemble a grounded prompt from retrieved chunks and call Groq to generate a response."""
    if not retrieved_chunks:
        return NO_CONTEXT_RESPONSE

    context_parts = []
    for chunk in retrieved_chunks:
        source = chunk["metadata"]["source"]
        doc_type = chunk["metadata"]["type"]
        distance = chunk.get("distance")
        distance_str = f"{distance:.4f}" if distance is not None else "n/a"
        context_parts.append(
            f"(source: {source}, type: {doc_type}, distance: {distance_str}) - {chunk['text']}"
        )
    context = "\n\n---\n\n".join(context_parts)

    user_message = f"Context:\n{context}\n\nQuestion: {query}"

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    if history:
        # Each turn is {"role": ..., "content": ...}; slice by pairs to keep HISTORY_WINDOW turns
        recent = history[-(HISTORY_TURNS * 2):]
        for turn in recent:
            messages.append({"role": turn["role"], "content": turn["content"]})

    messages.append({"role": "user", "content": user_message})

    response = _client.chat.completions.create(
        model=GROQ_MODEL,
        messages=messages,
    )

    return response.choices[0].message.content
