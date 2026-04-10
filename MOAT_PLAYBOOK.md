# MOAT App Discovery System — Playbook Operationnel

> **Objectif** : Transformer des signaux de marche en decisions rationnelles pour lancer des apps Flutter rentables.
> **Principe** : On ne cherche pas "la meilleure idee", mais la meilleure asymetrie exploitable pour toi, maintenant.

---

## 1. Pipeline en 5 couches

```
SOURCING → QUALIFICATION → SCORING → VALIDATION → DECISION
  (signaux)    (problemes)    (notes)    (preuves)     (go/kill)
```

### Regle d'or
Une idee ne passe a l'etape suivante que si elle survit a l'etape courante.
Pas de raccourci. Pas de "on verra bien".

---

## 2. Sourcing — Capter les signaux

### Sources hebdomadaires obligatoires

| Source | Quoi chercher | Frequence |
|--------|--------------|-----------|
| Google Play / App Store reviews (1-3 etoiles) | Frustrations repetees, mots-cles recurrents | Lundi |
| Reddit (r/smallbusiness, r/SaaS, r/productivity, niches) | Problemes exprimes, bricolages, demandes d'outils | Lundi |
| Product Hunt | Nouveaux lancements, reactions, gaps | Lundi |
| Google Trends | Tendances montantes, saisonnalite | Lundi |
| Sensor Tower / data.ai (free tier) | Categories en croissance, top apps emergentes | Lundi |
| Communities Discord/Slack niches | Douleurs metier, workflows brises | Continu |

### Signaux forts a reperer

- **Douleur repetee** : le meme probleme revient dans 5+ avis differents
- **Bricolage visible** : les gens utilisent WhatsApp/Excel/Notion pour un besoin specifique
- **Segment ignore** : les apps existantes ciblent le grand public mais ratent un sous-segment
- **Paiement actif** : les gens paient deja pour une solution mediocre
- **Friction observable** : copier-coller, multi-outils, processus manuels

---

## 3. Qualification — Formuler le probleme

Chaque signal devient un probleme structure :

```
[SEGMENT] perd [QUOI] a cause de [POURQUOI]
```

**Exemples** :
- "Les kines respiratoires independants perdent 2h/semaine a gerer leurs exercices patients parce qu'ils utilisent WhatsApp + PDF."
- "Les micro-entrepreneurs francais oublient leurs echeances fiscales parce qu'aucune app ne les alerte avec le bon calendrier."
- "Les profs de yoga perdent des clients parce qu'ils n'ont pas d'outil simple de reservation + paiement."

### Criteres d'elimination immediate

Tuer l'idee si :
- Le probleme est vague ("les gens veulent mieux s'organiser")
- Pas de frequence (usage unique ou tres rare)
- Pas de douleur reelle (confort, pas necessite)
- Pas de monetisation visible
- Le segment est "tout le monde"

---

## 4. Matrice de Scoring — 100 points

| # | Critere | Poids | Score (1-5) | Formule |
|---|---------|-------|-------------|---------|
| 1 | Intensite du probleme | x4 | _ | score × 4 |
| 2 | Frequence d'usage | x3 | _ | score × 3 |
| 3 | Volonte de payer | x3 | _ | score × 3 |
| 4 | Taille du segment accessible | x2 | _ | score × 2 |
| 5 | Faiblesse concurrentielle | x2 | _ | score × 2 |
| 6 | Differenciation possible | x2 | _ | score × 2 |
| 7 | Fit personnel | x2 | _ | score × 2 |
| 8 | Vitesse de MVP | x1 | _ | score × 1 |
| 9 | Retention potentielle | x1 | _ | score × 1 |
| **TOTAL** | | **/100** | | |

### Seuils de decision

| Score | Decision |
|-------|----------|
| 75-100 | **A — Build now** : lancer la validation terrain |
| 60-74 | **B — Validate** : creuser les hypotheses |
| 45-59 | **C — Watchlist** : surveiller, pas d'action |
| 0-44 | **D — Kill** : archiver et oublier |

### Guide de notation (1-5)

**Intensite du probleme**
- 1 = Leger inconfort, on fait sans
- 2 = Genant mais supportable
- 3 = Probleme reel, solutions de contournement actives
- 4 = Douleur forte, perte de temps/argent mesurable
- 5 = Critique, les gens se plaignent activement et cherchent des solutions

**Frequence d'usage**
- 1 = Annuel
- 2 = Mensuel
- 3 = Hebdomadaire
- 4 = Plusieurs fois par semaine
- 5 = Quotidien

**Volonte de payer**
- 1 = Aucun signal de paiement
- 2 = Segment habitue au gratuit
- 3 = Certains paient pour des alternatives
- 4 = Budget existant dans le segment
- 5 = Paiement evident, depense deja active

**Taille du segment accessible**
- 1 = Tres niche (<1000 personnes atteignables)
- 2 = Petit mais identifiable
- 3 = Segment moyen, communautes existantes
- 4 = Large avec canaux d'acquisition clairs
- 5 = Tres large, SEO/ASO naturel

**Faiblesse concurrentielle**
- 1 = Marche domine par 2-3 excellents produits
- 2 = Forte concurrence, peu de gaps
- 3 = Concurrence correcte mais angles exploitables
- 4 = Apps mediocres, avis negatifs recurrents
- 5 = Quasi-aucune solution adequate

**Differenciation possible**
- 1 = Me-too, rien de different
- 2 = Legere amelioration
- 3 = Angle clair mais pas unique
- 4 = Avantage net sur 1-2 axes
- 5 = Approche fondamentalement differente

**Fit personnel**
- 1 = Domaine inconnu, pas de reseau
- 2 = Connaissance superficielle
- 3 = Comprends le domaine, peux builder
- 4 = Expertise ou reseau dans le segment
- 5 = Experience directe du probleme + skills techniques

**Vitesse de MVP**
- 1 = 6+ mois
- 2 = 3-6 mois
- 3 = 6-12 semaines
- 4 = 2-6 semaines
- 5 = 1-2 semaines

**Retention potentielle**
- 1 = Usage unique
- 2 = Quelques fois puis abandon probable
- 3 = Usage mensuel
- 4 = Usage hebdomadaire
- 5 = Usage quotidien, habitude forte

---

## 5. Fiche Opportunite — Template

```markdown
# [NOM DE L'IDEE]

## Identite
- **Categorie** : [ex: Productivite / Sante / Finance / Education / Metier]
- **Segment cible** : [ex: "Kines respiratoires independants francophones"]
- **Date de creation** : YYYY-MM-DD
- **Statut** : Backlog | Scoring | Validation | Ready to Build | Killed

## Probleme
- **Enonce** : [SEGMENT] perd [QUOI] a cause de [POURQUOI]
- **Contexte d'usage** : [Quand et ou le probleme survient]
- **Alternative actuelle** : [Ce que les gens font aujourd'hui]
- **Pourquoi c'est penible** : [Les frictions concretes]

## Marche
- **Taille estimee du segment** : [Nombre de personnes / entreprises]
- **Tendance** : [Croissant / Stable / Decroissant]
- **Concurrents directs** : [Liste avec liens]
- **Gaps concurrentiels** : [Ce que les concurrents font mal]

## Proposition
- **Hypothese de valeur** : [Ce que l'app fait mieux]
- **Differenciation** : [Pourquoi toi, pourquoi maintenant]
- **Monetisation** : [Freemium / Abo / Usage / One-time]
- **Prix envisage** : [X EUR/mois ou equivalent]

## Validation
- **Hypothese probleme** : [ ] Confirmee / [ ] A tester
- **Hypothese segment** : [ ] Confirmee / [ ] A tester
- **Hypothese valeur** : [ ] Confirmee / [ ] A tester
- **Hypothese paiement** : [ ] Confirmee / [ ] A tester
- **Hypothese canal** : [ ] Confirmee / [ ] A tester

## Preuves
- **Avis analyses** : [Nombre + themes]
- **Posts/forums** : [Liens]
- **Interviews** : [Nombre + insights]
- **Landing page** : [URL + metriques]
- **Autres signaux** : [...]

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
- **Categorie** : A / B / C / D
- **Prochaine action** : [...]
- **Deadline** : YYYY-MM-DD
```

---

## 6. Analyse Concurrentielle — Template

Pour chaque concurrent direct, remplir :

| Axe | Analyse |
|-----|---------|
| **App** | [Nom + lien store] |
| **Note store** | [X.X / 5 — N avis] |
| **Promesse** | [Ce qu'ils vendent en 1 phrase] |
| **Prix** | [Gratuit / Freemium / X EUR/mois] |
| **Forces** | [Ce qu'ils font bien] |
| **Faiblesses** | [Themes recurrents dans avis negatifs] |
| **UX** | [Simple / Correcte / Lourde] |
| **Segment reel** | [Pour qui c'est vraiment concu] |
| **Distribution** | [Comment ils acquierent] |
| **Moat** | [Ce qui les protege] |
| **Angle exploitable** | [Ce que tu ferais differemment] |

---

## 7. Workflow Hebdomadaire

### Lundi — COLLECTE (1-2h)

- [ ] Lire 15-20 avis concurrents (1-3 etoiles)
- [ ] Capturer 5 frustrations + mots-cles reels
- [ ] Scanner Reddit/Discord/forums (3 communautes min)
- [ ] Verifier Google Trends sur les themes actifs
- [ ] Ajouter les signaux bruts dans le backlog

### Mardi — FORMULATION (1h)

- [ ] Transformer chaque frustration en "[SEGMENT] perd [QUOI] a cause de [POURQUOI]"
- [ ] Ecrire l'hypothese segment + monetisation
- [ ] Eliminer les idees sans frequence, sans douleur ou sans paiement
- [ ] Mettre a jour le backlog

### Mercredi — SCORING (1h)

- [ ] Noter les nouvelles idees sur la matrice 100 points
- [ ] Comparer le top 5
- [ ] Identifier les faux positifs ("interessant mais flou")
- [ ] Mettre a jour les statuts (A/B/C/D)

### Jeudi — VALIDATION (2h)

- [ ] Creer une landing page simple (Carrd/Framer/Tally)
- [ ] Formuler une promesse unique
- [ ] Diffuser aupres de 20-50 personnes ciblees
- [ ] Mesurer : clics, reponses, inscriptions, objections

### Vendredi — DECISION (30min)

- [ ] **GO** si signaux concrets (inscriptions, reponses qualifiees, intent de paiement)
- [ ] **PAUSE** si probleme reel mais ciblage a affiner
- [ ] **KILL** si aucune traction et aucune clarte
- [ ] Archiver les decisions et les raisons

---

## 8. Protocole de Validation Terrain

Avant de coder, tu dois confirmer au moins 3/5 hypotheses :

| # | Hypothese | Comment valider | Signal positif |
|---|-----------|-----------------|----------------|
| 1 | **Probleme** | 5+ avis/posts avec meme douleur | Mots identiques utilises |
| 2 | **Segment** | Profil coherent dans les sources | Meme role/contexte revient |
| 3 | **Valeur** | Landing page + promesse | >10% taux de clic/inscription |
| 4 | **Paiement** | Question directe ou pricing test | "Oui je paierais X EUR" |
| 5 | **Canal** | Test d'acquisition sur 1 canal | CAC estimable et viable |

### Outils de validation rapide

- **Landing page** : Carrd (gratuit), Framer, Webflow
- **Formulaire** : Tally (gratuit), Typeform
- **Waitlist** : Stripe Payment Links, Gumroad pre-order
- **Interviews** : 3-5 appels de 15min avec le segment cible
- **Test prix** : "Seriez-vous pret a payer X EUR/mois pour [promesse] ?"

---

## 9. Regle Go/No-Go

### 5 conditions obligatoires (minimum 4/5)

- [ ] Probleme douloureux
- [ ] Segment precis
- [ ] Paiement plausible
- [ ] MVP faisable en <6 semaines
- [ ] Canal d'acces realiste

### Red flags — Kill immediat

- Tu ne peux pas decrire le segment en 1 phrase
- Tu ne sais pas comment les atteindre
- Le pricing est "on verra"
- Le MVP prend +3 mois
- Tu n'as aucune preuve de demande

---

## 10. Stack d'outils

| Besoin | Outil | Usage |
|--------|-------|-------|
| Tendances mobile | Sensor Tower, data.ai, Appfigures | Categories, revenus, downloads |
| SEO / demande | Ahrefs, Semrush, Google Trends | Volume, mots-cles, tendances |
| Voix du client | Reddit, reviews, forums, Product Hunt | Frustrations, langue reelle |
| Scoring | Airtable (ou CSV local) | Pipeline d'opportunites |
| Documentation | Notion ou Markdown local | Fiches projet |
| Validation | Carrd, Tally, Framer | Landing pages, formulaires |
| Analyse | Claude Code, scripts Python | Synthese avis, extraction patterns |

---

## 11. Metriques de suivi du systeme

| Metrique | Cible |
|----------|-------|
| Idees sourcees / semaine | 5-10 |
| Idees qualifiees / mois | 10-15 |
| Idees scorees >60 / mois | 3-5 |
| Validations terrain / mois | 1-2 |
| Apps lancees / trimestre | 0-1 |

Le systeme fonctionne si tu tues plus d'idees que tu n'en lances.
C'est normal et sain.
