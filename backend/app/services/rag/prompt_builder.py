"""
Prompt Builder — Assemble LLM prompts from question + retrieved context.

Builds structured prompts that instruct the LLM to:
1. Answer based ONLY on the provided context
2. Include source citations
3. Admit when information is not available
"""


class PromptBuilder:
    """Builds prompts for the LLM using retrieved context chunks."""

    SYSTEM_PROMPT = """You are a Website Content Intelligence Assistant. Your role is to answer questions about a website's content based ONLY on the provided context.

Rules:
1. Answer ONLY using information from the provided context.
2. ALWAYS cite your sources by referencing the page URL and title.
3. If the context doesn't contain enough information to answer, say so clearly.
4. Do NOT make up or hallucinate information.
5. Be concise but thorough in your answers.
6. When multiple pages contain relevant information, synthesize the answer and cite all sources."""

    CONTEXT_TEMPLATE = """--- Source: {title} ---
URL: {url}
Content:
{content}
---"""

    QUESTION_TEMPLATE = """Based on the following website content, please answer the question.

CONTEXT:
{context}

QUESTION: {question}

Provide a clear answer with source citations. For each piece of information, reference the source URL."""

    def build_prompt(self, question: str, chunks: list[dict]) -> dict:
        """
        Build a complete prompt for the LLM.

        Args:
            question: The user's question
            chunks: Retrieved content chunks with metadata

        Returns:
            Dict with:
            {
                "system": str,  # System prompt
                "user": str,    # User prompt with context + question
            }
        """
        # Build context section from retrieved chunks
        context_parts = []
        for chunk in chunks:
            metadata = chunk.get("metadata", {})
            context_parts.append(
                self.CONTEXT_TEMPLATE.format(
                    title=metadata.get("title", "Unknown Page"),
                    url=metadata.get("url", "Unknown URL"),
                    content=chunk.get("content", ""),
                )
            )

        context = "\n\n".join(context_parts)

        # Build the full user prompt
        user_prompt = self.QUESTION_TEMPLATE.format(
            context=context,
            question=question,
        )

        return {
            "system": self.SYSTEM_PROMPT,
            "user": user_prompt,
        }
