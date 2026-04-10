# Setup Airtable & Notion — MOAT App Discovery System

---

## OPTION A : Airtable (recommande pour le scoring)

### 1. Creer la base

Importer `data/airtable_import.csv` dans Airtable (Add a base > Import > CSV).

### 2. Configurer les types de champs

| Champ | Type Airtable | Options |
|-------|--------------|---------|
| Idea | Single line text | (Titre) |
| Category | Single select | Productivite, Sante, Finance, Education, Metier, IA, Utilitaire |
| Segment | Long text | |
| Problem | Long text | |
| Context | Long text | |
| Current Alternative | Long text | |
| Pain (1-5) | Rating | Max 5 |
| Frequency (1-5) | Rating | Max 5 |
| Will Pay (1-5) | Rating | Max 5 |
| Market Access (1-5) | Rating | Max 5 |
| Competition Gap (1-5) | Rating | Max 5 |
| Differentiation (1-5) | Rating | Max 5 |
| Personal Fit (1-5) | Rating | Max 5 |
| MVP Speed (1-5) | Rating | Max 5 |
| Retention (1-5) | Rating | Max 5 |
| Total Score | Formula | (voir ci-dessous) |
| Revenue Model | Single select | Freemium, Abonnement, Usage-based, One-time, Ads |
| Distribution | Single line text | |
| Status | Single select | Backlog, Scoring, Validation, Ready to Build, Killed |
| Decision | Single select | A — Build now, B — Validate, C — Watchlist, D — Kill |
| Evidence | Long text | |
| Last Reviewed | Date | |
| Next Action | Single line text | |

### 3. Formule du score total

Coller cette formule dans le champ "Total Score" :

```
({Pain (1-5)} * 4) +
({Frequency (1-5)} * 3) +
({Will Pay (1-5)} * 3) +
({Market Access (1-5)} * 2) +
({Competition Gap (1-5)} * 2) +
({Differentiation (1-5)} * 2) +
({Personal Fit (1-5)} * 2) +
({MVP Speed (1-5)} * 1) +
({Retention (1-5)} * 1)
```

### 4. Ajouter un champ "Decision Auto" (optionnel)

```
IF({Total Score} >= 75, "A — Build now",
  IF({Total Score} >= 60, "B — Validate",
    IF({Total Score} >= 45, "C — Watchlist",
      "D — Kill")))
```

### 5. Creer les vues

| Vue | Type | Filtre |
|-----|------|--------|
| Backlog brut | Grid | Status = Backlog |
| Top 10 | Grid | Trier par Total Score desc, Limit 10 |
| A valider | Kanban | Grouper par Decision |
| Pipeline | Kanban | Grouper par Status |
| Tuees | Grid | Status = Killed |
| Cette semaine | Grid | Last Reviewed = cette semaine |

### 6. Automatisations utiles

- **Rappel hebdomadaire** : chaque lundi, notifier les idees en "Backlog" depuis >2 semaines
- **Auto-kill** : si Total Score < 45, mettre Decision = "D — Kill"
- **Relance validation** : si Status = "Validation" depuis >1 semaine sans update

---

## OPTION B : Notion (recommande pour la documentation)

### 1. Creer une database "MOAT Opportunity Tracker"

Proprietes :

| Propriete | Type | Options |
|-----------|------|---------|
| Idea | Title | |
| Category | Select | Productivite, Sante, Finance, Education, Metier, IA, Utilitaire |
| Segment | Text | |
| Problem | Text | |
| Pain | Number | |
| Frequency | Number | |
| Will Pay | Number | |
| Market Access | Number | |
| Competition Gap | Number | |
| Differentiation | Number | |
| Personal Fit | Number | |
| MVP Speed | Number | |
| Retention | Number | |
| Total Score | Formula | `prop("Pain") * 4 + prop("Frequency") * 3 + prop("Will Pay") * 3 + prop("Market Access") * 2 + prop("Competition Gap") * 2 + prop("Differentiation") * 2 + prop("Personal Fit") * 2 + prop("MVP Speed") * 1 + prop("Retention") * 1` |
| Decision | Formula | `if(prop("Total Score") >= 75, "A", if(prop("Total Score") >= 60, "B", if(prop("Total Score") >= 45, "C", "D")))` |
| Status | Select | Backlog, Scoring, Validation, Ready to Build, Killed |
| Revenue Model | Select | Freemium, Abonnement, Usage-based, One-time |
| Distribution | Text | |
| Evidence | URL | |
| Last Reviewed | Date | |
| Next Action | Text | |

### 2. Creer les vues

- **Table — Backlog** : filtre Status = Backlog
- **Table — Top Score** : tri Total Score desc
- **Board — Pipeline** : grouper par Status
- **Board — Decisions** : grouper par Decision
- **Calendar** : par Last Reviewed

### 3. Template de page

Chaque entree de la database peut contenir la fiche opportunite complete
(copier le contenu de `templates/opportunity_card.md` comme template de page).

---

## Workflow combine recommande

```
Airtable = pipeline + scoring + filtrage rapide
Notion = fiches detaillees + recherche qualitative + documentation
Claude Code = synthese + analyse + generation de fiches
```

Quand tu identifies une idee prometteuse dans Airtable (score > 60),
cree une fiche complete dans Notion avec le template opportunity_card.md.
