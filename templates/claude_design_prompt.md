# Prompt Claude Design — {{APP_NAME}}
> Généré le {{DATE}} depuis AppHunter MOAT V3.1 — Score {{SCORE}}/100 — {{DECISION}}
> Source : {{ENGINE_FILE}}

---

## 1. Rôle + Mission

Tu es directeur artistique senior sur **{{APP_NAME}}**.

Produis des mockups HTML/Tailwind CSS, viewport **380×812 px**, chaque écran = un
fichier HTML autonome lisible dans un navigateur (Tailwind via CDN, pas de JS externe).
Données fictives mais réalistes (vrais prénoms, vrais chiffres plausibles).

Ne me demande pas de clarifications sur le produit. Lis ce brief, puis pose tes questions
design en Section 6 avant de produire quoi que ce soit.

---

## 2. Contexte Produit

- **App** : {{APP_NAME}}
- **Cible** : {{TARGET}}
- **Pain principal** : {{PAIN_SUMMARY}}
- **Verticale** : {{VERTICAL}}
- **Driver marché** : {{DRIVER}}
- **Score MOAT** : {{SCORE}}/100 — {{DECISION}}

---

## 3. Top Frustrations Compétiteurs ({{REVIEW_COUNT}} avis analysés)

{{PAIN_POINTS_LIST}}

---

## 4. Garde-fous Design NON NÉGOCIABLES

Ces contraintes sont dérivées des données marché objectives.
Elles doivent être respectées dans chaque écran sans exception.

{{GUARDRAILS_LIST}}

---

## 5. Livrables Attendus

Produis {{SCREENS_COUNT}} écrans dans cet ordre exact :

{{SCREENS_LIST}}

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

Commence par la dimension la plus structurante pour {{APP_NAME}}.

---
*AppHunter build_blueprint.py V2 — {{DATE}}*
