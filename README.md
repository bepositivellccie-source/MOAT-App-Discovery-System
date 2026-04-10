# MOAT App Discovery System

Systeme data-driven de selection d'opportunites d'apps Flutter.
Connecte a Airtable + Google Play + Google Trends.

## Structure

```
AppHunter/
├── MOAT_PLAYBOOK.md                  # Framework complet (reference)
├── SETUP_AIRTABLE_NOTION.md          # Guide setup Airtable + Notion
├── dashboard.html                    # Dashboard visuel (localhost:8432)
├── templates/
│   ├── opportunity_card.md           # Template fiche opportunite
│   └── competitor_analysis.md        # Template analyse concurrentielle
├── scripts/
│   ├── score_opportunity.py          # Scoring interactif + CLI
│   ├── generate_card.py              # Generateur de fiches
│   ├── review_analysis.py            # Analyse de patterns dans les avis
│   ├── weekly_checklist.py           # Checklist hebdo datee
│   ├── playstore_intel.py            # Google Play intelligence (reviews, ratings, concurrence)
│   ├── trend_radar.py                # Google Trends analysis
│   └── deep_research.py              # Recherche complete (Play Store + Trends + rapport)
└── data/
    ├── opportunity_tracker.csv       # Base locale
    ├── airtable_import.csv           # Import Airtable
    ├── opportunities/                # Fiches generees
    ├── research/                     # Rapports de recherche approfondie
    └── weekly/                       # Checklists hebdomadaires
```

## Outils data

### Google Play Intelligence
```bash
# Analyser une app concurrente (ratings, reviews, frustrations)
python scripts/playstore_intel.py "com.calm.android"

# Analyser plusieurs concurrents
python scripts/playstore_intel.py "com.calm.android" "com.northcube.sleepcycle" --lang fr

# Recherche competitive par mot-cle
python scripts/playstore_intel.py --search "meditation" --lang fr --top 10
```

### Google Trends Radar
```bash
# Analyser une tendance
python scripts/trend_radar.py "insomnie" --geo FR

# Comparer plusieurs mots-cles
python scripts/trend_radar.py "insomnie" "trouble sommeil" "CBT insomnie" --geo FR
```

### Deep Research (tout-en-un)
```bash
# Recherche complete pour une idee
python scripts/deep_research.py "sleep coach" \
  --keywords "insomnie,CBT-I,sommeil app" \
  --competitors "com.northcube.sleepcycle,com.calm.android"
```

## Outils scoring

```bash
# Scorer une idee en interactif
python scripts/score_opportunity.py

# Score rapide CLI
python scripts/score_opportunity.py --idea "Mon app" --scores 4,3,4,3,4,3,3,4,4

# Generer une fiche opportunite
python scripts/generate_card.py

# Checklist de la semaine
python scripts/weekly_checklist.py

# Analyser des avis copies dans un fichier
python scripts/review_analysis.py reviews.txt
```

## Airtable

Base: MOAT App Discovery (appupXnLCe8ZIpKdV)
Table: Opportunity Tracker (tblKhcP3GsGMmhzb1)
22 champs + formule Total Score auto

## Dashboard

```bash
python -m http.server 8432
# Ouvrir http://localhost:8432/dashboard.html
```

## Pipeline

```
SOURCING → QUALIFICATION → SCORING → VALIDATION → DECISION
```

Seuils : A (75+) Build | B (60-74) Validate | C (45-59) Watch | D (<45) Kill

## Dependances

```bash
pip install google-play-scraper pytrends
```
