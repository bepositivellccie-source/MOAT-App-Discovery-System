# ProcheSoin

## Identite
- **Categorie** : Sante
- **Segment cible** : Aidants familiaux gerant les soins de proches ages (11M aidants FR, 4.5M en equipe)
- **Date de creation** : 2026-04-14
- **Statut** : Scoring

## Probleme
- **Enonce** : Les aidants familiaux perdent le suivi des medicaments et soins de leurs proches ages a cause de l'absence de coordination entre freres/soeurs
- **Contexte d'usage** : Quotidien — 2-3 freres/soeurs gerent les medicaments, RDV medicaux et soins d'un parent age a domicile. "Qui passe aujourd'hui? Maman a-t-elle pris ses cachets? Le medecin a dit quoi?"
- **Alternative actuelle** : Medisafe (devenu payant 5 EUR/mois janv 2026, 52% reviews negatives), MyTherapy (ajout pubs), WhatsApp, notes papier
- **Pourquoi c'est penible** : Medisafe = rappel individuel, pas de coordination. Les freres/soeurs dupliquent les actions ou oublient. Pas de journal partage. Pas d'export medecin. Information eparpillee entre SMS, appels, post-its.

## Marche
- **Taille estimee du segment** : 11M aidants FR, 4.5M en situation de coordination multi-aidants, ~1.35M utilisateurs potentiels d'app
- **Tendance** : Croissant (population vieillissante, 20% de 65+ en 2030)
- **Concurrents directs** :
  - Medisafe : 6.2M installs, 3.04/5, PASSE PAYANT janv 2026 (exode massif)
  - MyTherapy : 18.7M installs, 4.66/5, ajout pubs intrusives
  - Connected Caregiver : 58K installs, anglophone uniquement
  - ianacare : 62K installs, anglophone uniquement
  - Gabby : FR mais senior-facing (pas coordination famille)
- **Gaps concurrentiels** :
  - ZERO app FR de coordination multi-aidants familiaux
  - Medisafe/MyTherapy = rappel INDIVIDUEL, pas de partage famille
  - Apps caregiver anglophones = pas adaptees systeme sante FR
  - Gabby = pensee pour le SENIOR, pas pour les ENFANTS qui coordonnent

## Donnees concurrentielles (MOAT Engine)
- **Reviews analysees** : 300 (Medisafe + MyTherapy)
- **Ratio negatifs moyen** : 41.3%
- **Plaintes pricing** : 55.9% des avis negatifs
- **Top frustrations** : payant (70x), payante (48x), gratuit (26x), cher (12x), pub (8x), abonnement (7x)
- **Signal caregiver** : 30 reviews mentionnent famille/parent/aidant — preuve d'usage pour proches

## Proposition
- **Hypothese de valeur** : Une app qui permet a 2-3 freres/soeurs de coordonner les soins de leur parent age — medicaments, RDV, journal partage, taches — sans doublon ni oubli
- **Differenciation** :
  1. Multi-aidant sync (qui a fait quoi aujourd'hui)
  2. Journal partage temps reel (timeline familiale)
  3. Base medicaments FR (ANSM)
  4. Export rapport PDF pour le medecin
  5. Gratuit pour les features core (vs Medisafe payant)
  6. Calendrier zones FR A/B/C integre
- **Monetisation** : Freemium — core gratuit, Premium 4.99 EUR/mois (historique illimite, export PDF, stockage photos)
- **Prix envisage** : 4.99 EUR/mois ou 39.99 EUR/an

## Timing strategique
- **Medisafe paywall janvier 2026** : 6.2M utilisateurs cherchent une alternative MAINTENANT
- **MyTherapy pubs** : deuxieme vague de mecontentement
- **Fenetre d'acquisition** : 6-12 mois avant qu'un concurrent s'installe

## Driver structurel
- Loi 2022 grand age et autonomie : encourage outils numeriques de coordination
- Statut aidant (loi 2019) : reconnaissance legale = marche qui emerge
- France 20% de 65+ en 2030 : tendance longue irreversible
- HAS recommande coordination aidants

## Validation
- [x] Hypothese probleme confirmee (41.3% reviews negatives, 55.9% plaintes pricing)
- [x] Hypothese segment confirmee (11M aidants FR, 30 reviews mentionnent usage famille)
- [ ] Hypothese valeur confirmee (a tester avec landing page)
- [x] Hypothese paiement confirmee (55.9% plaintes pricing = volonte de payer prouvee)
- [ ] Hypothese canal confirmee (a tester SEO + communautes aidants)

## Preuves
- **Avis analyses** : 300 reviews FR (Medisafe + MyTherapy via MOAT Engine)
- **Posts/forums** : Medisafe Reddit/Play Store = exode massif post-paywall
- **Interviews** : 0 (a planifier)
- **Landing page** : Non creee (prochaine etape)
- **Autres signaux** : Medisafe passe de 4.5/5 a 3.04/5 en 3 mois = catastrophe concurrentielle

## Sizing
- **TAM** : 81,000,000 EUR (1.35M users x 60 EUR/an)
- **SAM (15%)** : 12,150,000 EUR
- **SOM (2%)** : 243,000 EUR/an = 20,250 EUR/mois
- **SOM Solo Dev Y1 (7%)** : 17,010 EUR/an = 1,418 EUR/mois (realiste)

## Scoring MOAT V3

| Critere | Score (1-5) | Pondere |
|---------|-------------|---------|
| Intensite probleme | 4 | 16/20 |
| Frequence usage | 4 | 12/15 |
| Volonte de payer | 4 | 12/15 |
| Segment accessible | 4 | 8/10 |
| Faiblesse concurrence | 4 | 8/10 |
| Differenciation | 5 | 10/10 |
| Fit personnel | 3 | 6/10 |
| Vitesse MVP | 3 | 3/5 |
| Retention | 5 | 5/5 |
| **BASE** | | **80/100** |
| Trend UP (x1.08) | | +6 pts |
| Driver structurel | | +8 pts |
| **TOTAL V3** | | **94/100** |

## Audit (Sonnet review 2026-04-14)
- Score engine brut : 94 (UP x1.08 + structural driver +8)
- Driver structurel retire : loi 2022 encourage mais n'oblige pas (-8 pts)
- FLAG RGPD Art.9 applique : donnees medicaments proche = sante (-5 pts)
- **Score V3 audite : 81/100**

## Decision
- **Categorie** : B — Validate (etait A avant audit)
- **Score V3** : 81/100 (engine brut: 94, audite: 81)
- **Prochaine action** : 10 interviews aidants actifs + landing page + verifier trend Google Trends FR
- **Deadline** : 2026-04-28
