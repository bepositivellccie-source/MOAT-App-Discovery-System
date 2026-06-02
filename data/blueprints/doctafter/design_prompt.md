# Prompt Claude Design — DoctAfter
> Généré le 2026-04-26 depuis AppHunter MOAT V3.1 — Score 88/100 — A -- Build now
> Source : engine_doctafter_20260410_1202.json

---

## 1. Rôle + Mission

Tu es directeur artistique senior sur **DoctAfter**.

Produis des mockups HTML/Tailwind CSS, viewport **380×812 px**, chaque écran = un
fichier HTML autonome lisible dans un navigateur (Tailwind via CDN, pas de JS externe).
Données fictives mais réalistes (vrais prénoms, vrais chiffres plausibles).

Ne me demande pas de clarifications sur le produit. Lis ce brief, puis pose tes questions
design en Section 6 avant de produire quoi que ce soit.

---

## 2. Contexte Produit

- **App** : DoctAfter
- **Cible** : ~40 000 000 personnes
- **Pain principal** : 50.0% d'avis négatifs sur les apps existantes · 52.1% de plaintes sur le pricing (signal de paiement fort) · validé sur 300 avis réels
- **Verticale** : Consumer — app grand public
- **Driver marché** : À préciser
- **Score MOAT** : 88/100 — A -- Build now

---

## 3. Top Frustrations Compétiteurs (300 avis analysés)

- **payant** (69 mentions, ~23% des avis négatifs)
- **payante** (47 mentions, ~16% des avis négatifs)
- **gratuit** (26 mentions, ~9% des avis négatifs)
- **cher** (16 mentions, ~5% des avis négatifs)
- **impossible** (15 mentions, ~5% des avis négatifs)
- **nul** (8 mentions, ~3% des avis négatifs)

---

## 4. Garde-fous Design NON NÉGOCIABLES

Ces contraintes sont dérivées des données marché objectives.
Elles doivent être respectées dans chaque écran sans exception.

- Paywall différé (J+14 minimum) sans saisie de CB — l'utilisateur expérimente la valeur AVANT de payer
- L'app reste utilisable sans paiement — le free tier est réel, pas un teaser frustrant
- Freemium lisible : les features gratuites clairement identifiées, pas de bait-and-switch sur les limites
- La valeur justifie le prix — afficher l'économie AVANT le chiffre de l'abonnement
- UX testée par 3 non-techniciens cible avant release — aucune action bloquante sans issue visible
- Qualité premium perçue dès le premier écran — polish visible avant même l'inscription
- Tarif annuel + économie visible AVANT le paywall — ex. 39.99€/an vs 59.88€ en mensuel
- Robustesse visible — chaque action a un état succès ET un état erreur avec instruction de récupération
- Stabilité visible — états error/empty/loading jamais silencieux, récupération toujours explicite
- ZÉRO publicité dans le tier payant — mentionné explicitement dans le paywall comme avantage clé
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

Commence par la dimension la plus structurante pour DoctAfter.

---
*AppHunter build_blueprint.py V2 — 2026-04-26*
