# Prompt Claude Design — DiabeteCoach FR
> Généré le 2026-04-26 depuis AppHunter MOAT V3.1 — Score 100/100 — A -- Build now
> Source : engine_diabetecoach_fr_20260424_1841.json

---

## 1. Rôle + Mission

Tu es directeur artistique senior sur **DiabeteCoach FR**.

Produis des mockups HTML/Tailwind CSS, viewport **380×812 px**, chaque écran = un
fichier HTML autonome lisible dans un navigateur (Tailwind via CDN, pas de JS externe).
Données fictives mais réalistes (vrais prénoms, vrais chiffres plausibles).

Ne me demande pas de clarifications sur le produit. Lis ce brief, puis pose tes questions
design en Section 6 avant de produire quoi que ce soit.

---

## 2. Contexte Produit

- **App** : DiabeteCoach FR
- **Cible** : ~4 500 000 personnes | SOM Solo Dev Y1 : ~4 646 EUR/mois
- **Pain principal** : 62.0% d'avis négatifs sur les apps existantes · 45.9% de plaintes sur le pricing (signal de paiement fort) · validé sur 150 avis réels
- **Verticale** : Sante numerique — pathologie chronique
- **Driver marché** : Driver structurel (loi ou pathologie — préciser)
- **Score MOAT** : 100/100 — A -- Build now

---

## 3. Top Frustrations Compétiteurs (150 avis analysés)

- **gratuit** (12 mentions, ~8% des avis négatifs)
- **payant** (11 mentions, ~7% des avis négatifs)
- **abonnement** (10 mentions, ~7% des avis négatifs)
- **premium** (10 mentions, ~7% des avis négatifs)
- **payante** (9 mentions, ~6% des avis négatifs)
- **impossible** (8 mentions, ~5% des avis négatifs)

---

## 4. Garde-fous Design NON NÉGOCIABLES

Ces contraintes sont dérivées des données marché objectives.
Elles doivent être respectées dans chaque écran sans exception.

- Freemium lisible : les features gratuites clairement identifiées, pas de bait-and-switch sur les limites
- Paywall différé (J+14 minimum) sans saisie de CB — l'utilisateur expérimente la valeur AVANT de payer
- Tarif annuel + économie visible AVANT le paywall — ex. 39.99€/an vs 59.88€ en mensuel
- Comparatif Free/Pro visible dès l'onboarding — bénéfice perçu avant demande de paiement
- L'app reste utilisable sans paiement — le free tier est réel, pas un teaser frustrant
- UX testée par 3 non-techniciens cible avant release — aucune action bloquante sans issue visible
- Robustesse visible — chaque action a un état succès ET un état erreur avec instruction de récupération
- ZÉRO publicité dans le tier payant — mentionné explicitement dans le paywall comme avantage clé
- Stabilité visible — états error/empty/loading jamais silencieux, récupération toujours explicite
- Qualité premium perçue dès le premier écran — polish visible avant même l'inscription
- Performance perçue prioritaire — transitions < 200ms, aucun spinner > 1s sans feedback textuel
- Action principale en 3 taps maximum — onboarding 3 étapes avec skip accessible à tout moment
- La valeur justifie le prix — afficher l'économie AVANT le chiffre de l'abonnement
- Tout opt-in (RGPD Art.7) — aucune action irréversible sans confirmation explicite, pas de cage dorée
- Légitimité médicale visible dès l'onboarding — mentions RGPD Art.9, encadrement médical, données chiffrées de sécurité
- Accessibilité prioritaire — typo min 17px, contrastes WCAG AAA, zones tactiles 48px+, aucun geste obscur (pas de swipe caché, pas de hold)
- Onboarding ultra-progressif — tutoriel skippable mais toujours ré-accessible, aucune hypothèse sur les compétences numériques

---

## 5. Livrables Attendus

Produis 6 écrans dans cet ordre exact :

Écran 1 — Dashboard accueil (mesures du jour + état global + alerte si hors seuil)
Écran 2 — Saisie rapide (action principale en < 3 taps, confirmation immédiate)
Écran 3 — Journal des 7 derniers jours (liste + mini-graph inline)
Écran 4 — Courbe Tendances 30j (évolution + marqueurs contextuels repas/médicaments)
Écran 5 — Paywall (essai 14j sans CB, tarif annuel mis en avant vs mensuel)
Écran 6 — Profil médical (seuils personnalisés, médecin référent, export PDF)

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

Commence par la dimension la plus structurante pour DiabeteCoach FR.

---
*AppHunter build_blueprint.py V2 — 2026-04-26*
