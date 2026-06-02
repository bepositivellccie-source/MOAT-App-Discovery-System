# Prompt Claude Design — CoachCRM
> Généré le 2026-04-26 depuis AppHunter MOAT V3.1 — Score 74/100 — B -- Validate
> Source : engine_coachcrm_20260410_1535.json

---

## 1. Rôle + Mission

Tu es directeur artistique senior sur **CoachCRM**.

Produis des mockups HTML/Tailwind CSS, viewport **380×812 px**, chaque écran = un
fichier HTML autonome lisible dans un navigateur (Tailwind via CDN, pas de JS externe).
Données fictives mais réalistes (vrais prénoms, vrais chiffres plausibles).

Ne me demande pas de clarifications sur le produit. Lis ce brief, puis pose tes questions
design en Section 6 avant de produire quoi que ce soit.

---

## 2. Contexte Produit

- **App** : CoachCRM
- **Cible** : ~50 000 personnes
- **Pain principal** : 44.5% d'avis négatifs sur les apps existantes · 67.1% de plaintes sur le pricing (signal de paiement fort) · validé sur 274 avis réels
- **Verticale** : B2B — outil professionnel / gestion
- **Driver marché** : À préciser
- **Score MOAT** : 74/100 — B -- Validate

---

## 3. Top Frustrations Compétiteurs (274 avis analysés)

- **gratuit** (33 mentions, ~12% des avis négatifs)
- **payant** (25 mentions, ~9% des avis négatifs)
- **abonnement** (22 mentions, ~8% des avis négatifs)
- **payante** (12 mentions, ~4% des avis négatifs)
- **cher** (9 mentions, ~3% des avis négatifs)
- **impossible** (8 mentions, ~3% des avis négatifs)

---

## 4. Garde-fous Design NON NÉGOCIABLES

Ces contraintes sont dérivées des données marché objectives.
Elles doivent être respectées dans chaque écran sans exception.

- Freemium lisible : les features gratuites clairement identifiées, pas de bait-and-switch sur les limites
- Paywall différé (J+14 minimum) sans saisie de CB — l'utilisateur expérimente la valeur AVANT de payer
- Tarif annuel + économie visible AVANT le paywall — ex. 39.99€/an vs 59.88€ en mensuel
- L'app reste utilisable sans paiement — le free tier est réel, pas un teaser frustrant
- La valeur justifie le prix — afficher l'économie AVANT le chiffre de l'abonnement
- UX testée par 3 non-techniciens cible avant release — aucune action bloquante sans issue visible
- Qualité premium perçue dès le premier écran — polish visible avant même l'inscription
- Comparatif Free/Pro visible dès l'onboarding — bénéfice perçu avant demande de paiement
- Performance perçue prioritaire — transitions < 200ms, aucun spinner > 1s sans feedback textuel
- Robustesse visible — chaque action a un état succès ET un état erreur avec instruction de récupération
- Sobriété professionnelle absolue — un seul CTA principal par écran, hiérarchie visuelle tranchée, chiffres en police tabulaire

---

## 5. Livrables Attendus

Produis 6 écrans dans cet ordre exact :

Écran 1 — Dashboard (KPIs trésorerie + actions en attente + alerte impayés)
Écran 2 — Liste principale (filtre par statut : brouillon / envoyée / payée / impayée)
Écran 3 — Création (formulaire principal + calcul automatique TVA)
Écran 4 — Détail (aperçu document + actions : envoyer / relancer / encaisser)
Écran 5 — Fiche client (coordonnées + historique + solde total)
Écran 6 — Paramètres (profil entreprise, modèles, conditions de paiement)

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

Commence par la dimension la plus structurante pour CoachCRM.

---
*AppHunter build_blueprint.py V2 — 2026-04-26*
