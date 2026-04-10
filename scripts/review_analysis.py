#!/usr/bin/env python3
"""
MOAT App Discovery System — Review Pattern Extractor

Extracts frustration patterns from app review text files.
You paste or import reviews, and it identifies recurring themes.

Usage:
    python review_analysis.py reviews.txt
    python review_analysis.py reviews.txt --top 10
    echo "review text" | python review_analysis.py -
"""

import argparse
import re
import sys
from collections import Counter


# Frustration markers in French and English
NEGATIVE_MARKERS_FR = [
    "bug", "plante", "crash", "lent", "complique", "cher", "payant",
    "manque", "impossible", "nul", "mauvais", "horrible", "decevant",
    "inutile", "pub", "publicite", "abonnement", "force", "oblige",
    "perdu", "supprime", "disparu", "bloque", "marche pas", "fonctionne pas",
    "erreur", "probleme", "difficile", "confus", "incomprehensible",
]

NEGATIVE_MARKERS_EN = [
    "bug", "crash", "slow", "complicated", "expensive", "missing",
    "impossible", "useless", "bad", "horrible", "disappointing",
    "ads", "subscription", "forced", "deleted", "lost", "broken",
    "error", "problem", "difficult", "confusing", "frustrating",
    "won't", "doesn't work", "can't", "annoying", "waste",
]

ALL_MARKERS = NEGATIVE_MARKERS_FR + NEGATIVE_MARKERS_EN


def extract_patterns(text: str, top_n: int = 15) -> dict:
    """Extract frustration patterns from review text."""
    text_lower = text.lower()
    lines = [l.strip() for l in text.split("\n") if l.strip()]

    # Count marker occurrences
    marker_counts = Counter()
    for marker in ALL_MARKERS:
        count = text_lower.count(marker)
        if count > 0:
            marker_counts[marker] = count

    # Extract sentences containing markers
    frustration_sentences = []
    for line in lines:
        line_lower = line.lower()
        if any(m in line_lower for m in ALL_MARKERS):
            frustration_sentences.append(line[:200])

    # Extract bigrams around negative markers for theme detection
    words = re.findall(r'\b[a-zA-Zàâäéèêëïîôùûüç]{3,}\b', text_lower)
    bigrams = Counter()
    for i in range(len(words) - 1):
        if words[i] in ALL_MARKERS or words[i + 1] in ALL_MARKERS:
            bigrams[f"{words[i]} {words[i + 1]}"] += 1

    return {
        "total_lines": len(lines),
        "frustration_lines": len(frustration_sentences),
        "top_markers": marker_counts.most_common(top_n),
        "top_bigrams": bigrams.most_common(top_n),
        "sample_frustrations": frustration_sentences[:10],
    }


def display_results(results: dict):
    """Display analysis results."""
    print("\n" + "=" * 60)
    print("  MOAT — Analyse de frustrations")
    print("=" * 60)

    total = results["total_lines"]
    frust = results["frustration_lines"]
    ratio = round(frust / total * 100, 1) if total > 0 else 0

    print(f"\n  Lignes analysees : {total}")
    print(f"  Lignes avec frustration : {frust} ({ratio}%)")

    print("\n  Marqueurs les plus frequents :")
    for marker, count in results["top_markers"]:
        bar = "#" * min(count, 30)
        print(f"    {marker:25s} {bar} ({count})")

    print("\n  Combinaisons frequentes :")
    for bigram, count in results["top_bigrams"][:10]:
        print(f"    {bigram:30s} ({count})")

    if results["sample_frustrations"]:
        print("\n  Exemples de frustrations :")
        for i, sent in enumerate(results["sample_frustrations"], 1):
            print(f"    {i}. {sent}")

    print("\n" + "=" * 60)


def main():
    parser = argparse.ArgumentParser(description="Extract frustration patterns from reviews")
    parser.add_argument("file", help="Text file with reviews (or - for stdin)")
    parser.add_argument("--top", type=int, default=15, help="Number of top results")
    args = parser.parse_args()

    if args.file == "-":
        text = sys.stdin.read()
    else:
        with open(args.file, "r", encoding="utf-8") as f:
            text = f.read()

    results = extract_patterns(text, args.top)
    display_results(results)


if __name__ == "__main__":
    main()
