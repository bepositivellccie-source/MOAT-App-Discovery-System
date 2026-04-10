#!/usr/bin/env python3
"""
MOAT App Discovery System — Opportunity Card Generator

Creates a pre-filled opportunity card from command line or interactive input.

Usage:
    python generate_card.py
    python generate_card.py --idea "Agenda Kine" --segment "Kines independants" --problem "Gestion manuelle des RDV"
"""

import argparse
import os
import re
from datetime import datetime


TEMPLATE = """# {idea}

## Identite
- **Categorie** : {category}
- **Segment cible** : {segment}
- **Date de creation** : {date}
- **Statut** : Backlog

## Probleme
- **Enonce** : {segment} perd {what} a cause de {why}
- **Contexte d'usage** : {context}
- **Alternative actuelle** : {alternative}
- **Pourquoi c'est penible** : {pain}

## Marche
- **Taille estimee du segment** : A estimer
- **Tendance** : A verifier
- **Concurrents directs** : A rechercher
- **Gaps concurrentiels** : A analyser

## Proposition
- **Hypothese de valeur** : {value_prop}
- **Differenciation** : A definir
- **Monetisation** : {monetization}
- **Prix envisage** : A tester

## Validation
- [ ] Hypothese probleme confirmee
- [ ] Hypothese segment confirmee
- [ ] Hypothese valeur confirmee
- [ ] Hypothese paiement confirmee
- [ ] Hypothese canal confirmee

## Preuves
- **Avis analyses** : 0
- **Posts/forums** :
- **Interviews** : 0
- **Landing page** : Non creee
- **Autres signaux** :

## Scoring

| Critere | Score (1-5) | Pondere |
|---------|-------------|---------|
| Intensite probleme | _ | _/20 |
| Frequence usage | _ | _/15 |
| Volonte de payer | _ | _/15 |
| Segment accessible | _ | _/10 |
| Faiblesse concurrence | _ | _/10 |
| Differenciation | _ | _/10 |
| Fit personnel | _ | _/10 |
| Vitesse MVP | _ | _/5 |
| Retention | _ | _/5 |
| **TOTAL** | | **_/100** |

## Decision
- **Categorie** : A scorer
- **Prochaine action** : Recherche concurrentielle + scoring
- **Deadline** : {deadline}
"""


def slugify(text: str) -> str:
    """Convert text to a filename-safe slug."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '_', text)
    return text


def interactive_generate():
    """Interactive card generation."""
    print("\n" + "=" * 60)
    print("  MOAT — Generateur de fiche opportunite")
    print("=" * 60)

    idea = input("\nNom de l'idee : ").strip()
    category = input("Categorie (Productivite/Sante/Finance/Education/Metier/Autre) : ").strip()
    segment = input("Segment cible (ex: 'Kines respiratoires independants') : ").strip()
    what = input("Ce que le segment perd (temps/argent/clients/...) : ").strip()
    why = input("A cause de quoi : ").strip()
    context = input("Contexte d'usage (quand/ou le probleme survient) : ").strip()
    alternative = input("Alternative actuelle (ce qu'ils font aujourd'hui) : ").strip()
    pain = input("Pourquoi c'est penible : ").strip()
    value_prop = input("Hypothese de valeur (ce que l'app ferait mieux) : ").strip()
    monetization = input("Monetisation envisagee (Freemium/Abo/Usage/One-time) : ").strip() or "A definir"

    today = datetime.now().strftime("%Y-%m-%d")
    deadline = input(f"Deadline de decision (defaut: 2 semaines) : ").strip()
    if not deadline:
        from datetime import timedelta
        deadline = (datetime.now() + timedelta(weeks=2)).strftime("%Y-%m-%d")

    content = TEMPLATE.format(
        idea=idea,
        category=category,
        segment=segment,
        date=today,
        what=what,
        why=why,
        context=context,
        alternative=alternative,
        pain=pain,
        value_prop=value_prop,
        monetization=monetization,
        deadline=deadline,
    )

    # Save to data/opportunities/
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "opportunities")
    os.makedirs(output_dir, exist_ok=True)

    filename = f"{today}_{slugify(idea)}.md"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"\n  Fiche creee : {filepath}")
    print(f"  Prochaine etape : scorer avec score_opportunity.py")

    return filepath


def quick_generate(idea: str, segment: str, problem: str):
    """Quick generation from args."""
    today = datetime.now().strftime("%Y-%m-%d")
    from datetime import timedelta
    deadline = (datetime.now() + timedelta(weeks=2)).strftime("%Y-%m-%d")

    content = TEMPLATE.format(
        idea=idea,
        category="A definir",
        segment=segment,
        date=today,
        what="[a preciser]",
        why=problem,
        context="[a preciser]",
        alternative="[a rechercher]",
        pain="[a documenter]",
        value_prop="[a definir]",
        monetization="A definir",
        deadline=deadline,
    )

    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "opportunities")
    os.makedirs(output_dir, exist_ok=True)

    filename = f"{today}_{slugify(idea)}.md"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"\n  Fiche creee : {filepath}")
    return filepath


def main():
    parser = argparse.ArgumentParser(description="MOAT Opportunity Card Generator")
    parser.add_argument("--idea", help="Nom de l'idee")
    parser.add_argument("--segment", help="Segment cible")
    parser.add_argument("--problem", help="Probleme central")
    args = parser.parse_args()

    if args.idea and args.segment and args.problem:
        quick_generate(args.idea, args.segment, args.problem)
    else:
        interactive_generate()


if __name__ == "__main__":
    main()
