# CoachCRM -- Specification MVP

> Document de specification produit | Version 1.0 | 10 avril 2026
> Score MOAT : 79/100 | Categorie A -- Build Now

---

## 1. VISION PRODUIT

### One-liner

**CoachCRM : le CRM mobile-first qui remplace WhatsApp + Google Sheets + Notion pour les coachs fitness et praticiens bien-etre independants.**

### Probleme

Les coachs sportifs et praticiens bien-etre independants (personal trainers, professeurs de yoga, nutritionnistes) gerent aujourd'hui leur activite avec un patchwork d'outils non connectes :

- **WhatsApp** pour communiquer avec les clients (messages perdus, pas de suivi structure)
- **Google Sheets** pour le suivi des seances et des paiements (erreurs, pas de vision globale)
- **Notion / Notes** pour les programmes d'entrainement (pas de partage client fluide)
- **Factures manuelles** ou pas de facturation du tout

**Resultat** : perte de temps administrative (3-5h/semaine), clients qui passent entre les mailles, revenus non suivis, image non professionnelle.

Les apps existantes (Strong, Fitbod, Hevy) sont des **trackers d'exercices pour utilisateurs finaux**, pas des outils business pour coachs. 52% d'avis negatifs sur Fitbod citent le pricing abusif et les fonctionnalites manquantes. **Aucune app ne combine gestion clients + programmes personnalises + facturation + suivi dans un seul outil mobile.**

### Persona cible

| | |
|---|---|
| **Nom** | Julien Marchand |
| **Age** | 32 ans |
| **Profession** | Coach sportif independant (auto-entrepreneur) |
| **Localisation** | Lyon, France |
| **Clients** | 15-30 clients actifs |
| **Contexte** | Donne des cours en salle partenaire et a domicile. Gere tout depuis son telephone. Utilise WhatsApp pour les RDV, un Google Sheet pour tracker les paiements, envoie les programmes par PDF via email. Perd 1 client/mois par oubli de relance. Ne sait jamais exactement combien il a facture ce mois-ci. |
| **Frustrations** | Pas de vision globale sur ses clients, oublie de relancer, facturation chaotique, image "pas pro" |
| **Objectif** | Professionnaliser son activite, gagner du temps, ne plus perdre de clients par oubli |
| **Budget tech** | 10-15 EUR/mois maximum |
| **Devices** | iPhone 13 (principal), iPad occasionnel |

**Persona secondaire** : Sophie, 28 ans, professeure de yoga independante a Bordeaux, 20 clients, memes frustrations mais avec suivi de bien-etre (stress, sommeil) en plus des exercices.

---

## 2. MVP SCOPE (6 semaines)

### Ce qui est DANS le MVP

| # | Feature | Priorite | Complexite |
|---|---------|----------|------------|
| F1 | **Dashboard coach** -- Vue d'ensemble (clients actifs, seances du jour, CA du mois, relances a faire) | P0 | Moyenne |
| F2 | **Gestion clients (CRUD)** -- Ajouter, modifier, archiver un client avec infos de contact, notes, objectifs | P0 | Faible |
| F3 | **Fiche client detaillee** -- Historique seances, programme actif, statut paiement, notes | P0 | Moyenne |
| F4 | **Creation de programmes** -- Builder simple (exercices, series, reps, repos) avec templates | P0 | Elevee |
| F5 | **Suivi de seance** -- Logger une seance realisee avec notes coach, feedback client | P0 | Moyenne |
| F6 | **Facturation simple** -- Generer une facture PDF, marquer comme payee, historique | P1 | Moyenne |
| F7 | **Rappels et relances** -- Notifications push pour seances, relances clients inactifs | P1 | Moyenne |
| F8 | **Authentification** -- Email/password + Google Sign-In | P0 | Faible |

### Ce qui est HORS du MVP

| Feature exclue | Raison | Version cible |
|----------------|--------|---------------|
| App client (vue client separee) | Complexite x2, valider d'abord la valeur coach | v1.1 |
| Paiement en ligne (Stripe) | Reglementation, complexite integration | v1.2 |
| Calendrier/planning avec prise de RDV | Feature complexe, les coachs ont deja Google Calendar | v1.1 |
| Chat integre coach-client | WhatsApp suffit pour le MVP, deeplink vers WhatsApp a la place | v1.2 |
| Statistiques avancees / graphiques | Pas critique pour validation MVP | v1.1 |
| Multi-langue | Francais uniquement au lancement | v1.2 |
| Version web / desktop | Mobile-first, validation smartphone d'abord | v2.0 |
| Bibliotheque d'exercices avec videos | Trop lourd pour le MVP, saisie texte libre | v1.1 |
| Export comptable (CSV/FEC) | Nice-to-have post-validation | v1.2 |
| Mode hors-ligne complet | Connexion requise pour le MVP | v1.1 |

### User Stories

#### Gestion clients

- **US-01** : En tant que coach, je veux ajouter un nouveau client avec ses coordonnees et objectifs, pour centraliser mes informations clients en un seul endroit.
- **US-02** : En tant que coach, je veux voir la liste de tous mes clients actifs avec un indicateur visuel de leur statut (actif, inactif, en retard de paiement), pour savoir en un coup d'oeil ou j'en suis.
- **US-03** : En tant que coach, je veux consulter la fiche detaillee d'un client (historique, programme, paiements), pour preparer ma seance en 30 secondes.
- **US-04** : En tant que coach, je veux archiver un client sans le supprimer, pour garder l'historique si le client revient.

#### Programmes

- **US-05** : En tant que coach, je veux creer un programme d'entrainement personnalise (exercices, series, repetitions, repos), pour envoyer un plan structure a mon client.
- **US-06** : En tant que coach, je veux dupliquer un programme existant et l'adapter pour un autre client, pour gagner du temps sur les profils similaires.
- **US-07** : En tant que coach, je veux utiliser des templates de programmes pre-definis, pour ne pas repartir de zero a chaque fois.

#### Suivi seances

- **US-08** : En tant que coach, je veux logger une seance realisee avec la date, les exercices faits et mes notes, pour garder une trace de la progression du client.
- **US-09** : En tant que coach, je veux voir l'historique des seances d'un client, pour adapter le programme en fonction de sa progression.
- **US-10** : En tant que coach, je veux voir sur mon dashboard les seances prevues aujourd'hui, pour organiser ma journee.

#### Facturation

- **US-11** : En tant que coach, je veux generer une facture simple (PDF) pour un client avec le detail des seances, pour professionnaliser ma facturation.
- **US-12** : En tant que coach, je veux marquer une facture comme payee et voir l'historique des paiements, pour savoir qui me doit de l'argent.
- **US-13** : En tant que coach, je veux voir mon chiffre d'affaires du mois en cours sur le dashboard, pour piloter mon activite.

#### Relances

- **US-14** : En tant que coach, je veux recevoir une notification quand un client n'a pas eu de seance depuis 2 semaines, pour le relancer avant qu'il decroche.
- **US-15** : En tant que coach, je veux voir une liste des relances a faire sur mon dashboard, pour ne plus oublier de suivre mes clients.

---

## 3. ARCHITECTURE TECHNIQUE

### Stack technologique

| Couche | Choix | Justification |
|--------|-------|---------------|
| **Frontend** | Flutter 3.x (Dart) | Cross-platform iOS/Android, hot reload, excellente performance mobile, large communaute |
| **State Management** | Riverpod 2.x | Plus moderne que Provider, meilleure testabilite, gestion async native, moins de boilerplate que BLoC |
| **Backend** | **Supabase** | Voir justification ci-dessous |
| **Auth** | Supabase Auth | Email/password + OAuth Google integre |
| **Base de donnees** | PostgreSQL (via Supabase) | Relationnel = ideal pour un CRM, requetes complexes, RLS integre |
| **Stockage fichiers** | Supabase Storage | PDFs factures, photos profil |
| **Notifications push** | Firebase Cloud Messaging (FCM) | Standard industrie, gratuit, fiable |
| **Generation PDF** | Package `pdf` (Dart) | Generation cote client, pas de serveur supplementaire |
| **CI/CD** | GitHub Actions + Fastlane | Automatisation builds et deploiement stores |

### Pourquoi Supabase plutot que Firebase ?

| Critere | Supabase | Firebase |
|---------|----------|---------|
| Base de donnees | **PostgreSQL relationnel** -- parfait pour les relations coach/client/programme/seance | Firestore NoSQL -- jointures complexes et couteuses |
| Requetes | SQL natif, jointures, agregations | Requetes limitees, pas de jointures natives |
| Row Level Security | **RLS natif PostgreSQL** -- chaque coach ne voit que ses donnees | Security Rules (syntaxe propre, plus complexe) |
| Pricing | Genereux free tier (500MB, 50K MAU) | Free tier plus restrictif sur Firestore reads |
| Migrations | SQL standard, versionnable | Pas de schema, migrations manuelles |
| Vendor lock-in | PostgreSQL standard, portable | Proprietaire Google |
| Real-time | Oui (Realtime subscriptions) | Oui (natif Firestore) |
| Edge Functions | Deno (TypeScript) | Cloud Functions (Node.js) |

**Verdict** : Supabase est le choix optimal pour un CRM. Les donnees sont hautement relationnelles (coach -> clients -> programmes -> seances -> factures) et PostgreSQL excelle dans ce cas d'usage. Le RLS simplifie la securite multi-tenant.

### Modele de donnees

```
┌─────────────────────────────────────────────────────────────┐
│                      MODELE DE DONNEES                       │
└─────────────────────────────────────────────────────────────┘

coaches
├── id              UUID (PK, = auth.uid())
├── email           TEXT NOT NULL UNIQUE
├── full_name       TEXT NOT NULL
├── phone           TEXT
├── business_name   TEXT
├── siret           TEXT (pour facturation FR)
├── address         TEXT
├── avatar_url      TEXT
├── created_at      TIMESTAMPTZ
└── updated_at      TIMESTAMPTZ

clients
├── id              UUID (PK)
├── coach_id        UUID (FK -> coaches.id) NOT NULL
├── first_name      TEXT NOT NULL
├── last_name       TEXT NOT NULL
├── email           TEXT
├── phone           TEXT
├── date_of_birth   DATE
├── goals           TEXT
├── notes           TEXT
├── status          TEXT ('active', 'inactive', 'archived')
├── avatar_url      TEXT
├── created_at      TIMESTAMPTZ
└── updated_at      TIMESTAMPTZ

programs
├── id              UUID (PK)
├── coach_id        UUID (FK -> coaches.id) NOT NULL
├── client_id       UUID (FK -> clients.id) -- NULL = template
├── title           TEXT NOT NULL
├── description     TEXT
├── is_template     BOOLEAN DEFAULT FALSE
├── duration_weeks  INTEGER
├── status          TEXT ('draft', 'active', 'completed')
├── created_at      TIMESTAMPTZ
└── updated_at      TIMESTAMPTZ

program_exercises
├── id              UUID (PK)
├── program_id      UUID (FK -> programs.id) NOT NULL
├── day_number      INTEGER NOT NULL
├── order_index     INTEGER NOT NULL
├── exercise_name   TEXT NOT NULL
├── sets            INTEGER
├── reps            TEXT (ex: "12" ou "8-12")
├── rest_seconds    INTEGER
├── notes           TEXT
├── created_at      TIMESTAMPTZ
└── updated_at      TIMESTAMPTZ

sessions
├── id              UUID (PK)
├── coach_id        UUID (FK -> coaches.id) NOT NULL
├── client_id       UUID (FK -> clients.id) NOT NULL
├── program_id      UUID (FK -> programs.id)
├── scheduled_at    TIMESTAMPTZ
├── completed_at    TIMESTAMPTZ
├── status          TEXT ('scheduled', 'completed', 'cancelled', 'no_show')
├── coach_notes     TEXT
├── client_feedback TEXT
├── duration_min    INTEGER
├── created_at      TIMESTAMPTZ
└── updated_at      TIMESTAMPTZ

session_exercises
├── id              UUID (PK)
├── session_id      UUID (FK -> sessions.id) NOT NULL
├── exercise_name   TEXT NOT NULL
├── planned_sets    INTEGER
├── planned_reps    TEXT
├── actual_sets     INTEGER
├── actual_reps     TEXT
├── weight_kg       DECIMAL
├── notes           TEXT
└── created_at      TIMESTAMPTZ

invoices
├── id              UUID (PK)
├── coach_id        UUID (FK -> coaches.id) NOT NULL
├── client_id       UUID (FK -> clients.id) NOT NULL
├── invoice_number  TEXT NOT NULL UNIQUE
├── amount_cents    INTEGER NOT NULL
├── tax_rate        DECIMAL DEFAULT 0
├── status          TEXT ('draft', 'sent', 'paid', 'overdue')
├── issued_at       DATE NOT NULL
├── due_at          DATE NOT NULL
├── paid_at         DATE
├── pdf_url         TEXT
├── notes           TEXT
├── created_at      TIMESTAMPTZ
└── updated_at      TIMESTAMPTZ

invoice_lines
├── id              UUID (PK)
├── invoice_id      UUID (FK -> invoices.id) NOT NULL
├── description     TEXT NOT NULL
├── quantity         INTEGER DEFAULT 1
├── unit_price_cents INTEGER NOT NULL
├── amount_cents    INTEGER NOT NULL
└── created_at      TIMESTAMPTZ
```

### Row Level Security (RLS)

Toutes les tables appliquent la politique suivante :

```sql
-- Exemple pour la table clients
CREATE POLICY "coaches_own_clients" ON clients
  FOR ALL
  USING (coach_id = auth.uid())
  WITH CHECK (coach_id = auth.uid());
```

Chaque coach ne peut voir et modifier que ses propres donnees. Securite multi-tenant sans complexite applicative.

### Flux d'authentification

```
1. Ecran de bienvenue (onboarding 3 slides)
         │
         ▼
2. Login / Register
   ├── Email + mot de passe
   └── Google Sign-In (OAuth)
         │
         ▼
3. Supabase Auth verifie / cree le user
         │
         ▼
4. Si nouveau : creation profil coach (business_name, siret optionnel)
         │
         ▼
5. Redirection Dashboard
         │
         ▼
6. Token JWT stocke localement (flutter_secure_storage)
   Refresh automatique via Supabase SDK
```

---

## 4. ECRANS MVP

### 4.1 Onboarding (3 ecrans)

- Slide 1 : "Gerez vos clients en un seul endroit" (illustration)
- Slide 2 : "Creez des programmes personnalises" (illustration)
- Slide 3 : "Facturez simplement" (illustration)
- Bouton "Commencer" -> ecran Login

### 4.2 Login / Register

- Champs email + mot de passe
- Bouton "Continuer avec Google"
- Lien "Mot de passe oublie"
- Toggle Login / Inscription
- Pour l'inscription : champs nom, prenom, email, mot de passe

### 4.3 Profil coach (setup initial)

- Nom de l'activite / entreprise
- Numero de telephone
- SIRET (optionnel, pour facturation)
- Adresse
- Photo de profil (optionnelle)

### 4.4 Dashboard coach

L'ecran principal apres connexion. Vision a 360 degres de l'activite.

| Zone | Contenu |
|------|---------|
| **Header** | "Bonjour Julien" + avatar + icone notifications |
| **KPI Cards** (scroll horizontal) | Clients actifs (nombre), Seances aujourd'hui (nombre), CA du mois (EUR), Factures en attente (nombre) |
| **Seances du jour** | Liste des seances planifiees avec nom client, heure, programme associe. Tap -> fiche seance |
| **Relances** | Clients inactifs depuis 14+ jours, badge rouge. Tap -> fiche client + action rapide (WhatsApp deeplink) |
| **Actions rapides** | FAB (Floating Action Button) avec : + Nouveau client, + Nouvelle seance, + Nouvelle facture |

### 4.5 Liste clients

- Barre de recherche en haut
- Filtres : Tous / Actifs / Inactifs / Archives
- Liste scrollable avec pour chaque client :
  - Avatar (initiales si pas de photo)
  - Nom complet
  - Statut (badge couleur)
  - Derniere seance (date relative : "il y a 3 jours")
  - Indicateur paiement (vert = a jour, rouge = en retard)
- FAB : "+ Nouveau client"
- Swipe gauche : archiver. Swipe droite : appeler / WhatsApp

### 4.6 Fiche client detail

Ecran a onglets :

**Onglet "Infos"**
- Photo, nom, prenom, email, telephone
- Date de naissance, objectifs
- Notes libres du coach
- Boutons d'action : Appeler, WhatsApp (deeplinks), Email

**Onglet "Programme"**
- Programme actif (si existant) avec liste des exercices par jour
- Bouton "Creer un programme" ou "Modifier"
- Historique des programmes passes

**Onglet "Seances"**
- Historique chronologique des seances
- Pour chaque seance : date, duree, statut, notes
- Bouton "+ Planifier une seance"

**Onglet "Facturation"**
- Factures liees au client (liste)
- Total facture / total paye / solde restant
- Bouton "+ Nouvelle facture"

### 4.7 Creer / Editer programme

- Champ titre du programme
- Champ description
- Duree en semaines
- Toggle "Sauvegarder comme template"
- **Builder par jour** :
  - Onglets Jour 1, Jour 2, Jour 3... (ajoutables)
  - Pour chaque jour, liste d'exercices :
    - Nom de l'exercice (saisie texte libre + autocompletion depuis historique)
    - Nombre de series
    - Nombre de repetitions (champ texte pour "8-12")
    - Temps de repos (en secondes)
    - Notes
  - Bouton "+ Ajouter un exercice"
  - Drag & drop pour reordonner
- Bouton "Assigner au client" (selecteur client)
- Bouton "Sauvegarder brouillon"

### 4.8 Suivi seance

**Avant la seance (planification)**
- Selecteur client
- Date et heure
- Programme associe (optionnel)
- Notes pre-seance

**Pendant / apres la seance (logging)**
- Liste des exercices prevus (depuis le programme)
- Pour chaque exercice : saisie des series/reps reellement faits + poids
- Chronometre de repos (optionnel)
- Notes du coach (texte libre)
- Duree totale
- Bouton "Terminer la seance"

**Resume post-seance**
- Recap des exercices faits vs. prevus
- Champ feedback client (optionnel)
- Bouton "Sauvegarder"

### 4.9 Facturation simple

**Creer une facture**
- Client (selecteur)
- Numero de facture (auto-genere, format : COACH-2026-001)
- Date d'emission
- Date d'echeance
- Lignes de facture :
  - Description (ex: "Seance coaching 1h", "Pack 10 seances")
  - Quantite
  - Prix unitaire
  - Montant (calcul auto)
- Sous-total, TVA (configurable, defaut 0% pour auto-entrepreneur), Total
- Notes / conditions
- Bouton "Generer PDF"
- Bouton "Marquer comme envoyee"

**Liste des factures**
- Filtres : Toutes / En attente / Payees / En retard
- Pour chaque facture : numero, client, montant, statut (badge couleur), date
- Tap -> detail avec actions : Telecharger PDF, Marquer payee, Envoyer par email (deeplink)

### 4.10 Parametres

- Profil coach (modifier)
- Informations de facturation (SIRET, adresse, logo)
- Preferences de notifications (activer/desactiver relances)
- Delai de relance client inactif (defaut : 14 jours)
- Deconnexion
- Supprimer mon compte

---

## 5. MONETISATION

### Strategie : Freemium avec limites

Le modele freemium est choisi pour maximiser l'acquisition (le coach teste sans risque) et convertir par la valeur.

### Plan Gratuit -- "Starter"

| Feature | Limite |
|---------|--------|
| Clients | **5 clients maximum** |
| Programmes | 3 programmes actifs |
| Facturation | 3 factures/mois |
| Seances | Illimitees |
| Historique | 3 mois de donnees |
| Support | FAQ / email |

### Plan Payant -- "Pro" (9,99 EUR/mois)

| Feature | Limite |
|---------|--------|
| Clients | **Illimites** |
| Programmes | Illimites |
| Facturation | Illimitee |
| Seances | Illimitees |
| Historique | Illimite |
| Templates programmes | Acces a la bibliotheque de templates |
| Export donnees | CSV export |
| Support | Prioritaire (chat) |
| Badge | "Coach Pro" sur le profil |

### Plan Annuel

- 9,99 EUR/mois si mensuel = **119,88 EUR/an**
- **79,99 EUR/an** si abonnement annuel (soit 6,67 EUR/mois, -33%)
- Incentive : 2 mois offerts sur l'annuel

### Mecaniques de conversion

1. **Mur doux a 5 clients** : quand le coach ajoute le 6e client, ecran "Passez a Pro pour gerer tous vos clients" avec CTA clair
2. **Rappel contextuel** : apres la 3e facture du mois, "Vous avez atteint la limite gratuite ce mois-ci"
3. **Trial Pro** : 14 jours d'essai Pro gratuit a l'inscription (pas de CB requise)
4. **Valeur percue** : le coach economise 3-5h/semaine -> 9,99 EUR est negligeable vs. la valeur

### Revenue projection (conservatrice)

| Mois | Users total | Users Pro (10% conv.) | MRR |
|------|-------------|----------------------|-----|
| M3 | 200 | 20 | 200 EUR |
| M6 | 800 | 80 | 800 EUR |
| M12 | 2 500 | 375 (15% conv.) | 3 750 EUR |

---

## 6. METRIQUES DE SUCCES

### KPIs MVP (a tracker des le jour 1)

| KPI | Outil de mesure | Objectif M1 |
|-----|----------------|-------------|
| **Inscriptions** | Supabase Auth + Analytics | 100 inscriptions |
| **Activation** (coach qui ajoute 1+ client) | Event tracking | 60% des inscrits |
| **Retention J7** (revient apres 7 jours) | Analytics | 40% |
| **Retention J30** (revient apres 30 jours) | Analytics | 25% |
| **Seances loggees / coach / semaine** | BDD query | 3+ seances/semaine |
| **NPS (Net Promoter Score)** | In-app survey (J14) | > 30 |
| **Conversion Free -> Pro** | Stripe/RevenueCat | 8% a M1 |
| **DAU / MAU ratio** | Analytics | > 0.3 |

### Criteres Go / No-Go (apres 4 semaines)

#### GO (au moins 3 sur 5)

- [ ] 100+ inscriptions organiques (sans paid ads)
- [ ] Activation > 50% (au moins 50 coachs ont ajoute 1+ client)
- [ ] Retention J7 > 35%
- [ ] NPS > 20
- [ ] Au moins 5 coachs utilisent la facturation

#### NO-GO (indicateurs d'arret)

- [ ] Moins de 30 inscriptions en 4 semaines
- [ ] Activation < 20%
- [ ] Retention J7 < 15%
- [ ] NPS negatif (< 0)
- [ ] 0 coach utilise la facturation (feature non comprise/non voulue)

#### PIVOT (signaux faibles a investiguer)

- Activation > 50% mais retention J7 < 25% -> probleme de valeur recurrente, investiguer les features manquantes
- Beaucoup d'inscriptions mais peu de seances loggees -> le logging est trop lourd, simplifier l'UX
- Facturation tres utilisee mais pas les programmes -> pivoter vers un outil de facturation coach plutot qu'un CRM complet

---

## 7. PLANNING (6 semaines)

### Semaine 1 -- Fondations

| Tache | Responsable | Livrable |
|-------|-------------|----------|
| Setup projet Flutter + architecture | Dev | Projet init, structure dossiers, Riverpod configure |
| Setup Supabase (projet, tables, RLS) | Dev | Schema BDD deploye, RLS actives |
| Design system (couleurs, typo, composants) | Design/Dev | Theme Flutter, composants de base |
| Ecrans Auth (login, register, onboarding) | Dev | Auth fonctionnelle email + Google |
| Setup CI/CD (GitHub Actions) | Dev | Build auto sur push |

**Milestone S1** : Un coach peut s'inscrire, se connecter et voir un dashboard vide.

### Semaine 2 -- Gestion clients

| Tache | Responsable | Livrable |
|-------|-------------|----------|
| CRUD clients complet | Dev | Ajout, edition, archivage clients |
| Liste clients avec recherche et filtres | Dev | Ecran liste fonctionnel |
| Fiche client detaillee (onglet Infos) | Dev | Ecran fiche client |
| Dashboard : KPI card "Clients actifs" | Dev | Card dynamique |
| Tests unitaires gestion clients | Dev | Coverage > 80% |

**Milestone S2** : Un coach peut gerer ses clients (ajouter, modifier, consulter, archiver).

### Semaine 3 -- Programmes

| Tache | Responsable | Livrable |
|-------|-------------|----------|
| Builder de programme (exercices par jour) | Dev | Ecran creation programme |
| Templates de programmes (3 pre-definis) | Dev | Templates disponibles |
| Duplication de programme | Dev | Feature fonctionnelle |
| Assignation programme a un client | Dev | Lien programme-client |
| Fiche client : onglet Programme | Dev | Onglet fonctionnel |

**Milestone S3** : Un coach peut creer un programme personnalise et l'assigner a un client.

### Semaine 4 -- Suivi seances

| Tache | Responsable | Livrable |
|-------|-------------|----------|
| Planification seance | Dev | Creation seance avec date/heure/client |
| Logging seance (exercices reels) | Dev | Ecran suivi fonctionnel |
| Historique seances par client | Dev | Fiche client onglet Seances |
| Dashboard : seances du jour | Dev | Liste seances du jour |
| Dashboard : KPI "Seances aujourd'hui" | Dev | Card dynamique |

**Milestone S4** : Un coach peut planifier, logger et consulter ses seances.

### Semaine 5 -- Facturation + Relances

| Tache | Responsable | Livrable |
|-------|-------------|----------|
| Creation facture avec lignes | Dev | Ecran creation facture |
| Generation PDF facture | Dev | PDF telechargeables |
| Liste factures + filtres statut | Dev | Ecran liste factures |
| Dashboard : KPI CA du mois + factures en attente | Dev | Cards dynamiques |
| Systeme de relances (notification push) | Dev | Notifications clients inactifs |
| Dashboard : section relances | Dev | Liste des relances |

**Milestone S5** : Un coach peut facturer ses clients et recevoir des rappels de relance.

### Semaine 6 -- Polish + Beta

| Tache | Responsable | Livrable |
|-------|-------------|----------|
| Ecran parametres | Dev | Profil, preferences, deconnexion |
| Paywall freemium (limites plan gratuit) | Dev | Logique de limites + ecran upgrade |
| Bug fixes et optimisations performance | Dev | App stable |
| Tests end-to-end sur devices reels | QA/Dev | Rapport de tests |
| Preparation store listing (ASO) | Marketing | Screenshots, description, mots-cles |
| Soumission TestFlight (iOS) + Beta interne (Android) | Dev | Builds beta distribues |
| Onboarding 5-10 beta testeurs (coachs reels) | Produit | Feedback initial |

**Milestone S6** : App beta-testable par de vrais coachs. Soumission stores en preparation.

---

## 8. RISQUES ET MITIGATIONS

| # | Risque | Probabilite | Impact | Mitigation |
|---|--------|-------------|--------|------------|
| R1 | **Scope creep** -- tentative d'ajouter des features en cours de dev | Elevee | Eleve | Spec MVP verrouille. Toute nouvelle feature va dans un backlog v1.1. Revue de scope hebdo. |
| R2 | **Builder de programme trop complexe** -- UX lourde, abandon utilisateur | Moyenne | Eleve | Version 1 minimaliste (texte libre + structure simple). Pas de drag-and-drop fancy. Iterer apres feedback. |
| R3 | **Acquisition initiale difficile** -- pas d'utilisateurs beta | Moyenne | Eleve | Cibler 3-5 coachs dans le reseau personnel avant le dev. Pre-lancer sur des groupes Facebook/Instagram de coachs. Landing page avec waitlist des S1. |
| R4 | **Facturation non conforme** -- obligations legales FR non respectees | Faible | Eleve | Rechercher les obligations facture auto-entrepreneur FR. Mentions obligatoires sur le PDF. Disclaimer "ceci n'est pas un logiciel de comptabilite agree". |
| R5 | **Performance Supabase** -- latence sur requetes complexes | Faible | Moyen | Index sur les FK et colonnes filtrees. Pagination. Monitoring Supabase Dashboard. |
| R6 | **Rejet App Store** -- non-conformite Apple | Faible | Eleve | Review guidelines Apple des S1. Pas de paiement hors IAP pour le contenu digital. Utiliser RevenueCat pour les IAP. |
| R7 | **Concurrent lance un produit similaire** -- un acteur etabli copie l'idee | Faible | Moyen | Vitesse d'execution. Focus sur un niche (coachs FR francophones). Construire la communaute early. Le MOAT est dans la relation utilisateur, pas la tech. |
| R8 | **Un seul developpeur** -- bus factor = 1, risque de retard | Moyenne | Eleve | Code propre et documente. Architecture simple (pas d'over-engineering). Prioriser impitoyablement. Avoir un dev backup identifie. |
| R9 | **Adoption de la facturation faible** -- les coachs ne facturent pas via l'app | Moyenne | Moyen | Onboarding guide. Feature optionnelle, pas bloquante. Si non adoptee, pivoter vers la valeur "suivi client" uniquement. |
| R10 | **Notifications push mal percues** -- spam, desinstallation | Faible | Moyen | Opt-in explicite. Frequence limitee (max 1/jour). Parametres de notification granulaires. |

---

## ANNEXES

### A. Palette de couleurs suggeree

| Token | Valeur | Usage |
|-------|--------|-------|
| Primary | `#2563EB` (Blue 600) | Actions principales, CTA |
| Primary Light | `#DBEAFE` (Blue 100) | Backgrounds, badges |
| Success | `#16A34A` (Green 600) | Paye, actif, complete |
| Warning | `#F59E0B` (Amber 500) | En attente, attention |
| Error | `#DC2626` (Red 600) | En retard, erreur |
| Neutral 900 | `#111827` | Texte principal |
| Neutral 500 | `#6B7280` | Texte secondaire |
| Neutral 100 | `#F3F4F6` | Backgrounds |
| Surface | `#FFFFFF` | Cards, surfaces |

### B. Packages Flutter recommandes

| Package | Usage |
|---------|-------|
| `flutter_riverpod` | State management |
| `supabase_flutter` | SDK Supabase |
| `go_router` | Navigation declarative |
| `pdf` | Generation PDF |
| `printing` | Impression/partage PDF |
| `flutter_secure_storage` | Stockage tokens securise |
| `firebase_messaging` | Notifications push |
| `flutter_local_notifications` | Notifications locales |
| `intl` | Formatage dates/monnaie |
| `url_launcher` | Deeplinks WhatsApp/tel/email |
| `image_picker` | Photo profil |
| `shimmer` | Loading states |
| `flutter_slidable` | Swipe actions sur les listes |

### C. Commandes Supabase CLI (setup initial)

```bash
# Init projet
supabase init

# Demarrer localement
supabase start

# Creer une migration
supabase migration new create_initial_schema

# Appliquer les migrations
supabase db push

# Generer les types Dart (optionnel, avec supabase_cli)
supabase gen types dart --local > lib/models/database.types.dart
```

---

> **Document redige le 10 avril 2026**
> **Prochaine etape** : Validation du scope avec 3-5 coachs cibles, puis lancement du sprint 1.
