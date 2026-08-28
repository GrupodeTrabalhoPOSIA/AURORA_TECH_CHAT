"""Dublês compartilhados pelos testes do backend."""

import math


class FakeEmbeddingService:
    """Gera vetores pequenos e determinísticos sem baixar modelos."""

    @staticmethod
    def _embed(text: str) -> list[float]:
        raw = [
            float(len(text)),
            float(sum(character.isalpha() for character in text)),
            float(sum(ord(character) for character in text) % 997),
        ]
        norm = math.sqrt(sum(value * value for value in raw)) or 1.0
        return [value / norm for value in raw]

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self._embed(text) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        return self._embed(text)

