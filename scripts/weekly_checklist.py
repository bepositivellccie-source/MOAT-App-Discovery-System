#!/usr/bin/env python3
"""
MOAT App Discovery System — Weekly Checklist Generator

Generates a dated weekly checklist for the MOAT workflow.

Usage:
    python weekly_checklist.py
    python weekly_checklist.py --week 2026-04-13
"""

import argparse
import os
from datetime import datetime, timedelta


def generate_checklist(start_date: datetime) -> str:
    """Generate a weekly MOAT checklist."""
    monday = start_date - timedelta(days=start_date.weekday())
    dates = {
        "lundi": monday,
        "mardi": monday + timedelta(days=1),
        "mercredi": monday + timedelta(days=2),
        "jeudi": monday + timedelta(days=3),
        "vendredi": monday + timedelta(days=4),
    }

    return f"""# MOAT Weekly — Semaine du {monday.strftime('%Y-%m-%d')}

---

## Lundi {dates['lundi'].strftime('%d/%m')} — COLLECTE (1-2h)

- [ ] Lire 15-20 avis concurrents (1-3 etoiles)
  - App 1 : _______________  Notes :
  - App 2 : _______________  Notes :
  - App 3 : _______________  Notes :
- [ ] Capturer 5 frustrations recurrentes
  1.
  2.
  3.
  4.
  5.
- [ ] Capturer 5 mots-cles / expressions reelles
  1.
  2.
  3.
  4.
  5.
- [ ] Scanner 3 communautes (Reddit/Discord/forums)
  - Communaute 1 :
  - Communaute 2 :
  - Communaute 3 :
- [ ] Verifier Google Trends (themes actifs)
- [ ] Ajouter les signaux bruts dans le backlog

---

## Mardi {dates['mardi'].strftime('%d/%m')} — FORMULATION (1h)

- [ ] Transformer chaque frustration en probleme structure
  - "[SEGMENT] perd [QUOI] a cause de [POURQUOI]"
  1.
  2.
  3.
  4.
  5.
- [ ] Ecrire l'hypothese segment pour chaque idee
- [ ] Ecrire l'hypothese monetisation pour chaque idee
- [ ] Eliminer les idees sans frequence / sans douleur / sans paiement
- [ ] Mettre a jour le backlog (data/opportunity_tracker.csv)

Idees eliminees et pourquoi :
-
-

---

## Mercredi {dates['mercredi'].strftime('%d/%m')} — SCORING (1h)

- [ ] Noter les nouvelles idees (python scripts/score_opportunity.py)
- [ ] Comparer le top 5 du backlog
- [ ] Identifier les faux positifs ("interessant mais flou")
- [ ] Mettre a jour les statuts A/B/C/D

Top 5 de la semaine :
| # | Idee | Score | Categorie |
|---|------|-------|-----------|
| 1 | | /100 | |
| 2 | | /100 | |
| 3 | | /100 | |
| 4 | | /100 | |
| 5 | | /100 | |

---

## Jeudi {dates['jeudi'].strftime('%d/%m')} — VALIDATION (2h)

- [ ] Creer une landing page simple (Carrd/Framer/Tally)
  - URL :
  - Promesse testee :
- [ ] Diffuser aupres de 20-50 personnes ciblees
  - Canal utilise :
  - Nombre de personnes contactees :
- [ ] Mesurer les resultats
  - Clics :
  - Inscriptions :
  - Reponses :
  - Objections :

---

## Vendredi {dates['vendredi'].strftime('%d/%m')} — DECISION (30min)

### Decisions de la semaine

| Idee | Decision | Raison |
|------|----------|--------|
| | GO / PAUSE / KILL | |
| | GO / PAUSE / KILL | |
| | GO / PAUSE / KILL | |

### Bilan hebdomadaire

- Idees sourcees cette semaine :
- Idees qualifiees :
- Idees tuees :
- Prochaine validation a faire :

---

## Notes de la semaine

"""


def main():
    parser = argparse.ArgumentParser(description="MOAT Weekly Checklist Generator")
    parser.add_argument("--week", help="Date de la semaine (YYYY-MM-DD), defaut: cette semaine")
    args = parser.parse_args()

    if args.week:
        start = datetime.strptime(args.week, "%Y-%m-%d")
    else:
        start = datetime.now()

    checklist = generate_checklist(start)

    # Save to data/weekly/
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "weekly")
    os.makedirs(output_dir, exist_ok=True)

    monday = start - timedelta(days=start.weekday())
    filename = f"week_{monday.strftime('%Y-%m-%d')}.md"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(checklist)

    print(f"Checklist creee : {filepath}")
    print(checklist)


if __name__ == "__main__":
    main()
