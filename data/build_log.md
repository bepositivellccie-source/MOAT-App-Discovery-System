# MOAT Build Log

## 2026-04-14 — Session radar concurrentiel + deblocage SleepCoach

### Analyses realisees
- Radar concurrentiel pipeline complet : 11 changements concurrents identifies
  - Calm : +15% prix (69.99 -> 79.99 EUR/an)
  - Headspace : pivot B2C -> B2B (Headspace for Work)
  - Sleep Cycle : -14K abonnes/trim, churn accelere
  - Medisafe : paywall janv 2026, 3.04/5, exode massif
  - MyTherapy : ajout pubs intrusives
- Pattern exode primaire identifie : les apps pre-existantes capturent les utilisateurs en exode, pas les nouvelles apps. Fenetre = 6-12 mois post-exode pour construire avant que le marche se stabilise.
- Timing windows : toutes les fenetres sont LONGUES (12+ mois), pas d'urgence tactique

### SleepCoach FR — DEBLOQUE + RECALCULE
- Bloquant partenaire sommeil leve : protocole CBT-I public (HAS 2006, Morin & Espie)
- Score : 67 conditionnel -> 82 debloque -> **100 recalcule**
  - Base 90 (competition_gap corrige 4->5) x UP (1.08) = 97 + driver structurel (+8) = 105 -> cap 100
  - Driver structurel JUSTIFIE : feuille de route interministerielle + HAS 1ere intention + Mon Bilan Prevention
  - RGPD non applicable (journal sommeil = lifestyle, pas Art.9)
  - Audit : aucune deduction justifiable
- Decision : A — Build now
- Google Trends FR : insomnie UP confirme (1 FR sur 3 insomniaque, 45% troubles sommeil 2026 vs 38% 2024)
- Feuille de route gouvernementale sommeil 2025-2026 = driver structurel confirme
- Congres du Sommeil 2025 : session TCC-I numerique — la profession se tourne vers le digital
- Territoire Play Store FR CBT-I : VIERGE
  - Somna : 577 installs, dec 2025, anglophone traduit — invisible
  - KANOPEE : 141K installs, CHU Bordeaux, hygiene sommeil seulement (pas TCC-I complete)
  - HALEO : 21K installs, B2B only (employeur/assureur)
  - TherasomNIA : web only, 199 EUR, pas d'app
  - CBT-i Coach (VA) : anglais uniquement
- competition_gap releve a 5/5

### ProcheSoin — AUDITE
- Score engine brut 94 -> audite 81
- Driver structurel loi 2022 retire (-8 pts : encourage mais n'oblige pas)
- FLAG RGPD Art.9 donnees sante (-5 pts)
- Calcul final : base 80 x UP (1.08) = 86 - 5 = 81
- Decision : B — Validate
- Prochaine etape : 10 interviews aidants + landing page + trend
- Deadline : 2026-04-28

### Ordre de priorite post-recalcul
1. **TimeToInvoice** (100) — driver reglementaire e-facturation 2026-2027, execution immediate
2. **SleepCoach FR** (100) — ex-aequo TTI, territoire vierge + driver gouvernemental + base 90
3. **DecidR** (95) — score eleve mais necessite education marche
4. **ProcheSoin** (81) — potentiel fort, validation requise (interviews + RGPD)

### BurnoutDetect — DOUBLON NETTOYE
- Deux records du 13 avril : recs1ThdpvuO8ch8m (02:47) et recEWmjGS7vf49ZZ2 (02:52)
- Garde : recs1ThdpvuO8ch8m (probleme, canal, verified, 38 recherches)
- Supprime : recEWmjGS7vf49ZZ2 (marque DOUBLON/Killed/D-Kill)
- Notes fusionnees : FLAGS market_education + rgpd_sante + 2 blockers

### Airtable — Etat final
- SleepCoach FR (rec06iSJ96ekX4ENr) : Score V3 = 100, A — Build now, driver structurel confirme
- ProcheSoin (reclB19nR4wjKqlDs) : Score V3 = 81, B — Validate, audit detaille
- BurnoutDetect (recs1ThdpvuO8ch8m) : Score V3 = 82 conditionnel, B — Validate, notes fusionnees
- Doublons marques SUPPRIMER (suppression manuelle UI requise) :
  - ProcheSoin : recicbXCcykZkLfYL
  - BurnoutDetect : recEWmjGS7vf49ZZ2

---

## 2026-04-19 — Scan shadow work + ShadowWork FR

### Analyses realisees
- Scan complet thematique shadow work (Google Trends + 14 apps Play Store)
- Geo-scan 4 marchees : FR, US, UK, DE
- Trend FR **+692% sur 12 mois** (sur volume faible mais explosion reelle)
- Trend US +61%, UK +30%, DE +180%
- Analyse 14 apps dediees shadow work : 660K installs cumules top 5
- Leader : Prompted Journal (Plum Studio) 474K installs / 4.61 etoiles
- Territoire Play Store FR + App Store FR : **VIERGE** (reviews 1 etoile explicites)

### ShadowWork FR — CREE
- Score V3 : **89/100** (base 82 x UP 1.08 = 89)
- Rang : PEPITE
- Decision : A — Build now
- Marketplace prioritaire : **App Store iOS FR** (ARPU premium 2-3x)
- Play Store FR en parallele (meme MVP Flutter cross-platform)
- Asset cle : **site FR existant** = canal acquisition deja actif
- Pas de driver structurel (tendance culturelle, pas reglementaire) — honnete
- Pas de FLAG RGPD (journal lifestyle pas Art.9)
- Pas de FLAG partner_medical (positionnement self-reflection, pas therapie)
- TAM francophonie : 24.6M EUR (82M francophones)
- SOM Solo Dev Y1 : 2.87K EUR/mois
- Prochaine etape : analyser audience site + landing test + 10 interviews

### Airtable + Dashboard
- Airtable : recD6RiiPoxVjx9kc cree
- Dashboard : BUILD_SHEET ajoute apres ProcheSoin
- Fiche : `data/opportunities/2026-04-19_shadowwork_fr.md`

### Classement pipeline mis a jour
1. **TimeToInvoice** (100) — driver reglementaire e-facturation
2. **SleepCoach FR** (100) — driver gouvernemental + territoire vierge
3. **DecidR** (95) — education marche requise
4. **BurnoutDetect** (82 cond.) — 2 blockers RGPD + psy
5. **ProcheSoin** (81) — validation en cours
6. **ShadowWork FR** (70 post-audit) — validation 3 conditions avant code

### AUDIT SONNET 2026-04-19 — ShadowWork FR
Score revise 89 → 70. Corrections :
- Trend STABLE (1.00) pas UP (1.08) : index FR 0, +692% artefact micro-volume
- Flag market_education -10 : terme anglais, comportement achat App Store non etabli
- personal_fit 4 → 3 : asset site est hypothese, pas donnee
- Conversion 1.5% pas 2.5% : coherent market_education
- Pricing 39 → 49 EUR/an : 18% discount standard premium
- Forecast realigne : M12 base = 1.4K€/mois (pas 27K)
- Decision : A — Build → B — Validate
- Rang : PEPITE → A explorer

Bloquants avant code : data site + landing test >3% + App Store search FR >100/mois.

### POST-MORTEM CROSS-REVIEW SONNET/OPUS — V3.1 identifiee
2 failles structurelles du moteur V3 decouvertes :
1. **Trend Multiplier mondial appliquable a un projet national** (documente : `scripts/MOAT_ENGINE_V3.1_POSTMORTEM.md`)
2. **SOM Solo Dev Y1 vs Forecast MRR sans coherence check** (documente : meme fichier)

Corrections V3.1 proposees :
- Enforcer trend geographique cible + guard sur micro-volume (<50/100 index moyen → STABLE par defaut)
- Enforcer ratio forecast/SOM Solo ≤ 3× (flag >3×, KILL >5×)
- Re-auditer pipeline existant avec nouvelles regles

Plafond post-validation ShadowWork FR = 80 (pas 89). Condition d'activation A-Build : 3 validations + aucune autre PEPITE dispo.

Lessons learned pour Opus : ne jamais appliquer trend multiplier sur micro-volume + valider asset avant scoring + coherence SOM/forecast obligatoire. Prochaine app du pipeline : appliquer V3.1 au moteur avant de scorer.

### AUDIT FLASH RETROACTIF V3.1 (ITEM 6)
Scan du top 17 (apps >= 80) pour detecter les biais identifies sur ShadowWork. Formule : SOM Solo Dev Y1 mensuel theorique = TAM × 0.0000175. Ratio forecast M12 base / SOM Solo theorique.

**5 apps flaggees [AUDIT V3.1 PENDING]** :

| App | TAM | Forecast M12 | SOM Solo theorique | Ratio | Verdict |
|-----|-----|--------------|---------------------|-------|---------|
| DecidR | 192M | 36K | 3.36K | **10.7x** | **KILL** |
| NutriZen | 600M | 84K | 10.5K | **8.0x** | **KILL** |
| SocialEase | 225M | 22.8K | 3.94K | **5.8x** | **KILL** |
| SoulageR | 720M | 57K | 12.6K | 4.5x | FLAG |
| SleepCoach FR | 1.2B | 89.7K | 21K | 4.3x | FLAG |

**Diagnostic systemique** : TAM affiche est souvent mondial alors que cible = FR. Ca gonfle mecaniquement SOM puis forecast. Solo dev fait rarement 50K+/mois solo, tous ces forecasts sont a re-auditer avec V3.1.

**Blocage pipeline** : aucune de ces 5 apps ne doit passer en Build avant re-scoring V3.1 complet. Si Olivier veut demarrer, seules TimeToInvoice (5K/mois explicite solo) + ZenColere (4.2K/mois explicite) + Devis Express (31K/mois, a verifier) sont surement "coherentes" dans leur forecast.

Apps non flaggees car forecast deja coherent avec Solo Dev :
- TimeToInvoice : Solo Dev Y1 5K/mois explicite
- ZenColere : Solo Dev Y1 4.2K/mois explicite
- PatientFlow : SOM 4.8K/mois (raisonnable)

Apps a re-verifier :
- Devis Express (SOM 31.2K/mois — TAM ?)
- BookMe (SOM 12K/mois — probablement OK)
- NutriSimple (SOM 90K/mois — suspect probable)
- FocusFlow (SOM 36K/mois — a verifier)
- AlzCompanion (SOM ? — a verifier)
- BurnoutDetect (flag deja applique)
- ProcheSoin (SOM 20.2K/mois — a verifier post-audit 81)
- MemoContext (SOM ? — a verifier)
- ProCompta (SOM ? — a verifier)

Prochain sprint V3.1 : re-score complet du pipeline avec regles geographic + coherence ratio.

### AUDIT SONNET V3.1 - PHASE 2 (apps suspectes re-scorees)

Sonnet a pousse plus loin que l'audit flash Opus. 3 erreurs structurelles supplementaires detectees :

#### SleepCoach FR : 100 -> 70 (sans psy) / 85 (avec psy)
3 erreurs cumulatives de ma part :
1. Driver structurel +8 contestable : feuille de route + HAS = tailwind culturel, pas obligation legale (seul TimeToInvoice a un vrai driver au sens MOAT)
2. Trend UP non source sur donnees FR. Verification trend_radar.py confirme : insomnie FR = STABLE +3.4% (pas UP). J'avais utilise articles de presse = prevalence, pas demande de recherche.
3. Flag partner_medical -15 doit etre retabli : protocole public != couverture responsabilite legale (risque suicide insomnie severe + comorbidites documentes).
+ Flag rgpd_sante -5 : ISI = questionnaire clinique valide, Art.9.
Calcul : 90 x STABLE - 5 - 15 = 70 sans psy, 85 avec psy.
Historique scoring : 67 (correct) -> 82 (erreur deblocage) -> 100 (erreur cumulative) -> 70 (verite post-audit).

#### SocialEase : 82 -> 63 (sans psy) / 78 (avec psy)
2 flags que j'ai completement OUBLIES :
1. partner_medical -15 : TCC anxiete sociale = intervention clinique (comme ZenColere/BurnoutDetect)
2. rgpd_sante -5 : journal pensees anxieuses = Art.9
Lesson : toute app Sante mentale + TCC -> partner_medical par defaut dans V3.1.

#### DecidR : 85 -> 78
Faille #1 V3.1 en action : calcul d'origine 88 x UP (1.08) - 10 (market_education) = 85. Le UP venait du trend monde, pas FR. J'ai reproduit la Faille #1 que je venais de documenter sur ShadowWork.
Correct : 88 x STABLE - 10 = 78 Prometteuse.

#### NutriZen : 80 -> 73
Scoring fantome +4 pts inexpliques (76 base -> 80 V3). Bodyguard zone grise (Yazio/MFP satisfaisants 55%+). Marche sature pas vierge. Ratio forecast 8x KILL. Decision : C - Watchlist (pas B - Validate).

### Pipeline reorganise post-audit V3.1

| # | App | Score avant | Score revise | Decision |
|---|-----|-------------|--------------|----------|
| 1 | TimeToInvoice | 100 | 100 (a confirmer) | A - Build now |
| 2 | SleepCoach FR (avec psy) | 100 | **85** | A - Build post-partenariat |
| 3 | DecidR | 85 | **78** | B - Validate (test LinkedIn) |
| 4 | SoulageR | 88 | **a re-auditer V3.1** | Validation pending |
| 5 | SocialEase (avec psy) | 82 | **78** | B - Validate (2 blockers) |
| 6 | NutriZen | 80 | **73** | **C - Watchlist** |
| 7 | ShadowWork FR | 89 | **70** | B - Validate |
| 8 | SleepCoach FR (sans psy) | 100 | **70** | B - Validate |
| 9 | SocialEase (sans psy) | 82 | **63** | B - Validate |

**INSIGHT STRATEGIQUE CLE** : aucune app en A - Build pur en dehors de TimeToInvoice. Toutes les autres ont des conditions de validation bloquantes. Le pipeline post-TimeToInvoice n'est pas aussi rempli qu'on le pensait.

Si Olivier veut coder apres TimeToInvoice, le meilleur choix honnete = **SleepCoach FR + partenariat clinicien prealable** (85). Effort commercial avant code, pas l'inverse.

### Lessons learned cumulatives Opus

1. Ne jamais appliquer trend multiplier sur micro-volume OU trend non-cible
2. Valider asset avant scoring
3. Coherence SOM/forecast obligatoire (ratio < 3x)
4. Categorie Sante mentale + TCC -> partner_medical par defaut
5. Driver structurel = obligation legale avec sanction, pas tailwind
6. Flag rgpd_sante = Art.9 si donnees medicales structurees (questionnaires cliniques, scores severite, pathologie)
7. Cross-review systematique sur fiches 80+ avant Build (proposer a Olivier pour formalisation)

### Prochain sprint V3.1 (obligatoire avant tout build)
- Patch `moat_engine.py` avec regle trend geographique + coherence ratio + defaut partner_medical sur Sante mentale
- Re-auditer SoulageR, Devis Express, NutriSimple, FocusFlow, AlzCompanion, BookMe, MemoContext, ProCompta, ProcheSoin
- Verifier coherence TimeToInvoice (normalement OK car driver reel FR)
- Review Olivier avant relance de tout code

---

## 2026-04-19 (soir) — V3.1 Phase 1 COMPLETE

### Patch moat_engine.py V3.1 applique
7 regles implementees :
- A1 : `validate_geographic_consistency_tam_trend_som()` - check TAM vs PIB national cible
- A2 : `validate_trend_geographic()` - force STABLE si index moyen cible <50/100
- A3 : `validate_forecast_coherence()` - ratio forecast/SOM Solo (FLAG >3x, KILL >5x)
- A4 : `validate_score_justification()` - BLOQUANT a l'ecriture si arithmetique mismatch
- B5 : `validate_timing_type()` - enum 1/2/3 obligatoire
- B6.1 : `check_readiness_gating()` - force B-Validate si blocker actif meme si score >=75
- B7 : `check_data_freshness()` - force re-audit si >90j et A-Build

Exception dediee : `MoatEngineValidationError`
CLI enrichi : `--geo-target`, `--trend-index-avg`, `--flags`, `--blockers-resolved`, `--timing-type`, `--forecast-m12-mrr`, `--data-freshness-date`

### Tests unitaires V3.1 : 7/7 PASS
- A1 : TAM 150B FR suspect, 1.2B FR OK
- A2 : index 20/100 force STABLE, index 77/100 respecte UP
- A3 : ratio 9.5x KILL, 3.5x FLAG, 1.7x COHERENT
- A4 : arithmetique mismatch raise ValidationError
- B5 : valid 1/2/3, invalid 4 raise
- B6.1 : blocker actif force B-Validate, blocker resolu laisse A-Build
- B7 : 120j + A-Build force re-audit, fresh OK

### Non-regression : TimeToInvoice V3 93 vs V3.1 93 = identique
- V3.1 detecte en plus : A3 flag forecast 4.76x (zone FLAG, pas KILL) - signal utile

### Reproduction audit SleepCoach FR
- Sans partenaire : **71/100** (target Sonnet 70, +/-1 pts)
- Avec partenaire : **86/100** (target Sonnet 85, +/-1 pts)

### Airtable schema V3.1 migre
5 nouveaux champs crees :
- `Score Justification V3.1` (multilineText) - A4 audit trail
- `Timing Type V3.1` (singleSelect 1/2/3) - B5
- `Data Freshness Date` (date ISO) - B7
- `Readiness Status V3.1` (singleSelect 8 options) - B6.1
- `Legacy V3` (checkbox) - migration tag

### Tag Legacy V3 applique sur 16 records
Tous les records avec score >=80 (incluant etalons et Sonnet-auditees) taggues :
- `Legacy V3 = TRUE`
- `Readiness Status = LEGACY_V3_PENDING`

Les records suivants resteront taggues jusqu'a re-audit Phase 2 :
- Etalons (validation par test non-regression) : TimeToInvoice, ZenColere, PatientFlow
- Sonnet-auditees (scoring revise, format A4 a re-ecrire) : SleepCoach FR, DecidR, NutriZen, SocialEase, ShadowWork FR
- Non-auditees (re-audit Phase 2) : SoulageR, Devis Express, NutriSimple, FocusFlow, BookMe, ProCompta, ProcheSoin, BurnoutDetect

### Phase 1 STOP
Prochaine etape : cross-review Sonnet du code avant Phase 2.

### Declaration etalons V3.1 (post test non-regression)
**TimeToInvoice / ZenColere / PatientFlow declares etalons V3.1 — REVOQUE.**

### Phase 2 COMPLETE (2026-04-19)

**16 apps re-auditees V3.1 avec audit trails A4 strict + cross-review Sonnet integrale.**

#### Scores revises (tous post-correction Sonnet)

| App | Avant | Apres V3.1 | Decision | Status |
|-----|-------|------------|----------|--------|
| TimeToInvoice | 100 | **87** | A — Build CLEAR | En build actif |
| DecidR | 85 | **78** | B — Validate | Test LinkedIn pending |
| Devis Express | 82 | **75** cond. (70/79/85) | B — Validate | POSITIONING_DECISION |
| ProcheSoin | 81 | **75** | B — Validate | DPIA pending |
| BookMe | 82 | **73** cond. (63/73/75) | B — Validate | POSITIONING_DECISION |
| NutriZen | 80 | **73** | C — Watchlist | Marche domine |
| NutriSimple | 80 | **74** | C — Watchlist | Marche domine |
| ProCompta | 84 | **74** | C — Watchlist | RC pro recommandee |
| SleepCoach FR | 100 | **70** (85 psy) | B — Validate | Partenaire pending |
| SoulageR | 88 | **70** (85 psy) | B — Validate | Partenaire pending |
| ShadowWork FR | 89 | **70** | B — Validate | 3 validations |
| PatientFlow | 82 | **67** | B — Validate | HDS+DPIA pending |
| BurnoutDetect | 82 cond. | **66** | B — Validate | 2 blockers |
| SocialEase | 82 | **63** | B — Validate | Partenaire+DPIA |
| ZenColere | 82 | **62** | B — Validate | Partenaire+DPIA |
| FocusFlow | 80 | **58** cond. (78 lifestyle) | B — Validate | POSITIONING_DECISION |

#### Insights strategiques majeurs

1. **TimeToInvoice seule app CLEAR A — Build** dans tout le pipeline V3.1. V3 donnait une illusion de pipeline riche avec plusieurs PEPITES.
2. **Le sprint V3.1 n'a pas cree ce probleme, il l'a revele.** Protocole validation pre-A-Build maintenant obligatoire.
3. **Cluster reglementaire TimeToInvoice + Devis Express scenario B/C** identifie (Sonnet). A penser comme gamme, pas silos.
4. **Pattern systemique sante mentale** : toutes les apps TCC FR (SleepCoach/SoulageR/SocialEase/ZenColere/FocusFlow/BurnoutDetect) ont le meme pattern partner_medical + rgpd_sante = unlock 85/76/78 conditionnel.
5. **3 patterns V3.2 emergents** : B9 (subscore obsolescence), B10 (POSITIONING_DECISION_REQUIRED flag formel), B11 (regulatory requalification risk).

#### Cross-review Sonnet/Opus — regle #8 validee

Cout demontre : ~30 min par app.
Benefice demontre : ShadowWork 89→70 (8-10 semaines evitees), SleepCoach 100→70 (risque legal evite), 5 autres apps nettoyees.

Formalise dans `MOAT_PLAYBOOK.md` section 12.

### Phase 3 — Documentation COMPLETE

- [x] `README.md` : section V3.1 Rules quick reference + CLI exhaustif + schema Airtable
- [x] `MOAT_PLAYBOOK.md` section 12 : Regle #8 Cross-review formalisee
- [x] `MOAT_PLAYBOOK.md` section 13 : Protocole validation systematique pre-A-Build
- [x] `scripts/MOAT_ENGINE_V3.1_POSTMORTEM.md` : backlog V3.2 enrichi (B9 + B10 + B11)
- [x] Build log : Phase 2 + 3 cloturees

### Decisions Olivier en attente (non-bloquantes)

1. Devis Express positionnement (A / B / C / Kill) — trancher post-TTI
2. SoulageR partenaire — contact existant ou demarche
3. BookMe positionnement (generaliste / vertical non-sante / vertical sante)
4. FocusFlow positionnement (lifestyle 78 / therapeutique 58)
5. Respir audit (en attente reponses 3 questions Sonnet)

### Prochain sprint

**V3.2 moteur** :
- B6.2 : Calcul readiness 0-100% auto
- B9 : Subscore obsolescence detection + cron market context
- B10 : POSITIONING_DECISION_REQUIRED flag formel
- B11 : Regulatory requalification risk

**Sprint Template Refactor (parallele)** :
- B8 : Journal hypotheses + retro-fill fiches

### Statistiques sprint V3.1

- Duree : ~1 journee de travail intensif (2026-04-19)
- Apps re-auditees : 16
- Cross-review Opus↔Sonnet : continue tout le sprint
- 3 failles V3 codifiees en V3.1
- 3 patterns V3.2 emergents documentes
- 5 nouveaux champs Airtable
- 7 regles moteur + 3 raffinements implementes et testes
- Non-regression TimeToInvoice : V3 93 == V3.1 93
- Lignes code moat_engine.py : +~400 (V3 a V3.1)

**Sprint V3.1 : formellement clos 2026-04-19.**

### REVOCATION ETALONS (post cross-review Sonnet)

Data integrity issues detectes sur TimeToInvoice et ZenColere :
- **TimeToInvoice** : subscores Airtable → base 79, mais score_v3 = 100 stocke. Math check : 79 x UP + driver = 93 ≠ 100. Note historique "base 86 + EXPLOSIVE + LOI" = coherent mais base 86 ≠ subscores actuels 79. **Delta fantome de +21 pts** (exactement le pattern A4 que V3.1 catch).
- **ZenColere** : subscores → base 82, score_v3 = 82. Match seulement si STABLE x1.00. Note dit "UP x1.08" mais arithmetique seulement coherente avec STABLE. Note fausse ou trend multiplier non applique.
- **PatientFlow** : positionnement B2B et pricing ARPU a verifier Phase 2.

**Aucun etalon V3.1 formellement confirme.** Phase 2 doit re-auditer :
- Les 8 apps non-auditees (SoulageR, Devis Express, NutriSimple, FocusFlow, BookMe, ProCompta, ProcheSoin, BurnoutDetect)
- Les 3 ex-etalons (TimeToInvoice, ZenColere, PatientFlow) — re-calibration A4 obligatoire
- = **11 apps total en Phase 2**

### Raffinements V3.1 ajoutes (post cross-review Sonnet)

1. **A2 MACRO_STABLE_GUARD** : force STABLE si volume >=50 ET variation abs <10%. Catch le pattern insomnie FR (77/100 + 3.4%).
2. **A4 regex stricte** : trend_multiplier doit matcher x1.00/x1.08/x1.15/x0.90 uniquement. Tolerance arithmetique = 0.
3. **B6.1 granularite** : BLOCKED_SINGLE (1 blocker) / BLOCKED_MULTIPLE (2) / BLOCKED_SEVERE (3+, reconsider Watchlist).

### Corrections Airtable (post cross-review Sonnet)

5 records Sonnet-auditees retaguees :
- Legacy V3 = FALSE
- Readiness Status reflete l'etat operationnel :
  - ShadowWork FR : AUDITED_V3_1_CROSS_REVIEW
  - NutriZen : AUDITED_V3_1_CROSS_REVIEW (C-Watchlist, pas de blocker)
  - SleepCoach FR : BLOCKED_BY_multiple (partner_medical + rgpd_sante)
  - DecidR : BLOCKED_BY_market_education
  - SocialEase : BLOCKED_BY_multiple (partner_medical + rgpd_sante)
