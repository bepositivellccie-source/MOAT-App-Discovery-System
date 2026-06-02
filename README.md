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

## MOAT Engine V3.1 — Regles d'enforcement (2026-04-19)

7 regles bloquantes ajoutees post-audit ShadowWork FR + 3 patterns V3.2 identifies. Voir `scripts/MOAT_ENGINE_V3.1_POSTMORTEM.md`.

### A — Corrections moteur (failles V3)

| Regle | Nom | Enforcement |
|-------|-----|-------------|
| A1 | Coherence TAM-Trend-SOM geographique | Valide TAM vs PIB national cible |
| A2 | Trend STABLE force si volume <50 OU variation <10% sur volume >50 | Override automatique |
| A3 | Ratio Forecast M12 / SOM Solo Y1 | <=3x OK / 3-5x FLAG / >5x KILL |
| A4 | Traçabilite deltas base → V3 | **BLOQUANT a l'ecriture** (regex + arithmetique) |

### B — Ajouts scoring V3.1

| Regle | Nom | Usage |
|-------|-----|-------|
| B5 | Timing type (1 reglementaire / 2 permanent / 3 culturel) | Priorite 1>2>3 a score equivalent |
| B6.1 | Readiness gating binaire (SINGLE/MULTIPLE/SEVERE) | Force B-Validate si blocker actif |
| B7 | Data freshness (>90j force re-audit) | Trigger re-scoring |

### CLI V3.1 exhaustif

```bash
python scripts/moat_engine.py "AppName" \
  --segment-size 1000000 --arpu 60 \
  --trend STABLE --geo-target FR --trend-index-avg 77 \
  --trend-variation-pct 3.4 \
  --flags "partner_medical,rgpd_sante" \
  --blockers-resolved "" \
  --timing-type 2 \
  --forecast-m12-mrr 5000 \
  --data-freshness-date 2026-04-19
```

### Regle #8 projet — Cross-review Opus↔Sonnet

**Declencheurs** (cross-review obligatoire AVANT commit A — Build) :
1. Score V3 >= 75
2. Driver structurel +8 applique
3. Flag retire (market_education, partner_medical, rgpd_sante)
4. Trend multiplier > 1.00

Cout : ~30 min. Benefice demontre : ShadowWork 89→70, SleepCoach 100→70, DecidR 85→78, 3 patterns V3.2 revelles.

## Airtable schema V3.1 (5 champs ajoutes)

- `Score Justification V3.1` (multilineText, BLOQUANT A4)
- `Timing Type V3.1` (singleSelect 1/2/3)
- `Data Freshness Date` (date ISO, trigger re-audit >90j)
- `Readiness Status V3.1` (singleSelect CLEAR/BLOCKED_SINGLE/BLOCKED_MULTIPLE/BLOCKED_SEVERE/STALE_DATA/LEGACY_V3_PENDING/AUDITED_V3_1_CROSS_REVIEW/POSITIONING_DECISION_REQUIRED)
- `Legacy V3` (checkbox, tag migration)

## Dependances

```bash
pip install google-play-scraper pytrends
```
