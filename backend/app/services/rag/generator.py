"""
LLM Generator — Generate answers using LLM (Ollama, OpenAI, Claude, Gemini).

Supports multiple LLM providers:
- Phase 1: Ollama (local, free) — Llama 3 / Mistral
- Phase 2: OpenAI, Claude, Gemini (cloud APIs)
"""

import httpx

from app.config import settings


class LLMGenerator:
    """
    Generates answers using configurable LLM providers.
    Provider is selected based on settings.llm_provider.
    """

    def __init__(self):
        self.provider = settings.llm_provider

    async def generate(self, system_prompt: str, user_prompt: str) -> str:
        """
        Generate a response from the LLM.

        Args:
            system_prompt: System instructions for the LLM
            user_prompt: User message with context and question

        Returns:
            Generated text response
        """
        if self.provider == "ollama":
            return await self._generate_ollama(system_prompt, user_prompt)
        elif self.provider == "openai":
            return await self._generate_openai(system_prompt, user_prompt)
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")

    async def _generate_ollama(self, system_prompt: str, user_prompt: str) -> str:
        """Generate response using local Ollama API."""
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{settings.ollama_base_url}/api/chat",
                json={
                    "model": settings.ollama_model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    "stream": False,
                },
            )
            response.raise_for_status()
            data = response.json()
            return data.get("message", {}).get("content", "")

    async def _generate_openai(self, system_prompt: str, user_prompt: str) -> str:
        """Generate response using OpenAI API."""
        # TODO: Implement OpenAI integration
        # Uses the openai Python package
        from openai import AsyncOpenAI

        client = AsyncOpenAI(api_key=settings.openai_api_key)
        response = await client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.3,
            max_tokens=2000,
        )
        return response.choices[0].message.content or ""


# Singleton instance
_generator_instance = None


def get_generator() -> LLMGenerator:
    """Get or create the singleton LLMGenerator instance."""
    global _generator_instance
    if _generator_instance is None:
        _generator_instance = LLMGenerator()
    return _generator_instance
