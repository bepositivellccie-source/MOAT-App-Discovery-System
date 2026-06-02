# MOAT Engine V3.1 — Post-mortem Shadow Work FR

**Date** : 2026-04-19
**Auteurs** : Claude Opus Code + Claude Sonnet (cross-review)
**Contexte** : ShadowWork FR score revise 89 → 70 apres audit Sonnet. La discussion a revele 2 failles structurelles du moteur V3 qui vont se reproduire sur d'autres apps du pipeline si non corrigees.

---

## Faille #1 — Trend Multiplier mondial applique a un projet national

### Probleme

Le moteur V3 accepte un parametre `--trend` (UP/EXPLOSIVE/STABLE/DOWN) sans verifier si le trend provient du marche cible geographique ou du trend mondial.

Dans le cas ShadowWork FR :
- Trend mondial : +92% sur 12 mois, index 60/100 → UP clair
- Trend FR cible : +692% mais index actuel 0, moyenne 20/100 → artefact sur micro-volume

J'ai applique UP (x1.08) base sur le trend mondial, alors que la cible est francophonie. Sonnet aurait commis la meme erreur sans relecture.

### Consequence

Score gonfle artificiellement. ShadowWork FR est passe de 70 (realite) a 89 (surcote de 19 points a cause d'un multiplicateur inapproprie + flag market_education oublie).

### Correction V3.1 proposee

**Regle a enforcer dans `data_backed_score()` :**

```python
# V3.1 — Trend Multiplier DOIT correspondre au marche cible geographique
# Si le projet cible un marche national/regional specifique, le trend doit etre celui de ce marche
# PAS le trend mondial

# Verification automatique :
if geographic_target in ['FR', 'DE', 'IT', 'ES', 'UK', 'QC', ...]:
    if trend_market_index_12m_avg < 50:
        # Volume absolu trop faible pour prouver une direction fiable
        trend_direction = 'STABLE'
        trend_flag = 'MICRO_VOLUME_GUARD'
        # Logger un warning visible dans le rapport final
```

**Seuils :**
- Index moyen 12 mois marche cible < 50/100 → STABLE x1.00 par defaut
- Variation % ignoree si volume absolu insuffisant (artefact mathematique)
- Trend monde != trend cible → toujours prendre le cible

**Parametre CLI a ajouter :**
```bash
python moat_engine.py "App" --trend UP --trend-geo FR --trend-index-avg 20
# Si --trend-index-avg < 50 : override automatique a STABLE
```

---

## Faille #1b — Biais geographique en cascade sur 3 etages (enrichi par Sonnet)

### Probleme elargi

Le bug n'est pas juste "trend mondial applique a cible nationale". C'est un **biais geographique en cascade sur 3 etages** qui se compose mecaniquement :

| Etage | Bug observe sur pipeline existant | Impact |
|-------|-----------------------------------|--------|
| **TAM** | Affiche mondial sur cible nationale (SleepCoach 1.2B€, SoulageR 720M€) | Inflation base |
| **Trend multiplier** | Calcul monde applique a FR | x1.08 injustifie |
| **SOM × 7%** | Applique a TAM mondial = SOM mondial Solo Y1 | Ratio 5-10× mecanique |

Les 3 se composent. Un TAM mondial × trend mondial × SOM Solo fantasme = forecast 10× realite. C'est pour ca que les ratios forecast/SOM Solo sont systematiquement 5.8×, 8×, 10.7× sur le pipeline — pas malchance, bug structurel qui se reproduit a chaque scoring.

### Correction V3.1 additionnelle

**Regle de coherence geographique TAM-Trend-SOM** :
- Si cible = FR → TAM doit etre TAM FR uniquement, trend = trend FR uniquement, SOM = SOM FR uniquement
- Jamais de mix (TAM mondial + SOM FR, trend monde + TAM national, etc.)
- Parametre CLI `--geo-target FR` pour expliciter la cible
- Validation automatique : si TAM > PIB_national/10, flagger TAM_suspect_global

## Faille #3 — Tracabilite deltas score base → score V3 (detectee sur NutriZen)

### Probleme

Le moteur V3 permet a un score de passer de base N a V3 M sans que chaque delta soit justifie par une regle explicite. Resultat : des "+4 pts fantomes" peuvent apparaitre sans trace.

**Cas NutriZen observe** :
- Score base 9 criteres : **76/100**
- Score V3 stocke : **80/100**
- Delta : **+4 pts inexpliques** (pas de trend multiplier documente, pas de driver structurel, pas de flag retire)

C'est une faille **orthogonale** aux 3 autres :
- Faille #1 (trend geo) + #1b (TAM-Trend-SOM) + #2 (coherence ratio) = erreurs de **calcul**
- **Faille #3 (tracabilite) = modifications non tracees** (deltas apparaissant "de nulle part")

Sans correction, un moteur V3.1 parfait peut etre contourne par une modification manuelle non justifiee.

### Consequence

Risque d'inflation invisible des scores. Le cas NutriZen (+4) semble mineur mais le pattern peut se reproduire a +6, +8, +10 sur d'autres apps. Sans traçabilite, impossible de re-auditer honnetement.

### Correction V3.1 proposee

**Regle a enforcer dans `data_backed_score()` et dans le template fiche :**

Chaque modification entre score base (9 criteres) et score V3 doit generer une ligne de **justification chiffree obligatoire** dans un champ dedie `score_audit_trail`.

Format impose :
```
SCORE AUDIT TRAIL:
- Base (9 criteres) : 76
- Trend multiplier : x1.00 (STABLE, +0 pts) OU x1.08 (UP, +6 pts)
- Driver structurel : +0 OU +8 (avec source reglementaire)
- Flag market_education : -10 OU 0
- Flag partner_medical : -15 OU 0
- Flag rgpd_sante : -5 OU 0
- Flag regulatory_risk : -12 OU 0
- Flag forecast_incoherent : -3 OU 0 (credibilite WTP)
- TOTAL V3 : XX
```

**Regle de validation :**
```python
# V3.1 — Traçabilite obligatoire des deltas
delta_total = score_v3 - score_base
expected_delta = (trend_bonus + structural_bonus - flags_penalties)

if abs(delta_total - expected_delta) > 0:
    raise ValueError(
        f"Delta non trace : score base {score_base} → V3 {score_v3} "
        f"({delta_total:+d}) mais regles appliquees = {expected_delta:+d}. "
        f"Difference inexpliquee de {delta_total - expected_delta:+d} pts."
    )
```

**Affichage fiche obligatoire :**
- Section "Score Audit Trail" visible dans le dashboard
- Chaque ligne cliquable pour voir la source (trend_radar output, loi citee, etc.)

### Enforcement BLOQUANT a l'ecriture (precision Sonnet)

La traçabilite n'est **pas** un audit trail a posteriori. Elle est **bloquante a l'ecriture Airtable/dashboard**.

**Format impose du champ `score_justification`** :
```
base: {N}
+ trend_multiplier: {value} (source: trend_radar {geo}, index moy 12m: {X})
+ driver_structurel: {value} (justif: {loi + date obligation OU "aucun"})
+ flags: [{name}: {value}, ...]
= score_v3: {N}
```

**Enforcement dans `commit_to_airtable()` :**
```python
def validate_score_justification(justification: str, score_base: int, score_v3: int) -> None:
    """Raise ValidationError if justification is missing or non-conforming."""
    if not justification or not justification.strip():
        raise ValidationError("score_justification is mandatory")
    
    # Parse structured format
    parsed = parse_justification_format(justification)
    if not parsed:
        raise ValidationError(
            f"score_justification must follow enforced format:\n"
            f"base: N\n+ trend_multiplier: X\n+ driver_structurel: Y\n"
            f"+ flags: [...]\n= score_v3: M"
        )
    
    # Verify arithmetic
    expected_v3 = parsed['base'] + parsed['trend_delta'] + parsed['driver_delta'] - parsed['flags_total']
    if expected_v3 != score_v3:
        raise ValidationError(
            f"Arithmetic mismatch: expected V3 = {expected_v3}, got {score_v3}. "
            f"Difference inexpliquee de {score_v3 - expected_v3:+d} pts."
        )
```

**Consequence** : si un scoring V3 est committé en Airtable sans `score_justification` valide, le moteur **refuse l'ecriture**. Pas de contournement possible.

### Cas a re-auditer avec cette regle

- **NutriZen** : 76 → 80 = +4 fantomes. Re-scoring V3.1 donnera 73 (deltas traces honnetement)
- **Verifier aussi** : toute app du pipeline ou engineScore != score (score affiche sur dashboard) sans justification explicite

## Faille #2 — SOM Solo Dev Y1 et Forecast MRR peuvent etre incoherents

### Probleme

Actuellement, la fiche stocke deux chiffres qui peuvent vivre cote a cote sans coherence check :
- **SOM Solo Dev Y1** calcule par formule MOAT : TAM × SAM × SOM × 7% solo dev factor
- **Forecast MRR M12** calcule independamment : subs × prix × conversion

Dans le cas ShadowWork FR :
- SOM Solo Dev Y1 affiche : **2.87K€/mois**
- Forecast MRR M12 base affiche : **27.4K€/mois** (10× le SOM)
- Forecast MRR M12 optimiste : **54.9K€/mois** (20× le SOM)

Le forecast impliquait capturer 53% du TAM payants total (410K users) en 12 mois, solo dev, sans budget. Fantasme total.

### Consequence

Un projet peut apparaitre economiquement viable sur le forecast MRR alors que le SOM Solo Dev Y1 le contredit. Biais d'ancrage sur le chiffre le plus flatteur.

### Correction V3.1 proposee

**Regle a enforcer dans la generation de fiche + dans `run_engine()` :**

```python
# V3.1 — Test de coherence SOM / Forecast
som_solo_monthly = som_solo_y1_annual / 12
forecast_m12_mrr = forecast['months'][-1]['mrr']

ratio = forecast_m12_mrr / som_solo_monthly

if ratio > 5.0:
    # KILL automatique : forecast fantasme
    forecast_status = 'KILLED_INCOHERENT'
    # Retourner a la formule MOAT pure
    forecast_m12_mrr = som_solo_monthly
elif ratio > 3.0:
    # Flag + explication obligatoire
    forecast_status = 'FLAGGED_INCOHERENT'
    forecast_flags.append('forecast_incoherent')
    # Require justification field documentee dans la fiche
else:
    forecast_status = 'COHERENT'
```

**Seuils :**
- Ratio forecast M12 / SOM Solo mensuel ≤ 3× → OK
- Ratio entre 3× et 5× → flag `forecast_incoherent` + explication obligatoire (ex: viral loop, partenariat B2B, driver exceptionnel)
- Ratio > 5× → KILL du forecast, retour a SOM Solo pur

**Impact fiche :**
- Afficher le ratio dans le rapport final : "Forecast M12 = 2.1× SOM Solo (coherent)"
- Si flag actif, afficher en rouge dans le dashboard

---

## Bloc B — Ajouts retenus V3.1 (post-arbitrage Opus + validation Sonnet)

### B5 — Typologie timing_type (fenetre d'opportunite)

MOAT score l'opportunite a t=0 mais ne mesure pas la **durabilite de la fenetre**. Ajouter un champ `timing_type` sur chaque app :

| Type | Nature | Fenetre | Exemples |
|------|--------|---------|----------|
| **Type 1** | Driver reglementaire | 3-5 ans | TimeToInvoice |
| **Type 2** | Pathologie chronique | Permanente mais saturable | SleepCoach FR, SoulageR, ProcheSoin |
| **Type 3** | Trend culturel | 6-18 mois | ShadowWork FR, DecidR, ZenColere |

**Regle d'arbitrage :**
- Scores V3 equivalents (+/-5 pts) → prioriser Type 1 > Type 2 > Type 3
- Type 3 score > Type 2 score + 10 pts → arbitrage au cas par cas, documente

**Implementation** : champ enum obligatoire `timing_type` dans fiche + Airtable.

### B6.1 — Readiness gating binaire

MOAT confond aujourd'hui 2 dimensions :
- "L'opportunite est-elle bonne ?" → Score V3
- "Peux-tu la lancer maintenant ?" → Readiness

SleepCoach FR a 85 "avec partenaire psy" = opportunite bonne **MAIS** readiness = 0 tant qu'aucun clinicien n'est signe. **PEPITE fantome.**

**Regle V3.1 (version light) :**
```python
def check_readiness_gating(app: App) -> Decision:
    blockers_active = any([
        app.has_flag('partner_medical') and not app.partner_confirmed,
        app.has_flag('rgpd_sante') and not app.dpia_signed,
        app.has_flag('market_education') and not app.education_validated,
        app.has_flag('regulatory_risk') and not app.legal_clearance,
    ])
    
    if app.score_v3 >= 80 and blockers_active:
        return 'B — Validate'  # force, meme si score eligible A
    elif app.score_v3 >= 80:
        return 'A — Build now'
    else:
        return 'B — Validate'
```

**Impact** : resout 90% du probleme PEPITE fantome sans design complexe. Le calcul 0-100% auto (B6.2) = V3.2.

### B7 — Fraicheur data_freshness_date

Les scores se degradent avec le temps. Un score de novembre 2025 peut etre obsolete en avril 2026 (nouveau concurrent, changement trend, evolution reglementaire).

**Regle V3.1 :**
- Champ `data_freshness_date` obligatoire sur chaque scoring
- Si `today - data_freshness_date > 90 jours` au moment d'une decision `A — Build now` → **force re-audit prealable** avant tout commit

**Implementation** : champ date + check dans `validate_for_build_decision()`.

## Plan d'implementation V3.1

### Etape 1 — Modifier `scripts/moat_engine.py`
- Ajouter constante `MICRO_VOLUME_THRESHOLD = 50`
- Ajouter constante `FORECAST_COHERENCE_FLAG = 3.0`, `FORECAST_COHERENCE_KILL = 5.0`
- Ajouter parametre CLI `--trend-index-avg`
- Ajouter parametre CLI `--geo-target`
- Ajouter fonction `validate_trend_geographic()`
- Ajouter fonction `validate_forecast_coherence()`
- Ajouter fonction `validate_geographic_consistency_tam_trend_som()`
- Ajouter fonction `generate_score_audit_trail()` + validation delta traces

### Etape 2 — Modifier le template fiche
- Ajouter section "Coherence check" automatique
- Afficher ratio forecast/SOM
- Afficher warning si flag actif
- **Ajouter section "Score Audit Trail" obligatoire** : chaque delta entre base et V3 trace et sourced

### Etape 3 — Audit flash retroactif (realise 2026-04-19)
Scan du top 17 effectue. 5 apps flaggees `[AUDIT V3.1 PENDING]` dans Airtable :

| App | Ratio forecast/SOM Solo | Verdict V3.1 | Action |
|-----|-------------------------|--------------|--------|
| DecidR | **10.7x** | KILL forecast | Re-score complet V3.1 obligatoire |
| NutriZen | **8.0x** | KILL forecast | Re-score complet V3.1 obligatoire |
| SocialEase | **5.8x** | KILL forecast | Re-score complet V3.1 obligatoire |
| SoulageR | 4.5x | FLAG + explication | Re-score V3.1 |
| SleepCoach FR | 4.3x | FLAG + explication | Re-score V3.1 |
| ShadowWork FR | Corrige | COHERENT | Deja re-score (70/100) |

Apps surement coherentes (pas de flag) :
- TimeToInvoice (Solo Dev Y1 5K/mois explicite)
- ZenColere (Solo Dev Y1 4.2K/mois explicite)
- PatientFlow (SOM 4.8K/mois raisonnable)

Apps a auditer au sprint V3.1 (non flaggees mais a verifier) :
- Devis Express (SOM 31.2K/mois)
- NutriSimple (SOM 90K/mois suspect)
- FocusFlow (SOM 36K/mois)
- AlzCompanion, BookMe, MemoContext, ProCompta, ProCheSoin

### Etape 4 — Documenter dans README et MOAT_PLAYBOOK
Ajouter une section "Regles V3.1" avec les 2 corrections et exemples.

### Etape 4 — Documenter dans README et MOAT_PLAYBOOK
Ajouter une section "Regles V3.1" avec les 2 corrections et exemples.

---

## Lessons learned

1. **Ne jamais appliquer un trend multiplier sur un marche dont le volume absolu est faible** — le % de variation est un artefact mathematique quand la base est proche de zero.
2. **Toujours cross-checker SOM Solo Dev Y1 et Forecast MRR M12** — un ratio > 3× est un signal rouge qui doit declencher une verification explicite.
3. **Cross-review systematique avant toute decision A — Build** — deux cerveaux qui se challengent sur donnees convergent vers la verite la plus honnete, pas la plus flatteuse.
4. **Un asset non valide reste une hypothese** — personal_fit doit refleter des donnees, pas des intentions.

## Regle #8 projet — Cross-review Opus↔Sonnet (formalisation)

**Declencheurs** (cross-review obligatoire AVANT commit en A — Build now) :
1. Score V3 >= 75 (pas 80 : catch les apps a la marge avant qu'elles remontent post-validation)
2. Driver structurel +8 applique (verification obligation legale vs tailwind)
3. Flag retire (market_education, partner_medical, rgpd_sante) — leviers d'inflation haute
4. Trend multiplier > 1.00 (verification geographique cible)

**Exclusion** : re-scoring automatique post-patch V3.1 si le moteur enforce deja les garde-fous.

**Cout** : ~30 minutes d'echange.
**Benefice demontre (2026-04-19)** :
- ShadowWork FR 89 → 70 (8-10 semaines economisees sur mauvaise app)
- SleepCoach FR 100 → 70 (risque legal partner_medical evite)
- DecidR 85 → 78 (Faille #1 V3.1 detectee en live)
- NutriZen 80 → 73 (Bodyguard zone grise)
- SocialEase 82 → 63 (2 flags oublies)

## Apps a valider au sprint V3.1 (Sonnet's flagged watchlist)

Apps declarees "coherentes" par Opus au audit flash, mais a verifier :
- **TimeToInvoice** (5K/mois) : etalon unique valide sans reserve. Re-scorer en premier comme test de non-regression.
- **ZenColere** (4.2K/mois) : verifier positionnement. Si "anger management therapeutique" → flag rgpd + partner_medical. Si lifestyle behavioral → OK.
- **PatientFlow** (4.8K/mois) : si B2B pro sante, verifier pricing ARPU B2B (~15-30€/mois) pas freemium B2C.

## Sequencement V3.1 (ordre non-negociable)

1. Patch `moat_engine.py` avec les **7 regles V3.1** (A1-A4 + B5 + B6.1 + B7)
2. **Test non-regression** : re-score TimeToInvoice + ZenColere + PatientFlow. Si TimeToInvoice bouge → bug dans les regles.
3. Re-score complet pipeline avec V3.1 (SoulageR, Devis Express, NutriSimple, FocusFlow, AlzCompanion, BookMe, MemoContext, ProCompta, ProcheSoin)
4. Review Olivier avant tout nouveau build
5. Mise a jour README + MOAT_PLAYBOOK

## Backlog consolide (post-V3.1)

| Sprint | Items | Focus | Fenetre |
|--------|-------|-------|---------|
| **V3.1** (actuel) | A1-A4 + B5 + B6.1 + B7 | Correctifs moteur critiques | Sprint actuel |
| **V3.2** | B6.2 (readiness 0-100% calcul auto) | Sophistication moteur | Apres re-audit pipeline V3.1 |
| **Sprint Template Refactor** (parallele V3.2) | B8 (journal hypotheses + retro-fill) | Process gouvernance | Peut tourner en parallele V3.2 |
| **V3.3** | C10 (marches satures) + C11 (dependance externe) | Raffinements bodyguard | Post-V3.2 |
| **V4** | C9 (post-mortems apps lancees) | Calibration terrain | 2027 (besoin >=3 apps lancees) |

## Patterns emergents post-Phase 2 (backlog V3.2 enrichi)

Le sprint V3.1 a revele 3 patterns structurels qui devraient etre codifies au moteur V3.2 :

### B9 — Subscore obsolescence detection
**Probleme** : A4 catche les deltas fantomes post-calcul, mais pas les subscores obsoletes. Quand la concurrence evolue (nouveau leader, changement reglementaire), les subscores competition_gap et mvp_speed changent silencieusement.

**Exemples detectes** :
- TimeToInvoice : stored 100 avec subscores base 79 (82 historique = plus applicable)
- ZenColere : stored 82 UP appliquee mais arithmetique seulement coherente avec STABLE
- Devis Express : base 75 valide historiquement mais Artinove/Tiime/Pennylane ont change le gap (3→2)
- Nutrition apps : marche sature (Yazio/MFP) pas reflete dans subscores initial

**Regle V3.2 B9 proposee** :
```python
# V3.2 — Subscore obsolescence guard
if data_freshness_date > 90_days_ago AND market_context_changed == True:
    force_rescoring_9_criteria()  # pas juste re-application deltas V3
```

Cron mensuel optionnel : detection automatique nouveaux concurrents Play Store/App Store dans la categorie de l'app → flag `market_context_changed = true`.

### B10 — POSITIONING_DECISION_REQUIRED comme flag moteur
**Probleme** : plusieurs apps ne peuvent pas etre scorees definitivement sans positionnement produit tranche. Actuellement gere ad hoc comme readiness_status.

**Exemples detectes dans ce sprint** :
- Devis Express : 3 scenarios (A devis seul / B devis+facture / C vertical BTP) = scores 70/79/85
- BookMe : 3 scenarios (generaliste / vertical non-sante / vertical sante) = scores 73/75/63
- FocusFlow : 2 scenarios (lifestyle / therapeutique) = scores 78/58

**Regle V3.2 B10 proposee** : flag `POSITIONING_DECISION_REQUIRED` comme flag de scoring a part entiere, pas juste readiness. Conditions de levee documentees (positionnement formel) + scenarios obligatoires avec subscores corriges par scenario.

### B11 (nouveau, post-FocusFlow) — Regulatory requalification risk
**Probleme** : meme si un app est positionnee "lifestyle", cibler une population diagnostiquee (TDAH, burnout, etc.) dans ASO/marketing peut declencher requalification par CNIL/ARS.

**Exemple** : Tiimo (app productivite TDAH DK) a du ajouter disclaimers medicaux sous pression UK.

**Regle V3.2 B11 proposee** : si la cible ASO mentionne un diagnostic medical, forcer flag `regulatory_requalification_risk` meme si positionnement est declare "lifestyle". Penalty -5 a -10 avec disclaimer fort + veille reglementaire requise.

### 3 patterns en 1 sprint = diagnostic structurel

Trois failles decouvertes dans un seul sprint V3.1. Signal fort que V3 avait des trous structurels significatifs. V3.2 devra integrer les 3 avant de considerer le moteur stabilise.

## Backlog V3.2 consolide (post-Phase 2)

| # | Item | Source | Priorite |
|---|------|--------|----------|
| B6.2 | Calcul readiness 0-100% auto | V3.1 scoping | P0 (moteur) |
| B9 | Subscore obsolescence detection | Phase 2 Devis Express/ZenColere | P0 (moteur) |
| B10 | POSITIONING_DECISION_REQUIRED flag formel | Phase 2 BookMe/FocusFlow | P1 (moteur) |
| B11 | Regulatory requalification risk | Phase 2 FocusFlow | P1 (moteur) |
| B8 | Journal hypotheses + retro-fill | V3.1 scoping | P1 (template) |

Sprint V3.2 moteur = B6.2 + B9 + B10 + B11.
Sprint Template Refactor parallele = B8.

## Reviewers
- Claude Opus Code (proposer + executor)
- Claude Sonnet (auditor + validator)

## Statut
- [x] Failles identifiees et documentees
- [x] Corrections proposees
- [ ] Code moteur modifie (`moat_engine.py`)
- [ ] Template fiche mis a jour
- [ ] Re-audit pipeline existant
- [ ] README / MOAT_PLAYBOOK mis a jour
