# Prompt Claude Design — SleepCoach FR
> Auto-généré par build_blueprint.py le 2026-04-24
> Score MOAT V3.1 : 88/100 | Archétype : wellness_organic
>
> ⚠️  Complétez les sections marquées [À COMPLÉTER] avant d'envoyer à Claude (~10-15 min)
> ✅  Sections pré-remplies depuis les données MOAT — relire et valider, ne pas modifier sans raison

---

## SECTION 1 — Rôle + Mission

Tu es directeur artistique senior sur **SleepCoach FR**.

Ta mission : produire des mockups SVG/HTML Tailwind en viewport 380×812 px que je peux
ouvrir directement dans un navigateur. Chaque écran = un fichier HTML autonome, styles
Tailwind via CDN inline, light mode par défaut, commenté composant par
composant.

Ne me demande pas de clarifications. Lis ce brief, respecte les contraintes, livre.

---

## SECTION 2 — Direction artistique NON NÉGOCIABLE

**Esthétique (1 phrase)** : Bienveillance organique, douce, respirante — l'app doit calmer avant d'informer

**Ambiance & Références** : Headspace, Calm, Noom

**Posture utilisateur** : Personne fatiguée ou stressée qui cherche du répit, pas un utilisateur expert

**Principe UX non-négociable** :
[À COMPLÉTER — 1 règle concrète, mesurable. Ex : "Jamais plus de 2 taps pour enregistrer une séance / consulter son progrès"]

---

## SECTION 3 — Design Tokens

**Palette**
| Rôle | Couleur | Hex |
|------|---------|-----|
| Primaire | Sage green | `#7BA05B` |
| Fond | Warm cream | `#FAF7F0` |
| Accent | Soft terracotta | `#E8A87C` |

**Typographie** : Nunito (titres, rounded) + Source Sans Pro (corps) — jamais de serif

**Iconographie** : Lucide Icons exclusivement — aucun emoji dans l'UI, aucune image raster

**Mode** : Light mode par défaut — dark optionnel en settings

**Tagline** (5-7 mots, apparaît dans onboarding) :
[À COMPLÉTER — ex : "Votre diabète, enfin sous contrôle"]

---

## SECTION 4 — Contexte Produit

SleepCoach FR résout : **49.7% d'avis négatifs sur les apps existantes · 62.3% de plaintes sur les prix (volonté de payer confirmée) · analysé sur 300 avis réels**

**Cible** : ~20 000 000 personnes

**Driver marché** : [À COMPLÉTER — driver principal du marché]

**Pain points validés** (top frustrations compétiteurs — intégrer dans chaque écran concerné) :
- **gratuit** (30 mentions, ~10.0% des avis négatifs)
- **payant** (28 mentions, ~9.0% des avis négatifs)
- **abonnement** (22 mentions, ~7.0% des avis négatifs)
- **payante** (12 mentions, ~4.0% des avis négatifs)
- **premium** (9 mentions, ~3.0% des avis négatifs)
- **impossible** (9 mentions, ~3.0% des avis négatifs)

**Vocabulaire produit** (libellés EXACTS à utiliser dans tous les écrans — ne pas substituer) :
<!-- Choisir 1 option par ligne, supprimer les autres -->
- **Action Log** : [CHOISIS : "Enregistrer ma séance" / "Ajouter au journal" / "Marquer fait"]
- **Action Track** : [CHOISIS : "Suivre ma progression" / "Voir mes tendances" / "Mon historique"]
- **Label Session** : [CHOISIS : "Séance" / "Moment" / "Session"]
- **Label Progress** : [CHOISIS : "Progression" / "Parcours" / "Chemin"]
- **Label Streak** : [CHOISIS : "Série en cours" / "Régularité" / "Streak"]

---

## SECTION 5 — Architecture

Navigation : Bottom Navbar — 4 onglets fixes

1. 🌙 **Aujourd'hui** — Entrée journal + action principale du jour
2. 📊 **Tendances** — Graphes progression 7j / 30j / 3m
3. 🧘 **Programme** — Contenu guidé, exercices, séances
4. 👤 **Profil** — Réglages, abonnement, historique

[À VALIDER — ajuster le nombre d'onglets et leur nom si la logique produit le requiert]

---

## SECTION 6 — Flow Clé

[À COMPLÉTER OBLIGATOIREMENT — c'est une décision produit, non automatisable]

Format attendu :
```
Point d'entrée unique : [écran de départ et contexte]
1. [Action utilisateur + ce qu'il voit]
2. [Transition + feedback système]
3. [Étape suivante]
...
N. Sortie : [confirmation / état final]

Ce qu'il N'Y A PAS dans ce flow : [lister explicitement les détours, écrans intermédiaires, confirmations superflues à éviter]
```

---

## SECTION 7 — Livrables

Produis dans cet ordre exact :

Écran 1 — Onboarding (étape 3/3 : personnalisation objectif)
Écran 2 — Dashboard Aujourd'hui (état + action rapide + streak)
Écran 3 — Journal d'entrée (formulaire principal)
Écran 4 — Tendances (graphe 30j + insight principal)
Écran 5 — Programme du jour (liste exercices/séances guidées)
Écran 6 — Paywall (upgrade vers premium, sans friction)

**Contraintes d'exécution :**
- Viewport fixe 380×812 px, pas de responsive breakpoints
- Chaque fichier = HTML autonome, Tailwind via CDN, pas de JS externe
- Commentaires `<!-- Composant : NomComposant -->` avant chaque bloc
- Pas de scroll horizontal, pas d'éléments tronqués
- Toutes les données sont fictives mais réalistes (vrais prénoms, vrais chiffres plausibles)

**Règle d'arbitrage finale :** En cas de doute entre deux options, choisis la plus **douce et rassurante**.

---

## FEATURES P0 À INTÉGRER (depuis analyse compétiteurs)

Les écrans doivent répondre aux frustrations suivantes, identifiées sur 300 avis :

- 🔴 **P0** — Frustration : "gratuit" (30 mentions) → **Mode freemium réel — pas de freemium-bait avec features bloquées après 2 jours**
- 🔴 **P0** — Frustration : "payant" (28 mentions) → **Essai 14 jours sans saisie de CB — choisir de payer après avoir vu la valeur**
- 🔴 **P0** — Frustration : "abonnement" (22 mentions) → **Prix affiché en clair AVANT le paywall — pas de surprise**
- 🔴 **P0** — Frustration : "premium" (9 mentions) → **Comparatif Free/Pro visible dès l'onboarding — valeur perçue immédiate**
- 🔴 **P0** — Frustration : "ne fonctionne" (7 mentions) → **Tests E2E sur device Android bas de gamme < 2 Go RAM — Pixel 4a minimum**
- 🔴 **P0** — Frustration : "bug" (4 mentions) → **Sentry intégré dès S1 — crash-free rate > 99.5% avant launch**
- 🟡 **P1** — Frustration : "impossible" (9 mentions) → **Tests utilisateur avec 3 non-techniciens avant launch public**
- 🟡 **P1** — Frustration : "cher" (9 mentions) → **Tarif annuel avec économie visible — ex. 39.99€/an vs 59.88€ en mensuel**

---
*Généré par AppHunter build_blueprint.py — github.com/appHunter*
*Source engine : engine_sleepcoach_fr_20260410_1225.json*
