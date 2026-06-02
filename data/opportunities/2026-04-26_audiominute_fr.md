# AudioMinute FR

> Nom de code temporaire — angle "résumés de livres 15 min audio FR"
> À renommer après validation positionnement (voir Q1 plus bas).

## Identite
- **Categorie** : Education / Self-improvement / Audio
- **Segment cible** : Francophones 25-50 ans qui veulent apprendre/lire mais n'ont pas le temps des livres complets — commuters, parents actifs, professionnels en formation continue
- **Date de creation** : 2026-04-26
- **Statut** : Backlog
- **Marketplace cible prioritaire** : **Play Store FR + iOS FR** (segment grand public mobile-first)

## Probleme
- **Enonce** : Les francophones qui veulent s'instruire/lire perdent ~85% des livres qu'ils achètent (jamais finis) parce qu'aucune app FR ne propose un format audio condensé adapté à leur quotidien (15 min entre 2 réunions, dans le métro, en cuisine).
- **Contexte d'usage** : Quotidien fragmenté — trajets, sport, vaisselle, attente. L'utilisateur veut "consommer" 1 livre en 1 jour, pas en 1 mois.
- **Alternative actuelle** :
  - Audible / Apple Books / Storytel : livres complets (8-15h), pas adaptés au format court
  - Wiser (anglophone, gagnant Best of Play Store 2025) : pas de version FR
  - Blinkist (anglophone) : version FR très limitée, catalogue daté
  - getAbstract : B2B uniquement, cher (>30€/mois)
  - Podcasts : non structurés, pas de progression mesurable
- **Pourquoi c'est penible** :
  - Format livre complet = engagement temporel impossible (commencer puis abandonner)
  - Apps anglo = barrière langue + culture US dominant le contenu
  - Pas de gamification du progrès (vs apps wellness type Focus Friend)
  - Pas de système de "1 livre/jour" structurant

## Marche
- **Taille estimee du segment** : ~12M francophones lecteurs réguliers (FR+BE+CH+QC), dont ~3M en quête d'efficacité temporelle (estimation à valider via Médiamétrie/CNL)
- **Tendance** : **À valider** — Wiser a gagné Play Store 2025 anglophone, signal fort que le format émerge globalement. Trend FR à mesurer via Google Trends.
- **Concurrents directs FR** :
  - **À benchmarker rigoureusement** : Sybel, Majelan, NewsBytes FR, Curio, Synapsen
  - **À benchmarker (pas FR mais utilisé en FR)** : Blinkist (catalogue FR limité), Wiser (pas en FR)
- **Gaps concurrentiels probables** (à confirmer) :
  - Aucun pur-play "résumés de livres 15 min" 100% FR avec catalogue récent
  - Aucun ne combine résumé audio + progression gamifiée + recommandation personnalisée
  - Blinkist FR = catalogue daté, prix premium, expérience cheap

## Driver structurel
- **Aucun driver réglementaire** (c'est un pari trend culturel, pas obligation légale)
- **Driver culturel** : décrochage attentionnel + inflation du temps fragmenté + succès Focus Friend / Wiser 2025 sur le créneau "micro-engagement"
- Donc **pas de bonus +8 dans le scoring V3** — honnête.

## Proposition
- **Hypothese de valeur** : Une app FR native qui transforme 1 livre en 1 séance audio de 15 min, avec une progression daily (1 livre/jour), des recommandations personnalisées, et une gamification légère type Focus Friend.
- **Differenciation** :
  1. **Première app pur-play résumés audio FR** (à valider absence concurrence directe)
  2. **Format strict 15 min** (pas variable comme Blinkist) = engagement prévisible
  3. **Catalogue FR-first** : essais français contemporains, pas que la traduction US
  4. **Streak daily** + avatar gamifié (lessons learned de Focus Friend)
  5. **Stack identique à Respir/SleepCoach** = coût marginal nul
- **Monetisation** : Freemium — 3 résumés/semaine gratuits, illimité 6.99€/mois ou 49€/an
- **Prix envisage** : 6.99€/mois ou 49€/an (cohérent SleepCoach FR / Respir)

## Validation requise (avant tout code)
- [ ] **Concurrence FR vide confirmée** : audit Play Store FR + App Store FR + reviews Blinkist FR (volumes négatifs sur catalogue/pricing/FR ?)
- [ ] **Demande organique** : community_signal.py sur Reddit FR + Twitter FR + Google Trends FR sur "résumé livre", "blinkist FR", "lire vite", "livre audio court"
- [ ] **Volume de recherche App Store FR** via AppTweak / SensorTower sur "résumé livres", "blinkist", variantes
- [ ] **Test landing** : page "App résumés de livres 15 min FR" avec formulaire pré-inscription. Seuil GO : >3% conversion visiteur → inscrit.
- [ ] **Validation pricing** : 5 interviews pour valider 6.99€/mois sur ce segment (contre 9.99€ Blinkist FR)

## Risques connus
1. **Droits d'auteur** : résumer un livre est une zone grise juridique en FR (droit moral fort). À cadrer avec un avocat avant publication. Modèles existants : Blinkist a des accords éditeurs, getAbstract aussi.
2. **Production de contenu** : 1 résumé = 4-8h de travail (lecture + rédaction + voix). Catalogue minimal viable = 100 résumés = 600-800h. **Bloquant solo dev** — nécessite stagiaires/freelances/IA assistée (TTS premium type ElevenLabs).
3. **Audio quality bar** : Wiser/Blinkist ont des voix studio. Solo dev = ElevenLabs/PlayHT. Risque rejet si voix synthétique perceptible.
4. **Catalogue minimum** : sous 50 titres = abandon. Au-dessus de 200 = effort de lancement énorme.

## Verdict provisoire (avant Engine)
- **Score estimé** : 65-75/100 si concurrence FR confirmée vide, 50-60/100 sinon
- **Categorie probable** : B — Validate (zone 60-74) — pas A
- **Bloquants pré-code** :
  1. Audit juridique droits éditeurs (1-2 semaines)
  2. Validation segment + concurrence (community_signal + scrape App Store FR)
  3. Décision modèle contenu : (a) accord éditeurs (long), (b) résumés inspirés non protégés (creux), (c) résumés sponsorisés par l'éditeur (modèle B2B2C)

## Next actions
1. **Lancer MOAT Engine** sur l'angle (à exécuter par Olivier — paramètres à définir) :
   ```bash
   python scripts/moat_engine.py "AudioMinute FR" \
     --query "résumé livre audio rapide" \
     --competitors "com.blinkslabs.blinkist.android,fr.sybel,com.majelan.app" \
     --segment-size 3000000 --arpu 60 \
     --geo-target FR --trend-index-avg 30 \
     --timing-type 3 \
     --data-freshness-date 2026-04-26
   ```
2. **Lancer community_signal.py** sur les forums FR :
   ```bash
   python scripts/community_signal.py "résumé livre" "lire vite" "livre audio" --idea "AudioMinute FR"
   ```
3. **Audit juridique préalable** (avant scoring final) — coût estimé 200-500€ pour cadrage initial avec un avocat PI.
4. **Si Engine valide** : créer le design_prompt via `python scripts/build_blueprint.py "AudioMinute FR"` puis discuter en équipe.

## Decision
- **Categorie** : ? (avant Engine) — probable **B — Validate** post-scoring
- **Prochaine action** : Lancer MOAT Engine + community_signal (commandes ci-dessus)
- **Deadline validation** : 2026-05-15 (3 semaines pour tirer un go/no-go)

---

## Sources auto
- **Date scaffolding** : 2026-04-26
- **Source idée** : Discussion 2026-04-26 — Best of Play Store 2025 Google a couronné Wiser (livres audio 15 min/jour) comme meilleure app quotidien. Pattern à porter en FR (aucune app pur-play équivalente sur le marché francophone à ce jour, à valider).
- **Engine source** : Aucun (à générer via MOAT Engine — voir Next actions)
- **Pattern référent** : Wiser (anglophone, gagnant Best of Play Store 2025), Blinkist (modèle économique de référence), Focus Friend (gamification légère wellness — vainqueur "Best App 2025")

*Scaffold rédigé manuellement à partir de la discussion. À enrichir avec les outputs MOAT Engine + community_signal.*
