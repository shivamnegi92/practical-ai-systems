"""Check whether inline [chunk_id] citations are lexically supported by the cited chunk.

This flags fabricated or mismatched citations using token overlap. It
cannot verify numeric facts or anything a cited chunk merely implies; it
only checks whether the claim's vocabulary appears in the cited source.
"""
from __future__ import annotations

import argparse
import re

_STOPWORDS = frozenset(
    "a an and are as at be by can do does for from has have how i in is it its of on or "
    "our that the their this to was we what when where which who why will with you your".split()
)
_TOKEN_RE = re.compile(r"[a-z0-9]+")
_SENTENCE_RE = re.compile(r"(?<=[.!?])\s+")


def _stem(token: str) -> str:
    for suffix in ("ing", "ed", "es", "s"):
        if len(token) > len(suffix) + 2 and token.endswith(suffix):
            return token[: -len(suffix)]
    return token


def tokenize(text: str) -> list[str]:
    return [_stem(t) for t in _TOKEN_RE.findall(text.lower()) if t not in _STOPWORDS]


def sentences(text: str) -> list[str]:
    return [s.strip() for s in _SENTENCE_RE.split(text.strip()) if s.strip()]

CITATION = re.compile(r"\[([^\]]+)\]")


def check_citations(answer: str, chunks: dict[str, str], min_overlap: float = 0.3) -> dict:
    results = []
    for sent in sentences(answer):
        for match in CITATION.finditer(sent):
            chunk_id = match.group(1)
            if chunk_id not in chunks:
                results.append({"chunk_id": chunk_id, "sentence": sent, "overlap": 0.0, "status": "unknown_chunk"})
                continue
            claim_tokens = set(tokenize(CITATION.sub('', sent)))
            chunk_tokens = set(tokenize(chunks[chunk_id]))
            overlap = len(claim_tokens & chunk_tokens) / len(claim_tokens) if claim_tokens else 0.0
            status = "supported" if claim_tokens and overlap >= min_overlap else "unsupported"
            results.append({"chunk_id": chunk_id, "sentence": sent, "overlap": round(overlap, 4), "status": status})
    return {
        "citations": len(results),
        "results": results,
        "unsupported": [r for r in results if r["status"] != "supported"],
        "all_supported": all(r["status"] == "supported" for r in results) if results else True,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("answer")
    args = parser.parse_args()
    report = check_citations(args.answer, {})
    print(f"{report['citations']} citation(s) found")


if __name__ == "__main__":
    main()
