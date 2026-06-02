# Prompt Claude Design — DecidR
> Généré le 2026-04-26 depuis AppHunter MOAT V3.1 — Score 95/100 — A -- Build now
> Source : engine_decidr_20260411_2059.json

---

## 1. Rôle + Mission

Tu es directeur artistique senior sur **DecidR**.

Produis des mockups HTML/Tailwind CSS, viewport **380×812 px**, chaque écran = un
fichier HTML autonome lisible dans un navigateur (Tailwind via CDN, pas de JS externe).
Données fictives mais réalistes (vrais prénoms, vrais chiffres plausibles).

Ne me demande pas de clarifications sur le produit. Lis ce brief, puis pose tes questions
design en Section 6 avant de produire quoi que ce soit.

---

## 2. Contexte Produit

- **App** : DecidR
- **Cible** : ~4 000 000 personnes | SOM Solo Dev Y1 : ~3 360 EUR/mois
- **Pain principal** : 53.3% d'avis négatifs sur les apps existantes · 69.8% de plaintes sur le pricing (signal de paiement fort) · validé sur 150 avis réels
- **Verticale** : Consumer — app grand public
- **Driver marché** : À préciser
- **Score MOAT** : 95/100 — A -- Build now

---

## 3. Top Frustrations Compétiteurs (150 avis analysés)

- **gratuit** (22 mentions, ~15% des avis négatifs)
- **abonnement** (15 mentions, ~10% des avis négatifs)
- **payant** (15 mentions, ~10% des avis négatifs)
- **cher** (7 mentions, ~5% des avis négatifs)
- **impossible** (7 mentions, ~5% des avis négatifs)
- **payante** (5 mentions, ~3% des avis négatifs)

---

## 4. Garde-fous Design NON NÉGOCIABLES

Ces contraintes sont dérivées des données marché objectives.
Elles doivent être respectées dans chaque écran sans exception.

- Freemium lisible : les features gratuites clairement identifiées, pas de bait-and-switch sur les limites
- Tarif annuel + économie visible AVANT le paywall — ex. 39.99€/an vs 59.88€ en mensuel
- Paywall différé (J+14 minimum) sans saisie de CB — l'utilisateur expérimente la valeur AVANT de payer
- La valeur justifie le prix — afficher l'économie AVANT le chiffre de l'abonnement
- UX testée par 3 non-techniciens cible avant release — aucune action bloquante sans issue visible
- L'app reste utilisable sans paiement — le free tier est réel, pas un teaser frustrant
- Comparatif Free/Pro visible dès l'onboarding — bénéfice perçu avant demande de paiement
- Qualité premium perçue dès le premier écran — polish visible avant même l'inscription
- Performance perçue prioritaire — transitions < 200ms, aucun spinner > 1s sans feedback textuel

---

## 5. Livrables Attendus

Produis 6 écrans dans cet ordre exact :

Écran 1 — Onboarding (setup profil + valeur démontrée en < 60s)
Écran 2 — Accueil (dashboard principal + action principale du jour)
Écran 3 — Feature principale (cœur du produit, flow complet)
Écran 4 — Progression (historique + tendances + insights)
Écran 5 — Paywall (essai sans CB, valeur avant prix)
Écran 6 — Profil / Paramètres (compte + préférences + abonnement)

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

Commence par la dimension la plus structurante pour DecidR.

---
*AppHunter build_blueprint.py V2 — 2026-04-26*
