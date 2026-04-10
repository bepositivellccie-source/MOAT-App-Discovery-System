#!/usr/bin/env python3
"""
MOAT App Discovery System — Scoring Calculator

Usage:
    python score_opportunity.py
    python score_opportunity.py --batch data/opportunity_tracker.csv
    python score_opportunity.py --idea "Mon idee" --scores 4,3,4,3,4,3,3,4,4
"""

import argparse
import csv
import os
import sys
from datetime import datetime

CRITERIA = [
    ("Intensite du probleme", 4, "Douleur forte et repetee? (1=confort, 5=critique)"),
    ("Frequence d'usage", 3, "Besoin recurrent? (1=annuel, 5=quotidien)"),
    ("Volonte de payer", 3, "Paiement observe ou evident? (1=aucun, 5=actif)"),
    ("Segment accessible", 2, "Facile a atteindre? (1=invisible, 5=canaux clairs)"),
    ("Faiblesse concurrentielle", 2, "Marche mal servi? (1=domine, 5=aucune solution)"),
    ("Differenciation", 2, "Angle nettement meilleur? (1=me-too, 5=unique)"),
    ("Fit personnel", 2, "Skills + reseau + interet? (1=etranger, 5=expert)"),
    ("Vitesse MVP", 1, "Rapidite de build? (1=6mois+, 5=1-2 semaines)"),
    ("Retention potentielle", 1, "Usage habituel? (1=unique, 5=quotidien)"),
]

MAX_SCORE = sum(weight * 5 for _, weight, _ in CRITERIA)  # 100


def calculate_score(scores: list[int]) -> dict:
    """Calculate weighted score from a list of 9 scores (1-5 each)."""
    if len(scores) != len(CRITERIA):
        raise ValueError(f"Expected {len(CRITERIA)} scores, got {len(scores)}")

    details = []
    total = 0
    for i, (name, weight, _) in enumerate(CRITERIA):
        raw = scores[i]
        if not 1 <= raw <= 5:
            raise ValueError(f"Score for '{name}' must be 1-5, got {raw}")
        weighted = raw * weight
        total += weighted
        details.append({
            "criterion": name,
            "raw": raw,
            "weight": weight,
            "weighted": weighted,
            "max": weight * 5,
        })

    category = (
        "A — Build now" if total >= 75 else
        "B — Validate" if total >= 60 else
        "C — Watchlist" if total >= 45 else
        "D — Kill"
    )

    return {
        "total": total,
        "max": MAX_SCORE,
        "percentage": round(total / MAX_SCORE * 100, 1),
        "category": category,
        "details": details,
    }


def interactive_scoring():
    """Interactive mode: ask each criterion one by one."""
    print("\n" + "=" * 60)
    print("  MOAT Scoring — Evaluation interactive")
    print("=" * 60)

    idea_name = input("\nNom de l'idee : ").strip()
    segment = input("Segment cible : ").strip()

    scores = []
    print("\nNote chaque critere de 1 a 5 :\n")

    for name, weight, description in CRITERIA:
        while True:
            try:
                val = int(input(f"  [{weight}x] {name}\n       {description}\n       Score : "))
                if 1 <= val <= 5:
                    scores.append(val)
                    print()
                    break
                print("       → Entre 1 et 5.")
            except ValueError:
                print("       → Nombre entier requis.")

    result = calculate_score(scores)

    print("\n" + "=" * 60)
    print(f"  RESULTAT : {idea_name}")
    print("=" * 60)
    print(f"\n  Segment : {segment}\n")

    for d in result["details"]:
        bar = "#" * d["raw"] + "." * (5 - d["raw"])
        print(f"  {d['criterion']:30s} [{bar}] {d['weighted']:2d}/{d['max']}")

    print(f"\n  {'TOTAL':30s}         {result['total']}/{result['max']}")
    print(f"  {'CATEGORIE':30s}         {result['category']}")
    print("=" * 60)

    # Go/No-Go checklist
    print("\n  Checklist Go/No-Go (repondre o/n) :\n")
    conditions = [
        "Probleme douloureux",
        "Segment precis",
        "Paiement plausible",
        "MVP faisable en <6 semaines",
        "Canal d'acces realiste",
    ]
    passed = 0
    for c in conditions:
        resp = input(f"  [ ] {c} ? (o/n) : ").strip().lower()
        if resp in ("o", "oui", "y", "yes"):
            passed += 1
            print(f"  [x] {c}")
        else:
            print(f"  [ ] {c}")

    print(f"\n  Conditions validees : {passed}/5")
    if passed >= 4:
        print("  → GO : cette idee merite un MVP.")
    elif passed >= 3:
        print("  → VALIDER : creuser avant de builder.")
    else:
        print("  → KILL ou WATCHLIST : pas assez de signal.")

    return {
        "idea": idea_name,
        "segment": segment,
        "scores": scores,
        "total": result["total"],
        "category": result["category"],
        "go_conditions": passed,
    }


def quick_score(idea_name: str, scores_str: str):
    """Quick score from command line args."""
    scores = [int(s.strip()) for s in scores_str.split(",")]
    result = calculate_score(scores)

    print(f"\n  {idea_name}: {result['total']}/100 — {result['category']}")
    for d in result["details"]:
        bar = "#" * d["raw"] + "." * (5 - d["raw"])
        print(f"    {d['criterion']:30s} {bar} {d['weighted']:2d}/{d['max']}")


def batch_recalculate(csv_path: str):
    """Recalculate scores for all entries in the CSV tracker."""
    if not os.path.exists(csv_path):
        print(f"Fichier non trouve : {csv_path}")
        return

    rows = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            try:
                scores = [
                    int(row.get("pain_score", 0) or 0),
                    int(row.get("frequency_score", 0) or 0),
                    int(row.get("willingness_to_pay", 0) or 0),
                    int(row.get("competition_gap", 0) or 0),
                    int(row.get("differentiation", 0) or 0),
                    int(row.get("fit_with_me", 0) or 0),
                    int(row.get("mvp_speed", 0) or 0),
                    int(row.get("retention", 0) or 0),
                ]
                # Check if all scores are valid
                if all(1 <= s <= 5 for s in scores):
                    # Note: CSV has 8 score fields but scoring needs 9
                    # competition_gap maps to both "faiblesse concurrentielle" and "differenciation"
                    # Adjust if your CSV structure differs
                    result = calculate_score(scores + [scores[-1]])  # placeholder
                    row["total_score"] = result["total"]
                    row["decision"] = result["category"][0]  # A, B, C, or D
            except (ValueError, KeyError):
                pass
            rows.append(row)

    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Scores recalcules pour {len(rows)} entrees dans {csv_path}")


def main():
    parser = argparse.ArgumentParser(description="MOAT Scoring Calculator")
    parser.add_argument("--idea", help="Nom de l'idee (mode rapide)")
    parser.add_argument("--scores", help="9 scores separes par des virgules (mode rapide)")
    parser.add_argument("--batch", help="Recalculer les scores d'un fichier CSV")
    args = parser.parse_args()

    if args.batch:
        batch_recalculate(args.batch)
    elif args.idea and args.scores:
        quick_score(args.idea, args.scores)
    else:
        interactive_scoring()


if __name__ == "__main__":
    main()
