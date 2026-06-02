# ExpatRadar — Scoring MOAT Engine V3

## Identité
- **Catégorie** : Lifestyle / Safety community
- **Segment cible** : Expats et voyageurs francophones (FR + BE + CH + QC) en Amérique latine (Guatemala → Brésil)
- **Date de scoring** : 2026-05-01
- **Statut** : Scoring → Validation
- **Record Airtable** : recCEQqdupjNbaQKp

## Concept
App d'intelligence collective terrain, 3 couches superposées :
- 🔴 **Alertes scams/dangers temps réel** (géolocalisées, datées, validées communauté)
- 🟡 **Terrain naturel** (crocodiles, courants, risques locaux spécifiques)
- 🟢 **Bons plans vérifiés** (avocats immigration, médecins francophones, agents immo de confiance)

## Douleur fondatrice
Olivier (founder), expat français Panama 20 ans, a payé **2× trop cher sa résidence** faute de contact avocat de confiance francophone. Douleur vécue, vérifiée, chiffrée. Pattern documenté à grande échelle : Washington Post (mai 2025) sur "fake notario / immigration scams", AARP, Iberian America.

---

## 1. Recherche concurrentielle Play Store

| App | Note | Avis | Segment réel | Verdict |
|-----|------|------|---------------|---------|
| **InterNations** | 4.4 | ~9 700 | Généraliste mondial 420 villes, freemium (Albatross 144-240 USD/an) | Events/networking, pas safety/alertes, **anglophone** |
| **Expat.com app** | 4★ | n/d | Forum mondial + classifieds, web dominant | Pas de couche safety/géoloc, navigation datée |
| **GeoSure** | n/d | n/d | Safety scoring 400k POI, IA (39,99 USD/an) | Anglophone, B2B/voyageur, pas communautaire, scores critiqués |
| **Citizen** | 5M+ users | — | Alertes safety hyperlocale | **US-only**, absent LATAM |
| **Nextdoor** | — | — | Communauté quartier | US/UK/AU/EU partiel, **absent LATAM** |
| **lepetitjournal.com** | — | — | Média 2,5M lecteurs FR (77 villes) | **Pas d'app mobile** = trou structurel |

**Conclusion concurrentielle** : aucun acteur ne combine les 3 couches pour francophones LATAM. Espace structurellement délaissé en mobile.

## 2. Google Trends signal

Recherche directe Trends FR pour "expat panama / vivre au panama / sécurité voyage amérique latine" : volume estimé **micro-volume** (<50/100) sur target francophone.

Signal indirect très fort :
- **Panama #1 mondial** Expat Insider 2025-2026 (94% expats satisfaits, record mondial)
- **Colombie #2** (en gain de 3 places)
- **Mexique #3** (top 3 mondial complet)
- Couverture média 2025-2026 explosive (Expat Insider, lesfrancais.press, lepetitjournal)

**Verdict trend** : **STABLE forcé** (A2 micro-volume guard sur target FR). Vague porteuse macro mais volume Trends FR insuffisant pour multiplier.

---

## 3. Scoring V3 — 9 critères

| # | Critère | Poids | Note | Pondéré | Justification |
|---|---------|-------|------|---------|---------------|
| 1 | **Pain Intensity** | ×4 | **4/5** | 16/20 | Arnaques avocats/notarios documentées (WashPost 05/2025), burundanga Colombie, scams immo Panama. Pain réel, chiffré (1500-4000$ surfacturé/résidence). Olivier = preuve vécue. Pas vital (5/5) mais douloureux. |
| 2 | **Frequency** | ×3 | **3/5** | 9/15 | Alertes safety = quotidien-hebdo. Bons plans = mensuel-ponctuel. Phase intensive arrivée (3-12 mois) puis ponctuel. Hebdomadaire moyenne. |
| 3 | **Will Pay** | ×3 | **3/5** | 9/15 | Capacité confirmée : Chapka 60-250€/mois, GeoSure 40$/an, InterNations 144-240$/an, concierge expat 500-2000€/an. MAIS habituation gratuit (Facebook, lepetitjournal, WhatsApp). Conversion B2C app sociale faible. |
| 4 | **Market Access** | ×2 | **3/5** | 6/10 | Hubs identifiables : Mexico (~15k FR), São Paulo (~10k), Buenos Aires (~8k), Medellín+Bogotá (~5k). Communautés Facebook 40-60k cumulés. LePetitJournal canal. **Mais fragmentation forte** : 22k/pays moyenne, Panama City ~2k seulement. |
| 5 | **Competition Gap** | ×2 | **4/5** | 8/10 | 0 app FR LATAM combinant 3 couches. InterNations + GeoSure couvrent partiellement, anglo. LePetitJournal sans app. Citizen/Nextdoor US-only. Trou clair. |
| 6 | **Differentiation** | ×2 | **4/5** | 8/10 | Multi-couches (alertes + terrain + bons plans) = unique. Focus francophone = unique. Réseau founder 20 ans = défendable. Couche "bons plans vérifiés FR" difficile à copier par généralistes. |
| 7 | **Personal Fit** | ×2 | **5/5** | 10/10 | Olivier 20 ans Panama, expat FR, douleur vécue (résidence 2× trop cher), réseau terrain existant, solo dev Flutter. Founder = utilisateur cible avec expertise terrain + skills tech. |
| 8 | **MVP Speed** | ×1 | **2/5** | 2/5 | App sociale UGC complexe : modération, géoloc, profils, signalements multi-couches. 3 couches contenu = ambitieux. Solo dev Flutter = **3-4 mois minimum** pour V1 fonctionnelle. |
| 9 | **Retention** | ×1 | **3/5** | 3/5 | Alertes safety = sticky si masse critique atteinte. Bons plans = retention faible si peu contenu. Network effect crucial. Cold start = risque #1. |
| | | | | **71/100** | **Score brut V3** |

---

## 4. Application formule V3 (révisé post Sonnet contre-analyse 2026-05-01)

```
base: 77
+ trend_multiplier: x1.00 (+0 pts)
+ driver_structurel: +0
+ flags: [aucun]
= score_v3: 77
```

**Révision post Sonnet — 61 → 77 (+16 pts)** :
- **Will Pay 3→4** (+3) : B2B data licensing (Chapka, AXA Travel, agences aventure type Tirawa/66 Nord) intégré au revenue stream, pas seulement B2C freemium
- **Market Access 3→4** (+2) : segment élargi aux voyageurs francophones longue durée (nomades digitaux FR + backpackers + expats LATAM) — ~440k au lieu de 220k, sans diluer le founder fit
- **Retention 3→4** (+1) : founder-seeded content (200 fiches Olivier Panama) donne valeur Day 1 sur 2 couches sur 3 (bons plans + terrain), pattern Reddit/Product Hunt
- **Flag `market_education` retiré** (+10) : sur révision stricte de la définition du flag (*"Behavior doesn't exist yet, needs education"*), le comportement existe **déjà** — groupes FB FR LATAM 40-60k cumulés brassent activement scams/bons plans/alertes. C'est de la **substitution d'outil**, pas de l'éducation marché. Friction adoption (FB→app) reste réelle mais n'est pas un flag MOAT formel.

**Détails contextuels** :
- **Trend STABLE forcé** (A2 micro-volume guard, geo=GLOBAL francophone, index_avg < 50/100) — pas de multiplier malgré dynamique macro positive (Panama #1 Expat Insider 2026)
- **Pas de driver structurel** (aucune obligation légale/réglementaire ne crée la demande, c'est un trend culturel post-COVID)

## 5. FLAGS V3.1 — Vérification structurelle

| Flag | Statut | Détail |
|------|--------|--------|
| `market_education` | ✅ ACTIF (-10) | Marché ne cherche pas activement une app dédiée |
| `network_effect` | ⚠️ STRUCTUREL (non pénalisé moteur) | App sociale → masse critique requise par pays. Hubs viables : Mexico (~15k), São Paulo (~10k), pas Panama City (2k). |
| `content_dependency` | ⚠️ STRUCTUREL (non pénalisé moteur) | 3 couches de contenu UGC = besoin de signalements actifs et bons plans vérifiés. App vide = inutile. |
| `regulatory_risk` | ⚠️ NOTÉ (non pénalisé) | Modération UGC + diffamation sur signalements d'arnaques = défi opérationnel + juridique (CGU robustes, modération scalable, droit local LATAM). Pas blocker légal majeur (pas RGPD santé), mais à anticiper. |
| `rgpd_sante` | ❌ N/A | Pas de données santé |
| `partner_medical` | ❌ N/A | Pas de domaine clinique |

**Risques structurels non capturés par le moteur** :
- **Fragmentation** : 220k francophones répartis sur 10 pays, hub max ~15k = sous le seuil de masse critique d'app sociale (~50k)
- **Cold start massif** : 3 couches × N pays = effort contenu démesuré pour solo dev

---

## 6. SOM Solo Dev Y1

### TAM/SAM/SOM
- **Segment** : 220 000 francophones (FR+BE+CH+QC) en Amérique latine, hors registre consulaire = ~260k réel
- **ARPU théorique** : 30€/an (freemium → premium concierge)
- **TAM** : 220 000 × 30 = **6 600 000 €**
- **SAM (15% atteignable)** : **990 000 €**
- **SOM (2% capture Y1)** : **19 800 €**
- **SOM mensuel** : **1 650 €/mois**

### Solo Dev Y1 réaliste (×7%)
- **SOM Solo Dev Y1** : 19 800 × 0.07 = **1 386 €/an = 115 €/mois**

### Sensibilités B2C
| Scénario | ARPU | Capture | SOM/mois | Solo Dev/mois |
|----------|------|---------|----------|---------------|
| Pessimiste | 24€/an | 1.5% | 990€ | 70€ |
| **Réaliste B2C** | **30€/an** | **2%** | **1 650€** | **115€** |
| Optimiste B2C | 60€/an | 3% | 4 950€ | 347€ |

### Revenue B2B Y2+ (révisé post Sonnet)
- **1 contrat data licensing** (Chapka, AXA Travel, ou agence aventure) : 5-10k€/an = 400-833€/mois
- **2-3 contrats Y3** : 1 200-2 500€/mois
- Cycle commercial 6-12 mois, pas Y1 réaliste

### SOM total Y1+Y2 réaliste
- **Y1 (B2C only)** : 115-230€/mois
- **Y2 (B2C scale + 1 deal B2B)** : **500-1 050€/mois**
- **Y3 (B2C + 2-3 B2B + extension multi-pays)** : 1 500-3 000€/mois

**Verdict marché** : **VIABLE** en hybride B2C+B2B Y2+. Path viable = V1 Panama mono-pays + pivot rapide vers data licensing dès traction B2C confirmée.

---

## 7. Verdict final (révisé)

### Score
- **Score V3 : 77/100** (révisé de 61, post Sonnet contre-analyse)
- **Confidence : 70%** (data Play Store partielle, signaux indirects forts, founder fit unique)

### Rang
**Prometteuse** (révision : douleur réelle + gap concurrentiel + founder fit 5/5 + cold start mitigé par seed content founder + monétisation B2C+B2B viable)

### Decision
**A — Build now** (conditionnel : test WhatsApp 0€ 3 semaines)

### Test pré-build obligatoire (intégration angle 5 Sonnet)
**Test WhatsApp groupe "Expats Panama — Bons plans & Alertes"** :
- 30 personnes du réseau Olivier (Panama focus)
- Olivier anime 3 semaines
- Coût : **0€** (vs 200€ landing page)
- KPI : si **<80% messages d'Olivier** = UGC validé → GO build V1 mono-pays Panama
- KPI : si **>80% messages d'Olivier** = UGC ne tient pas → pivot ou C-Watchlist

### Conditions de build V1 (post test WhatsApp +)
1. **V1 Panama uniquement** avec 200 fiches founder-seedées (avocats vérifiés, médecins FR, zones dangereuses)
2. **Extension géographique progressive** : Mexico City puis Medellín/Bogotá (hubs francophones les plus denses)
3. **Modération UGC** : CGU + workflow signalements + workflow diffamation
4. **Monétisation hybride** : freemium B2C (premium 5-10€/mois) + 1 contrat B2B data licensing Y2 (Chapka ou agence aventure)

---

## 8. Position dans le pipeline (41 apps) — RÉVISÉE

| Score V3 | App | Statut |
|----------|-----|--------|
| 100 | ChronoFacture | Build (en cours) |
| 95 | DecidR | Build sheet prête |
| 89→70 | ShadowWork FR | Cross-review révisé |
| 86 | AlzCompanion (V3 conditionnel) | Validation |
| 85 | Apaise (V3 conditionnel) | Validation |
| 78 | MemoContext | Build sheet |
| **77** | **ExpatRadar (révisé)** | **A-Build conditionnel test WhatsApp** |
| 74 | Agenda Kine | Validation |
| 49-58 | Watchlist apps | C — Watchlist |
| <45 | Killed apps | D — Kill |

**Position révisée : ~6-8e / 41** (top 20% du pipeline, vs 28-30e initialement)

---

## 9. Note stratégique solo dev (révisée post Sonnet)

**Pourquoi A-Build conditionnel maintenant ?**
1. Score révisé 77/100 ≥ 75 (zone A formelle)
2. Founder fit 5/5 unique (20 ans Panama + réseau actif)
3. Cold start mitigé : seed founder sur 2 couches/3 (bons plans + terrain), Day 1 value sans masse critique
4. Substitution d'outil (FB→app), pas market_education — comportement existe déjà
5. Monétisation hybride B2C+B2B viable (Chapka, agences aventure paient pour data terrain)
6. Test WhatsApp 0€ comme garde-fou pré-build

**Risques résiduels (non flag formels mais à monitorer)** :
- **Fragmentation** : reste un défi sur extension multi-pays Y2+. Pivot V1 mono-pays Panama l'évite Y1.
- **Couche alertes UGC** : seule la couche 🔴 reste dépendante de masse critique. Acceptable car bons plans + terrain donnent déjà de la valeur.
- **Modération diffamation** : CGU + workflow signalements + véracité requis dès V1.
- **Cycle B2B** : 6-12 mois, pas Y1. SOM Y1 reste B2C-dominant.

**Garde-fou avant code** : test WhatsApp 30 personnes Panama, 3 semaines, 0€. KPI binaire (<80% messages d'Olivier = UGC validé). Ce test est **plus puissant qu'une landing page** (signal comportemental réel vs intention déclarée) et **moins coûteux** (0€ vs 200€).

**Si test +** : build V1 Panama mono-pays avec 200 fiches founder-seedées. ETA 12-16 semaines solo dev Flutter.
**Si test —** : retour en C-Watchlist, pivot à étudier (B2B-first ? service concierge non-app ?).

---

## Sources

- [MEAE Carte registre consulaire 2025](https://webapps.france-diplomatie.info/carte-registre/)
- [Panama #1 Expat Insider 2025-2026](https://lesfrancais.press/le-panama-premiere-destination-mondiale-pour-expatriation-en-2026/)
- [Washington Post — fake immigration scams 05/2025](https://www.washingtonpost.com/technology/2025/05/10/immigration-scams/)
- [Iberian America — Scamming Gringo LATAM](https://iberianamerica.com/2022/01/30/the-scamming-gringo-of-latin-america/)
- [Common scams Panama - Expat.com](https://www.expat.com/en/forum/central-america/panama/1099862-most-common-scams-targeting-expats-in-panama.html)
- [InterNations Trustpilot](https://www.trustpilot.com/review/internations.org)
- [Chapka assurance expat](https://assurances-expat.fr/assureurs/chapka/)
- [GeoSure travel safety](https://www.travelandtourworld.com/news/article/geosure-launches-ai-powered-safety-tool-for-travelers-across-europe-america-asia-and-beyond-everything-you-need-to-know/)
- [Groupe FB Français au Panama](https://www.facebook.com/groups/francaisaupanama/)
- [LePetitJournal.com](https://lepetitjournal.com)
