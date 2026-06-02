# Prompt Claude Design — ZenColere
> Généré le 2026-04-24 depuis AppHunter MOAT V3.1 — Score 82/100 — A -- Build now
> Source : engine_zencolere_20260410_1709.json

---

## 1. Rôle + Mission

Tu es directeur artistique senior sur **ZenColere**.

Produis des mockups HTML/Tailwind CSS, viewport **380×812 px**, chaque écran = un
fichier HTML autonome lisible dans un navigateur (Tailwind via CDN, pas de JS externe).
Données fictives mais réalistes (vrais prénoms, vrais chiffres plausibles).

Ne me demande pas de clarifications sur le produit. Lis ce brief, puis pose tes questions
design en Section 6 avant de produire quoi que ce soit.

---

## 2. Contexte Produit

- **App** : ZenColere
- **Cible** : ~5 000 000 personnes | SOM Solo Dev Y1 : ~3 000 EUR/mois
- **Pain principal** : 60.7% de plaintes sur le pricing (signal de paiement fort) · validé sur 187 avis réels
- **Verticale** : Bien-etre — sante mentale / physique
- **Driver marché** : À préciser
- **Score MOAT** : 82/100 — A -- Build now

---

## 3. Top Frustrations Compétiteurs (187 avis analysés)

- **gratuit** (13 mentions, ~7% des avis négatifs)
- **payant** (12 mentions, ~6% des avis négatifs)
- **payante** (8 mentions, ~4% des avis négatifs)
- **abonnement** (8 mentions, ~4% des avis négatifs)
- **nul** (6 mentions, ~3% des avis négatifs)
- **cher** (3 mentions, ~2% des avis négatifs)

---

## 4. Garde-fous Design NON NÉGOCIABLES

Ces contraintes sont dérivées des données marché objectives.
Elles doivent être respectées dans chaque écran sans exception.

- Freemium lisible : les features gratuites clairement identifiées, pas de bait-and-switch sur les limites
- Paywall différé (J+14 minimum) sans saisie de CB — l'utilisateur expérimente la valeur AVANT de payer
- L'app reste utilisable sans paiement — le free tier est réel, pas un teaser frustrant
- Tarif annuel + économie visible AVANT le paywall — ex. 39.99€/an vs 59.88€ en mensuel
- Qualité premium perçue dès le premier écran — polish visible avant même l'inscription
- La valeur justifie le prix — afficher l'économie AVANT le chiffre de l'abonnement
- Robustesse visible — chaque action a un état succès ET un état erreur avec instruction de récupération
- UX testée par 3 non-techniciens cible avant release — aucune action bloquante sans issue visible
- Performance perçue prioritaire — transitions < 200ms, aucun spinner > 1s sans feedback textuel
- Environnement visuel calme — espaces blancs généreux, aucune urgence visuelle artificielle, couleurs apaisantes sans être fades

---

## 5. Livrables Attendus

Produis 6 écrans dans cet ordre exact :

Écran 1 — Onboarding étape finale (personnalisation de l'objectif principal)
Écran 2 — Dashboard Aujourd'hui (état émotionnel + action rapide + streak)
Écran 3 — Séance guidée en cours (exercice principal, progression visible)
Écran 4 — Journal de progression (graphe humeur + insights hebdo)
Écran 5 — Paywall (argument valeur, pas d'urgence artificielle)
Écran 6 — Bibliothèque de contenu (séances guidées disponibles, filtrables)

**Contraintes d'exécution :**
- Viewport fixe 380×812 px — pas de responsive, pas de scroll horizontal
- Tailwind CSS via CDN inline — aucune dépendance externe
- Commentaire `<!-- Composant : NomComposant -->` avant chaque bloc
- Lucide Icons exclusivement — aucun emoji dans l'UI, aucune image raster

---

## 6. Prochaine Étape

Avant de produire les mockups, pose-moi tes questions design.

Format attendu : questions à choix multiples, 3-4 options par question, chaque option
visuellement décrite (pas juste "option A" — décrire l'ambiance, le contraste, la densité).
Une question par dimension (couleur de fond, typographie, densité d'information, ton
iconographique, hiérarchie visuelle...).

Commence par la dimension la plus structurante pour ZenColere.

---
*AppHunter build_blueprint.py V2 — 2026-04-24*
