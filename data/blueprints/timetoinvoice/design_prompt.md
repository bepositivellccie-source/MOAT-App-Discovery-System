# Prompt Claude Design — TimeToInvoice
> Généré le 2026-04-26 depuis AppHunter MOAT V3.1 — Score 51/100 — C -- Watchlist
> Source : engine_timetoinvoice_20260419_1026.json

---

## 1. Rôle + Mission

Tu es directeur artistique senior sur **TimeToInvoice**.

Produis des mockups HTML/Tailwind CSS, viewport **380×812 px**, chaque écran = un
fichier HTML autonome lisible dans un navigateur (Tailwind via CDN, pas de JS externe).
Données fictives mais réalistes (vrais prénoms, vrais chiffres plausibles).

Ne me demande pas de clarifications sur le produit. Lis ce brief, puis pose tes questions
design en Section 6 avant de produire quoi que ce soit.

---

## 2. Contexte Produit

- **App** : TimeToInvoice
- **Cible** : ~1 000 000 personnes | SOM Solo Dev Y1 : ~1 050 EUR/mois
- **Pain principal** : Données de reviews insuffisantes — relancer avec --competitors
- **Verticale** : B2B — outil professionnel / gestion
- **Driver marché** : Driver reglementaire
- **Score MOAT** : 51/100 — C -- Watchlist

---

## 3. Top Frustrations Compétiteurs (0 avis analysés)

- [Aucune donnée disponible — relancer avec --competitors pour l'analyse reviews]

---

## 4. Garde-fous Design NON NÉGOCIABLES

Ces contraintes sont dérivées des données marché objectives.
Elles doivent être respectées dans chaque écran sans exception.

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

Commence par la dimension la plus structurante pour TimeToInvoice.

---
*AppHunter build_blueprint.py V2 — 2026-04-26*
