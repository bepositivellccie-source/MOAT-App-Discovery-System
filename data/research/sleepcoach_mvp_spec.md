# SleepCoach FR — Specification MVP

> **Le premier programme anti-insomnie sur mobile, en francais.**
> Score MOAT : 90/100 | Statut : GO | Date : 2026-04-10

---

## Table des matieres

1. [Vision Produit](#1-vision-produit)
2. [Protocole CBT-I Simplifie](#2-protocole-cbt-i-simplifie)
3. [MVP Scope (8 semaines de dev)](#3-mvp-scope-8-semaines-de-dev)
4. [Architecture Technique](#4-architecture-technique)
5. [Ecrans MVP](#5-ecrans-mvp)
6. [Monetisation](#6-monetisation)
7. [Validation Medicale](#7-validation-medicale)
8. [Metriques](#8-metriques)
9. [Planning (8 semaines)](#9-planning-8-semaines)
10. [Risques et Mitigations](#10-risques-et-mitigations)

---

## 1. VISION PRODUIT

### Positionnement

**"Le premier programme anti-insomnie sur mobile, en francais."**

SleepCoach FR n'est pas une enieme app de suivi du sommeil. C'est un programme therapeutique structure, base sur la CBT-I (Therapie Cognitive et Comportementale de l'Insomnie), le traitement de reference recommande par la HAS (Haute Autorite de Sante).

### Le probleme : tracker ≠ traiter

Les apps existantes (Sleep Cycle, Calm, Sleep as Android) **mesurent** le sommeil sans le **soigner**. C'est comme si toutes les apps de fitness se contentaient de peser les utilisateurs sans jamais proposer d'exercice.

| Ce que font les concurrents | Ce que fait SleepCoach |
|----|-----|
| Tracking du sommeil (capteur, micro) | Programme therapeutique structure |
| Sons/ambiances pour s'endormir | Exercices cognitifs et comportementaux |
| Donnees et graphiques | Plan d'action personnalise sur 8 semaines |
| Abonnement pour des features passives | Abonnement pour un accompagnement actif |

Resultat concurrents : 41% d'avis negatifs en moyenne, 78% des plaintes liees au prix. Les utilisateurs paient pour du tracking qui ne resout pas leur probleme.

### Pourquoi la CBT-I fonctionne

La CBT-I est le traitement de premiere intention de l'insomnie chronique. Elle a ete validee par plus de 200 essais cliniques :

- **Efficacite** : 75-80% des patients voient une amelioration significative
- **Durabilite** : les effets persistent apres la fin du programme (contrairement aux somniferes)
- **Sans effets secondaires** : alternative aux benzodiazepines qui entrainent dependance et tolerance
- **Programme court** : 6-8 semaines suffisent pour restructurer le sommeil
- **Adaptable au mobile** : exercices quotidiens courts (5-15 min), journal du sommeil, education

En France, la CBT-I est quasi inaccessible : peu de praticiens formes, listes d'attente de plusieurs mois, zero app en francais.

### Synergie avec Respir

L'app Respir (coherence cardiaque / respiration) partage le meme univers bien-etre :

- **Relaxation pre-sommeil** : la coherence cardiaque est un outil reconnu pour faciliter l'endormissement
- **Base utilisateur commune** : les utilisateurs de Respir sont deja sensibilises au bien-etre
- **Cross-promotion** : SleepCoach peut integrer des exercices de respiration issus de Respir dans le module relaxation
- **Vision ecosysteme** : a terme, une suite "bien-etre francophone" (Respir + SleepCoach + ...)
- **Code partage** : meme stack Flutter, composants UI reutilisables, architecture similaire

---

## 2. PROTOCOLE CBT-I SIMPLIFIE

### Les 5 piliers adaptes au mobile

#### a) Education sur le sommeil (Psychoeducation)

**Objectif** : comprendre le fonctionnement du sommeil pour desactiver l'anxiete.

| Contenu | Format mobile |
|---------|---------------|
| Horloge circadienne et pression de sommeil | Micro-lecon illustree (2-3 min) |
| Mythes sur le sommeil ("il faut 8h") | Quiz interactif |
| Comment l'insomnie se maintient (cercle vicieux) | Animation/schema interactif |
| Effets des ecrans, cafeine, alcool | Fiches pratiques |

**Semaines** : 1-2 (introduction), puis rappels tout au long du programme.

#### b) Restriction de sommeil (Sleep Window)

**Objectif** : consolider le sommeil en reduisant le temps passe au lit.

C'est le pilier le plus puissant et le plus contre-intuitif de la CBT-I.

| Etape | Implementation mobile |
|-------|----------------------|
| Calcul de l'efficacite du sommeil (SE) | Automatique via le journal du sommeil |
| Definition de la fenetre de sommeil initiale | Algorithme : temps de sommeil reel + 30 min (min 5h) |
| Ajustement hebdomadaire | Si SE > 85% : +15 min. Si SE < 80% : -15 min |
| Heure de lever FIXE | Alarme non-negociable configuree dans l'app |
| Heure de coucher calculee | Notification "c'est l'heure d'aller au lit" |

**Semaines** : 2-8. Ajustements chaque dimanche soir.

**Garde-fou** : fenetre de sommeil jamais inferieure a 5h. Avertissement si l'utilisateur conduit ou a un metier a risque.

#### c) Controle du stimulus

**Objectif** : reconditionner l'association lit = sommeil.

| Regle | Implementation mobile |
|-------|----------------------|
| Le lit sert uniquement a dormir (et au sexe) | Rappel dans les notifications du soir |
| Se lever si pas endormi apres 20 min | Timer discret + notification douce |
| Ne retourner au lit que quand on a sommeil | Checklist "signaux de sommeil" |
| Se lever a la meme heure chaque jour | Alarme fixe, meme le week-end |
| Pas de sieste (ou max 20 min avant 15h) | Rappel en journee si sieste detectee dans le journal |

**Semaines** : 2-8 (mis en place avec la restriction de sommeil).

#### d) Restructuration cognitive

**Objectif** : identifier et modifier les pensees dysfonctionnelles sur le sommeil.

| Pensee automatique | Exercice mobile |
|-------------------|-----------------|
| "Je ne dormirai jamais" | Journal de pensees (CBT classique) |
| "Une mauvaise nuit = journee foutue" | Registre de preuves pour/contre |
| "Je dois absolument dormir 8h" | Education + experience comportementale |
| Catastrophisation | Technique de decatastrophisation guidee |
| Rumination au coucher | Exercice "periode d'inquietude" (worry time) en soiree |

**Format** : exercices interactifs de 5-10 min, cartes a swiper, journaux structures.

**Semaines** : 3-6 (une fois les bases comportementales en place).

#### e) Hygiene du sommeil + Relaxation

**Objectif** : optimiser l'environnement et le corps pour le sommeil.

| Categorie | Contenu |
|-----------|---------|
| Environnement | Temperature, obscurite, bruit (checklist) |
| Alimentation | Cafeine (seuil 14h), alcool, repas lourds |
| Activite physique | Timing optimal (pas apres 19h) |
| Relaxation musculaire progressive | Audio guide (15 min) — **lien Respir** |
| Coherence cardiaque | Exercice 5-5-5 pre-sommeil — **module Respir** |
| Body scan | Audio guide (10 min) |
| Visualisation | Audio guide (10 min) |

**Semaines** : 1-8 (hygiene des la semaine 1, relaxation a partir de la semaine 3).

---

### Programme 8 semaines : structure detaillee

| Semaine | Theme principal | Piliers actifs | Contenu |
|---------|----------------|----------------|---------|
| **S1** | Comprendre son insomnie | Education, Hygiene | Questionnaire ISI, debut du journal, lecon "le cercle vicieux de l'insomnie", checklist hygiene |
| **S2** | Restructurer son sommeil | Restriction, Stimulus, Education | Calcul efficacite sommeil, definition fenetre initiale, regles du stimulus, lecon "horloge biologique" |
| **S3** | Tenir bon | Restriction, Stimulus, Cognitif | Ajustement fenetre, debut exercices cognitifs (pensees automatiques), relaxation musculaire |
| **S4** | Les pensees qui empechent de dormir | Cognitif, Restriction | Journal de pensees, technique de decatastrophisation, ajustement fenetre, lecon "rumination" |
| **S5** | L'inquietude du soir | Cognitif, Relaxation | Exercice "worry time", coherence cardiaque pre-sommeil, body scan, ajustement fenetre |
| **S6** | Consolider les progres | Tous les piliers | Bilan mi-parcours (ISI), renforcement des techniques qui marchent, lecon "rechute" |
| **S7** | Autonomie | Tous les piliers | Reduction progressive de la dependance a l'app, creation de sa routine personnelle |
| **S8** | Bilan et maintien | Tous les piliers | ISI final, comparaison S1 vs S8, plan de maintien, transition vers mode "libre" |

### Routine quotidienne

**Soir (check-in) — notification a H-1 avant coucher :**
1. Comment s'est passee la journee ? (humeur 1-5)
2. Session du jour (exercice CBT-I, 5-15 min)
3. Relaxation optionnelle (audio)
4. Rappel des regles du stimulus

**Matin (journal) — notification au reveil :**
1. A quelle heure vous etes-vous couche ?
2. Combien de temps pour vous endormir ? (estimation)
3. Combien de reveils nocturnes ?
4. Heure de reveil final ?
5. Heure de lever ?
6. Qualite ressentie (1-5)

> Le journal du matin prend **moins de 60 secondes** a remplir. C'est critique pour la retention.

---

## 3. MVP SCOPE (8 semaines de dev)

### IN (fonctionnalites MVP)

| Feature | Priorite | Justification |
|---------|----------|---------------|
| Onboarding + questionnaire ISI | P0 | Personnalisation du programme, baseline medicale |
| Journal du sommeil (matin) | P0 | Donnee fondamentale du protocole, calcul efficacite |
| Check-in du soir + session du jour | P0 | Coeur du programme CBT-I |
| Programme 8 semaines (timeline) | P0 | Structure et progression, motivation |
| Dashboard sommeil (score, tendances) | P0 | Feedback visuel, motivation |
| Calcul automatique fenetre de sommeil | P0 | Pilier restriction — le plus efficace |
| Notifications (coucher, lever, session) | P0 | Sans notifications, pas d'adherence au programme |
| Contenu educatif (8 lecons) | P0 | Pilier education |
| Exercices cognitifs (4 types) | P1 | Pilier restructuration cognitive |
| Audio relaxation (3 seances) | P1 | Body scan, relaxation musculaire, coherence cardiaque |
| Profil utilisateur + settings | P1 | Preferences, rappels, objectifs |
| Ecran "Bilan" semaines 4 et 8 | P1 | Mesure d'efficacite, motivation |

### OUT (post-MVP)

| Feature | Raison de l'exclusion |
|---------|-----------------------|
| Tracking par capteur/micro | Complexite technique, pas necessaire pour la CBT-I |
| Smart alarm (reveil intelligent) | Feature concurrents, pas therapeutique |
| Communaute / forum | Moderation, RGPD, complexite |
| Integration Apple Health / Google Fit | Nice-to-have, pas critique |
| Mode sombre automatique | Post-MVP |
| Multi-langue | Francais uniquement au MVP |
| Gamification avancee (badges, niveaux) | Risque de trivialiser le therapeutique |
| Chat avec un professionnel | Complexite juridique et technique |
| Integration Respir (deep link) | Post-MVP, une fois les deux apps stables |
| Partenariats mutuelles | Post-validation du produit |
| Apple Watch / Wear OS | Post-MVP |
| Export PDF du journal | Nice-to-have |
| IA conversationnelle | Risque medical, complexite |

### User Stories

**Onboarding :**
- US-01 : En tant que nouvel utilisateur, je peux remplir le questionnaire ISI en moins de 3 minutes pour obtenir mon score d'insomnie initial.
- US-02 : En tant que nouvel utilisateur, je peux configurer mon heure de lever habituelle et mes preferences de notification.
- US-03 : En tant que nouvel utilisateur, je recois une explication claire de ce qu'est la CBT-I et pourquoi ca marche.

**Journal du sommeil :**
- US-04 : En tant qu'utilisateur, je remplis mon journal du sommeil chaque matin en moins de 60 secondes.
- US-05 : En tant qu'utilisateur, je vois mon efficacite de sommeil calculee automatiquement apres chaque entree.
- US-06 : En tant qu'utilisateur, je peux voir l'historique de mon journal sur les 7 derniers jours.

**Programme :**
- US-07 : En tant qu'utilisateur, je vois ma progression dans le programme de 8 semaines.
- US-08 : En tant qu'utilisateur, je recois chaque jour une session adaptee a ma semaine de programme.
- US-09 : En tant qu'utilisateur, je recois une notification le soir pour faire ma session du jour.
- US-10 : En tant qu'utilisateur, je peux rattraper une session manquee le lendemain.

**Restriction de sommeil :**
- US-11 : En tant qu'utilisateur, je vois ma fenetre de sommeil recommandee (heure coucher / heure lever).
- US-12 : En tant qu'utilisateur, je recois une notification a l'heure de coucher recommandee.
- US-13 : En tant qu'utilisateur, ma fenetre de sommeil est ajustee automatiquement chaque semaine selon mon efficacite.

**Dashboard :**
- US-14 : En tant qu'utilisateur, je vois mon score de sommeil actuel et sa tendance.
- US-15 : En tant qu'utilisateur, je vois mon streak (jours consecutifs de journal rempli).
- US-16 : En tant qu'utilisateur, je vois un graphique de mon efficacite de sommeil sur les 4 dernieres semaines.

**Relaxation :**
- US-17 : En tant qu'utilisateur, je peux lancer un audio de relaxation (body scan, relaxation musculaire, coherence cardiaque).
- US-18 : En tant qu'utilisateur, je peux ecouter l'audio en arriere-plan.

**Cognitif :**
- US-19 : En tant qu'utilisateur, je peux faire un exercice de restructuration cognitive guide (identifier pensee → preuves pour/contre → pensee alternative).
- US-20 : En tant qu'utilisateur, je peux faire un exercice de "worry time" (liste d'inquietudes → plan d'action → lacher prise).

---

## 4. ARCHITECTURE TECHNIQUE

### Stack principal

```
Flutter 3.x (Dart)
├── State Management : Riverpod 2.x
├── Navigation : GoRouter
├── Local DB : Drift (SQLite)
├── Backend : Supabase
├── Audio : just_audio + audio_service
├── Notifications : flutter_local_notifications + FCM
├── Charts : fl_chart
└── Animations : Lottie + Flutter built-in
```

### Pourquoi Riverpod

- Architecture reactif claire (providers typed)
- Pas de boilerplate excessif (vs BLoC)
- Testabilite native (provider overrides)
- Communaute active, documentation francaise disponible

### Backend : Supabase (recommande) vs Firebase

| Critere | Supabase | Firebase |
|---------|----------|----------|
| Base de donnees | PostgreSQL (relationnel) | Firestore (NoSQL) |
| Donnees de sommeil | Relations naturelles (user → diary → entries) | Documents imbriques, denormalisation |
| Auth | Built-in, magic link, social | Built-in, social |
| Realtime | WebSocket natif | Realtime listeners |
| Hebergement donnees | EU (Frankfurt) | US par defaut (EU possible) |
| RGPD | Conforme EU natif | Possible mais complexe |
| Prix | Gratuit jusqu'a 50K MAU | Gratuit jusqu'a limits Spark |
| Row Level Security | Natif PostgreSQL | Firestore rules |
| Open source | Oui | Non |

**Recommandation : Supabase** pour la conformite RGPD, le modele relationnel adapte aux donnees de sommeil, et l'hebergement EU natif.

### Modele de donnees

```sql
-- Profil utilisateur
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now(),
  display_name TEXT,
  timezone TEXT DEFAULT 'Europe/Paris',
  wake_time TIME NOT NULL,              -- Heure de lever fixe
  program_start_date DATE,              -- Debut du programme
  current_week INT DEFAULT 1,           -- Semaine actuelle (1-8)
  isi_initial INT,                      -- Score ISI initial (0-28)
  isi_week4 INT,                        -- Score ISI semaine 4
  isi_final INT,                        -- Score ISI semaine 8
  notification_evening BOOLEAN DEFAULT true,
  notification_morning BOOLEAN DEFAULT true,
  sleep_window_start TIME,              -- Heure coucher recommandee
  sleep_window_end TIME,                -- = wake_time
  subscription_status TEXT DEFAULT 'trial', -- trial, active, expired
  subscription_expires_at TIMESTAMPTZ
);

-- Journal du sommeil (1 entree par jour)
CREATE TABLE sleep_diary (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  date DATE NOT NULL,                   -- Date de la nuit (= date du coucher)
  bedtime TIMESTAMPTZ,                  -- Heure a laquelle l'utilisateur se couche
  sleep_onset_latency INT,              -- Minutes pour s'endormir (estimation)
  awakenings INT DEFAULT 0,             -- Nombre de reveils nocturnes
  wake_after_sleep_onset INT DEFAULT 0, -- Minutes eveille apres reveils
  final_wake_time TIMESTAMPTZ,          -- Heure du dernier reveil
  rise_time TIMESTAMPTZ,               -- Heure de lever effective
  perceived_quality INT CHECK (perceived_quality BETWEEN 1 AND 5),
  mood_evening INT CHECK (mood_evening BETWEEN 1 AND 5),
  notes TEXT,
  -- Calculs automatiques
  time_in_bed INT GENERATED ALWAYS AS (
    EXTRACT(EPOCH FROM (rise_time - bedtime)) / 60
  ) STORED,
  total_sleep_time INT,                 -- TIB - SOL - WASO (calcule cote app)
  sleep_efficiency NUMERIC(5,2),        -- TST / TIB * 100 (calcule cote app)
  created_at TIMESTAMPTZ DEFAULT now(),
  UNIQUE(user_id, date)
);

-- Progression du programme
CREATE TABLE program_progress (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  week INT NOT NULL CHECK (week BETWEEN 1 AND 8),
  day INT NOT NULL CHECK (day BETWEEN 1 AND 7),
  session_type TEXT NOT NULL,           -- 'education', 'cognitive', 'relaxation', 'checkin'
  session_id TEXT NOT NULL,             -- Reference vers le contenu
  completed BOOLEAN DEFAULT false,
  completed_at TIMESTAMPTZ,
  UNIQUE(user_id, week, day, session_type)
);

-- Sessions / Contenu CBT-I
CREATE TABLE sessions (
  id TEXT PRIMARY KEY,                  -- ex: 'edu_w1_circadian', 'cog_w3_catastrophe'
  week INT NOT NULL,
  day INT,                              -- NULL = disponible toute la semaine
  pillar TEXT NOT NULL,                 -- 'education', 'restriction', 'stimulus', 'cognitive', 'hygiene'
  title TEXT NOT NULL,
  description TEXT,
  content_type TEXT NOT NULL,           -- 'lesson', 'exercise', 'audio', 'quiz'
  content_json JSONB,                   -- Contenu structure (texte, questions, etapes)
  duration_minutes INT,
  audio_url TEXT,                       -- URL si audio
  sort_order INT DEFAULT 0
);

-- Ajustements fenetre de sommeil (historique)
CREATE TABLE sleep_window_history (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  week INT NOT NULL,
  sleep_efficiency_avg NUMERIC(5,2),    -- Efficacite moyenne de la semaine
  previous_window_minutes INT,          -- Fenetre precedente
  new_window_minutes INT,               -- Nouvelle fenetre
  adjustment TEXT,                       -- '+15min', '-15min', 'unchanged'
  applied_at TIMESTAMPTZ DEFAULT now()
);

-- Exercices cognitifs (journal de pensees)
CREATE TABLE thought_records (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  date DATE NOT NULL,
  situation TEXT,                        -- "Je me suis reveille a 3h"
  automatic_thought TEXT,               -- "Je ne vais jamais me rendormir"
  emotion TEXT,                         -- "Anxiete"
  emotion_intensity INT CHECK (emotion_intensity BETWEEN 1 AND 10),
  evidence_for TEXT,                    -- Preuves POUR la pensee
  evidence_against TEXT,                -- Preuves CONTRE la pensee
  alternative_thought TEXT,             -- Pensee alternative equilibree
  emotion_intensity_after INT CHECK (emotion_intensity_after BETWEEN 1 AND 10),
  created_at TIMESTAMPTZ DEFAULT now()
);
```

### Notifications (critiques pour la CBT-I)

Les notifications sont le nerf de la guerre pour l'adherence au programme.

| Notification | Timing | Contenu | Priorite |
|-------------|--------|---------|----------|
| **Rappel session du soir** | H-2 avant coucher | "Votre session du jour vous attend" | P0 |
| **Heure de coucher** | = sleep_window_start | "C'est l'heure d'aller au lit. Bonne nuit." | P0 |
| **Reveil / journal** | = wake_time | "Bonjour ! 60 secondes pour votre journal." | P0 |
| **Journal non rempli** | wake_time + 2h | "N'oubliez pas votre journal du sommeil" | P1 |
| **Bilan hebdomadaire** | Dimanche 18h | "Bilan de la semaine : votre efficacite est de X%" | P1 |
| **Encouragement streak** | Apres 3, 7, 14, 21 jours | "X jours consecutifs ! Continuez." | P2 |

**Implementation technique :**
- `flutter_local_notifications` pour les alarmes locales (coucher, lever)
- Firebase Cloud Messaging (FCM) via Supabase Edge Functions pour les notifications push
- `android_alarm_manager_plus` pour les alarmes fiables sur Android (meme en mode Doze)
- Gestion du fuseau horaire (`Europe/Paris` par defaut, configurable)

### Audio

- **Stockage** : Supabase Storage (bucket prive, URLs signees)
- **Format** : MP3 128kbps (compromis qualite/taille, ~1 Mo/min)
- **Cache local** : telechargement anticipatif des audios de la semaine en cours
- **Lecture** : `just_audio` + `audio_service` pour playback en arriere-plan
- **Contenu MVP** : 3 seances (body scan 10 min, relaxation musculaire 15 min, coherence cardiaque 5 min)

### Architecture locale (offline-first)

```
Drift (SQLite local)
├── Cache du journal du sommeil (7 derniers jours)
├── Programme et sessions (pre-charge)
├── Audio (cache)
└── Sync avec Supabase quand connecte
```

L'app doit fonctionner **hors ligne** pour les fonctions critiques : journal du sommeil, consultation du programme, lecture audio (cache). La synchronisation se fait en arriere-plan quand la connexion est disponible.

---

## 5. ECRANS MVP

### 5.1 Onboarding (3 ecrans + ISI)

**Ecran 1 — Bienvenue**
- Titre : "Retrouvez le sommeil en 8 semaines"
- Sous-titre : "Programme CBT-I, le traitement de reference recommande par la HAS"
- Illustration : nuit etoilee apaisante
- CTA : "Commencer"

**Ecran 2 — Comment ca marche**
- 3 etapes illustrees :
  1. "Remplissez votre journal du sommeil chaque matin (60 sec)"
  2. "Suivez votre programme personnalise chaque soir (10 min)"
  3. "Retrouvez un sommeil de qualite en 8 semaines"
- CTA : "Evaluer mon sommeil"

**Ecran 3 — Questionnaire ISI (Insomnia Severity Index)**
- 7 questions validees scientifiquement (score 0-28)
- Format : sliders ou boutons radio, une question par sous-ecran
- Questions :
  1. Difficulte a s'endormir (0-4)
  2. Difficulte a rester endormi (0-4)
  3. Reveil precoce (0-4)
  4. Satisfaction du sommeil (0-4)
  5. Impact sur le fonctionnement diurne (0-4)
  6. Impact remarque par les autres (0-4)
  7. Inquietude causee par les troubles du sommeil (0-4)
- Resultat : score + interpretation (0-7 normal, 8-14 leger, 15-21 modere, 22-28 severe)

**Ecran 4 — Configuration**
- Heure de lever souhaitee (time picker)
- Preferences de notification (soir, matin)
- Inscription (email + mot de passe ou magic link)
- CTA : "Demarrer mon programme"

### 5.2 Dashboard sommeil (ecran principal)

```
┌─────────────────────────────────┐
│  Bonjour [prenom]         S3/J4 │  <- Semaine 3, Jour 4
│                                  │
│  ┌──────────────────────────┐   │
│  │   Score sommeil : 72%     │   │  <- Efficacite de sommeil moyenne 7j
│  │   ████████░░░░            │   │
│  │   +8% cette semaine       │   │
│  └──────────────────────────┘   │
│                                  │
│  🔥 12 jours consecutifs        │  <- Streak journal
│                                  │
│  ┌──────────────────────────┐   │
│  │  Graphique efficacite 4s  │   │  <- fl_chart, courbe 28j
│  │  ╱─╲  ╱──────╱           │   │
│  └──────────────────────────┘   │
│                                  │
│  ┌──────────┐ ┌──────────┐     │
│  │ Session   │ │ Journal  │     │
│  │ du jour   │ │ du matin │     │  <- 2 CTA principaux
│  │ 10 min    │ │ 60 sec   │     │
│  └──────────┘ └──────────┘     │
│                                  │
│  Fenetre de sommeil :           │
│  23:30 → 06:30 (7h)            │  <- Restriction actuelle
│                                  │
├─────────────────────────────────┤
│  🏠  📓  ▶️  📅  👤              │  <- Bottom nav
│ Home Journal Session Programme Profil │
└─────────────────────────────────┘
```

### 5.3 Journal du sommeil (entree matinale)

**Flow rapide, 5 champs :**

1. **Heure de coucher** — Time picker, pre-rempli avec la veille si dispo
2. **Temps d'endormissement** — Slider (0, 5, 10, 15, 20, 30, 45, 60, 90+ min)
3. **Reveils nocturnes** — Counter (0, 1, 2, 3, 4, 5+) + duree totale eveillee
4. **Heure de lever** — Time picker, pre-rempli avec wake_time
5. **Qualite ressentie** — 5 emojis (tres mauvais → excellent)

**Apres validation :**
- Affichage immediat : "Efficacite de sommeil cette nuit : 78%"
- Comparaison avec la semaine precedente
- Encouragement adapte

**Historique :**
- Vue liste des 7 derniers jours
- Tap pour voir le detail d'une nuit

### 5.4 Session du jour

**Structure type d'une session :**

```
┌─────────────────────────────────┐
│  ← Retour              S3 / J4  │
│                                  │
│  Semaine 3 — Session 4          │
│  ─────────────────────          │
│  "Les pensees qui empechent     │
│   de dormir"                     │
│                                  │
│  Type : Exercice cognitif        │
│  Duree : ~10 min                │
│                                  │
│  ┌──────────────────────────┐   │
│  │                          │   │
│  │  [Contenu de la session] │   │  <- Texte, quiz, exercice interactif
│  │                          │   │
│  │  Etape 1/4               │   │
│  │  ██░░░░░░░░              │   │
│  │                          │   │
│  └──────────────────────────┘   │
│                                  │
│  ┌──────────────────────────┐   │
│  │    Terminer la session    │   │
│  └──────────────────────────┘   │
└─────────────────────────────────┘
```

**Types de sessions :**
- **Lecon** : texte illustre, scrollable, quiz de comprehension a la fin
- **Exercice cognitif** : formulaire guide etape par etape (pensee → preuves → alternative)
- **Audio** : lecteur integre avec minuteur, progression visuelle
- **Checklist** : liste de taches comportementales a cocher (ex: hygiene du sommeil)

### 5.5 Programme (timeline 8 semaines)

```
┌─────────────────────────────────┐
│  Mon programme                   │
│                                  │
│  S1 ● Comprendre son insomnie   │  ✅ Complete
│  S2 ● Restructurer son sommeil  │  ✅ Complete
│  S3 ◉ Les pensees nocturnes     │  ← En cours (J4/7)
│      ├── J1 ✅ Lecon            │
│      ├── J2 ✅ Exercice         │
│      ├── J3 ✅ Audio            │
│      ├── J4 ○  Exercice ← AUJOURD'HUI
│      ├── J5 ○  Lecon            │
│      ├── J6 ○  Exercice         │
│      └── J7 ○  Bilan semaine    │
│  S4 ○ Worry time                │
│  S5 ○ Relaxation avancee        │  🔒 Verrouille
│  S6 ○ Consolider                │  🔒
│  S7 ○ Autonomie                 │  🔒
│  S8 ○ Bilan final               │  🔒
│                                  │
└─────────────────────────────────┘
```

- Semaines passees : resume + possibilite de revoir
- Semaine en cours : detail jour par jour
- Semaines futures : verrouillees (progression lineaire pour l'adherence)

### 5.6 Relaxation audio

```
┌─────────────────────────────────┐
│  Relaxation                      │
│                                  │
│  ┌──────────────────────────┐   │
│  │  🧘 Body Scan            │   │
│  │  Scannez votre corps     │   │
│  │  10 min                  │   │
│  └──────────────────────────┘   │
│                                  │
│  ┌──────────────────────────┐   │
│  │  💪 Relaxation musculaire │   │
│  │  Tension-relachement     │   │
│  │  15 min                  │   │
│  └──────────────────────────┘   │
│                                  │
│  ┌──────────────────────────┐   │
│  │  🫁 Coherence cardiaque  │   │  <- Synergie Respir
│  │  Respiration guidee 5-5  │   │
│  │  5 min                   │   │
│  └──────────────────────────┘   │
│                                  │
│  ┌──────────────────────────┐   │
│  │  💡 Decouvrez Respir     │   │  <- Cross-promo discrete
│  │  App de coherence        │   │
│  │  cardiaque complete      │   │
│  └──────────────────────────┘   │
│                                  │
└─────────────────────────────────┘
```

**Lecteur audio :**
- Play/Pause, barre de progression
- Timer optionnel (arret automatique)
- Playback en arriere-plan (notification persistante)
- Volume independant

### 5.7 Profil et settings

- **Profil** : prenom, email, date de debut du programme
- **Mon sommeil** : score ISI actuel, historique des scores
- **Notifications** : activer/desactiver, heures personnalisees
- **Fenetre de sommeil** : visualisation de l'historique des ajustements
- **Abonnement** : statut, gestion, restauration d'achats
- **A propos** : mentions legales, disclaimer medical, credits scientifiques
- **Aide** : FAQ, contact support
- **Deconnexion**

---

## 6. MONETISATION

### Modele freemium avec semaine 1 gratuite

| Acces | Gratuit (Semaine 1) | Premium |
|-------|---------------------|---------|
| Questionnaire ISI | Oui | Oui |
| Journal du sommeil | Oui | Oui |
| Dashboard basique | Oui | Oui |
| Session S1 (education) | Oui | Oui |
| Programme S2-S8 | Non | Oui |
| Restriction de sommeil personnalisee | Non | Oui |
| Exercices cognitifs | Non | Oui |
| Audios relaxation | 1 seance decouverte | Toutes |
| Bilan ISI mi-parcours et final | Non | Oui |
| Historique complet | 7 jours | Illimite |

### Tarification

| Formule | Prix | Prix/mois | vs Calm |
|---------|------|-----------|---------|
| **Mensuel** | 6,99 EUR/mois | 6,99 EUR | -17% |
| **Annuel** | 49,99 EUR/an | 4,17 EUR | -29% |
| ~~A vie~~ | ~~Non prevu au MVP~~ | — | — |

### Pourquoi ce pricing fonctionne

1. **Moins cher que Calm** (69,99 EUR/an) et Headspace (69,99 EUR/an)
2. **Plus de valeur percue** : programme therapeutique vs contenu de bien-etre generique
3. **Duree naturelle** : le programme dure 8 semaines. A 6,99 EUR/mois, le cout total est ~14 EUR pour le programme complet. C'est le prix d'un livre.
4. **Bien en-dessous d'une consultation** : 1 seance chez un psychologue du sommeil = 60-90 EUR
5. **Le paywall tombe apres le hook** : la semaine 1 gratuite demontre la valeur (journal, education, premier score)

### Potentiel de monetisation secondaire

- **Partenariat mutuelles** : les mutuelles francaises remboursent de plus en plus les programmes de sante numerique. SleepCoach pourrait etre prescrit ou rembourse via un partenariat (MGEN, Harmonie Mutuelle, etc.)
- **Entreprises / QVT** : le sommeil est un enjeu de qualite de vie au travail. Licences B2B pour offrir SleepCoach aux salaries.
- **Contenu additionnel** : sessions de maintien post-programme, thematiques specifiques (insomnie de grossesse, jet lag, travail poste)

---

## 7. VALIDATION MEDICALE

### Ce qui necessite une validation medicale

| Element | Niveau de risque | Action requise |
|---------|-----------------|----------------|
| Protocole CBT-I (structure 8 semaines) | **ELEVE** | Validation par un medecin/psychologue du sommeil |
| Algorithme de restriction de sommeil | **ELEVE** | Validation formules + garde-fous par specialiste |
| Contenu educatif (lecons) | **MOYEN** | Relecture par specialiste |
| Scripts audio relaxation | **FAIBLE** | Relecture optionnelle |
| Exercices cognitifs | **MOYEN** | Validation par psychologue TCC |
| Questionnaire ISI | **FAIBLE** | Instrument valide, pas de modification |
| Seuil minimal fenetre de sommeil (5h) | **ELEVE** | Validation par specialiste |

### Comment trouver un partenaire sommeil

**Profil recherche** : medecin ou psychologue specialise en medecine du sommeil, pratiquant la CBT-I en clinique.

**Canaux de recherche :**
1. **Societe Francaise de Recherche et Medecine du Sommeil (SFRMS)** — annuaire des membres
2. **Institut National du Sommeil et de la Vigilance (INSV)** — reseau de specialistes
3. **LinkedIn** : recherche "CBT-I" + "France" ou "medecine du sommeil" + "TCC"
4. **CHU / centres du sommeil** : contacter les responsables d'unite (Paris, Lyon, Bordeaux, Montpellier)
5. **Reseau Morphee** : association specialisee, basee en Ile-de-France

**Modele de partenariat propose :**
- Validation initiale du protocole : honoraires forfaitaires (1500-3000 EUR)
- Mention "Programme valide par Dr [Nom], specialiste du sommeil" dans l'app
- Eventuellement : royalties sur les abonnements (2-5%) ou advisory board

### Strategie de disclaimer

**Disclaimer obligatoire (onboarding + settings + store) :**

> SleepCoach est un programme d'education a la sante base sur la Therapie Cognitive et Comportementale de l'Insomnie (CBT-I). Il ne remplace pas un avis medical. Si vous souffrez d'apnee du sommeil, de depression severe, d'epilepsie, de trouble bipolaire, ou si vous prenez des medicaments pour le sommeil, consultez votre medecin avant d'utiliser cette application. La restriction de sommeil peut entrainer une somnolence temporaire — ne conduisez pas si vous vous sentez somnolent.

**Exclusions a l'onboarding :**
- Question de depistage : "Prenez-vous des medicaments pour dormir ?" → message adapte
- Question : "Avez-vous ete diagnostique avec une apnee du sommeil ?" → redirection vers medecin
- Si ISI > 25 (insomnie tres severe) → message : "Votre score suggere une insomnie severe. Nous vous recommandons de consulter un specialiste du sommeil en parallele de ce programme."

**Statut juridique :**
- SleepCoach est une **application de bien-etre / education a la sante**, pas un dispositif medical
- La CBT-I delivree par app sans supervision medicale directe ne releve pas du reglement sur les dispositifs medicaux (EU MDR) tant qu'elle ne pretend pas diagnostiquer ou traiter une pathologie
- A surveiller : evolution de la reglementation europeenne sur les DTx (Digital Therapeutics)

---

## 8. METRIQUES

### Metrique primaire

**Amelioration du score ISI apres 4 semaines**

- ISI initial (onboarding) vs ISI semaine 4
- Objectif : **reduction moyenne de 5 points** (= amelioration cliniquement significative)
- Mesure : ISI integre a la session de bilan S4

### Metriques secondaires

| Metrique | Objectif MVP | Mesure |
|----------|-------------|--------|
| **Retention J7** | > 60% | % d'utilisateurs actifs 7 jours apres inscription |
| **Retention J28** | > 35% | % d'utilisateurs actifs 28 jours apres inscription |
| **Completion S1 (gratuite)** | > 70% | % d'utilisateurs ayant termine la semaine 1 |
| **Conversion trial → paid** | > 8% | % d'utilisateurs S1 qui souscrivent |
| **Completion programme (S8)** | > 25% | % d'utilisateurs payants terminant les 8 semaines |
| **Journal quotidien** | > 80% des jours | % de jours avec journal rempli (utilisateurs actifs) |
| **NPS** | > 40 | Enquete in-app a S4 et S8 |
| **Note store** | > 4.5/5 | Google Play + App Store |

### Go / No-Go apres 8 semaines

L'evaluation se fait 8 semaines apres le lancement, avec les premiers utilisateurs ayant termine le programme complet.

| Critere | Go | No-Go |
|---------|-----|-------|
| ISI reduction moyenne | >= 4 points | < 2 points |
| Retention J7 | >= 50% | < 30% |
| Conversion trial → paid | >= 5% | < 2% |
| Completion programme | >= 15% | < 5% |
| NPS | >= 30 | < 10 |
| Note store | >= 4.0 | < 3.5 |

**Si Go** : investir dans le marketing, ajouter du contenu, explorer partenariat mutuelle.
**Si No-Go** : analyser les points de churn, pivoter (contenu ? pricing ? UX ?) ou abandonner.

---

## 9. PLANNING (8 semaines)

### Semaine 1 — Fondations

**Dev :**
- Setup projet Flutter + Supabase
- Architecture Riverpod + GoRouter
- Schema de base de donnees + migrations
- Auth (email/password + magic link)
- CI/CD (GitHub Actions → builds iOS/Android)

**Contenu :**
- Contact specialiste sommeil pour validation protocole
- Redaction structure detaillee des 8 semaines de contenu

### Semaine 2 — Onboarding + Journal

**Dev :**
- Ecrans onboarding (3 ecrans + ISI)
- Questionnaire ISI (7 questions, calcul score)
- Configuration utilisateur (heure lever, notifications)
- Journal du sommeil (formulaire + sauvegarde)

**Contenu :**
- Redaction lecons semaine 1 (education sommeil)
- Premiere passe du disclaimer

### Semaine 3 — Dashboard + Programme

**Dev :**
- Dashboard sommeil (score, streak, graphique efficacite)
- Calcul automatique efficacite de sommeil
- Vue programme 8 semaines (timeline)
- Session du jour (affichage contenu)

**Contenu :**
- Redaction lecons semaine 2 (restriction, stimulus)
- Redaction exercices cognitifs (templates)

### Semaine 4 — Restriction de sommeil + Notifications

**Dev :**
- Algorithme fenetre de sommeil (calcul, ajustement)
- Systeme de notifications (coucher, lever, session, journal)
- Historique fenetre de sommeil
- Gestion offline (Drift sync)

**Contenu :**
- Redaction lecons semaines 3-4
- Enregistrement audio body scan (10 min)

### Semaine 5 — Cognitif + Audio

**Dev :**
- Exercices cognitifs interactifs (journal pensees, worry time)
- Lecteur audio (just_audio + background)
- Ecran relaxation (liste audio, lecteur)
- Cache audio local

**Contenu :**
- Enregistrement audio relaxation musculaire (15 min)
- Enregistrement audio coherence cardiaque (5 min)
- Redaction lecons semaines 5-6

### Semaine 6 — Monetisation + Profil

**Dev :**
- Integration in-app purchases (RevenueCat recommande)
- Paywall (apres S1 gratuite)
- Ecran profil et settings
- Gestion abonnement (statut, restauration)
- Bilan S4 (ISI mi-parcours)

**Contenu :**
- Redaction lecons semaines 7-8
- Redaction bilan final
- Finalisation disclaimer + mentions legales

### Semaine 7 — Polish + Tests

**Dev :**
- Tests unitaires et d'integration
- Correction de bugs
- Optimisation performance (temps de chargement, animations)
- Accessibilite (contraste, taille texte, VoiceOver/TalkBack)
- Analytics (Mixpanel ou Posthog)

**Contenu :**
- Validation finale du protocole avec le specialiste
- Relecture complete de tout le contenu
- Fiches store (textes, screenshots)

### Semaine 8 — Lancement

**Dev :**
- Tests beta (TestFlight + Google Play internal testing)
- Corrections post-beta
- Soumission App Store + Google Play
- Landing page (optionnel, sinon page store)

**Contenu :**
- FAQ
- Email de bienvenue
- Communication lancement (reseaux, forums sante)

### Timeline contenu (en parallele du dev)

| Semaine dev | Contenu a produire |
|-------------|-------------------|
| S1-S2 | Structure 8 semaines + lecons S1-S2 |
| S3 | Lecons S3-S4 + templates exercices cognitifs |
| S4 | Lecons S5-S6 + enregistrement audio 1/3 |
| S5 | Enregistrement audios 2/3 et 3/3 + lecons S7-S8 |
| S6 | Bilan, disclaimer, mentions legales |
| S7 | Validation specialiste + relecture complete |
| S8 | Fiches store, FAQ, communication lancement |

---

## 10. RISQUES ET MITIGATIONS

### Risques elevees

| Risque | Impact | Probabilite | Mitigation |
|--------|--------|-------------|------------|
| **Impossible de trouver un specialiste partenaire dans les delais** | Retard lancement, credibilite | Moyenne | Commencer la recherche des la semaine 1. Plan B : valider avec la litterature scientifique publiee et ajouter "en cours de validation clinique". Contacter 5+ specialistes en parallele. |
| **Restriction de sommeil mal implementee = danger** | Risque sante utilisateur, responsabilite juridique | Faible | Garde-fous stricts : min 5h, avertissements, question de depistage a l'onboarding, disclaimer clair. Pas de restriction pour les profils a risque. |
| **Churn massif apres semaine 1 gratuite (refus de payer)** | Modele economique non viable | Haute | Prix agressif (6,99 EUR/mois), valeur demontree en S1 (score, education, journal). Test A/B sur le pricing. Essai 7 jours gratuits comme alternative au modele S1 gratuite. |
| **Apple/Google rejettent l'app (claim medical)** | Retard lancement | Faible | Positionner comme "education a la sante" et non "traitement medical". Disclaimers conformes aux guidelines store. Precedents : Headspace, Calm, Woebot sont acceptes. |

### Risques moyens

| Risque | Impact | Probabilite | Mitigation |
|--------|--------|-------------|------------|
| **Faible adherence au journal quotidien** | Donnees insuffisantes pour la restriction, programme inefficace | Moyenne | UX optimise (< 60 sec), notifications intelligentes, gamification legere (streak), feedback immediat (score efficacite). |
| **Calm ou Headspace lancent une feature CBT-I en francais** | Perte d'avantage concurrentiel | Faible (court terme) | First-mover advantage, expertise CBT-I profonde vs feature superficielle, pricing plus agressif, credibilite specialiste. |
| **Contenu CBT-I trop complexe pour un format mobile** | Engagement faible, incomprehension | Moyenne | Test utilisateur des la S3, langage simple, illustrations, sessions courtes (5-15 min max), progression tres graduelle. |
| **Problemes de notifications Android (Doze mode, constructeurs chinois)** | Utilisateurs manquent les rappels critiques | Haute | `android_alarm_manager_plus`, instructions de whitelisting dans l'onboarding, guide par constructeur (Xiaomi, Huawei, Samsung). |
| **Reglementation DTx (Digital Therapeutics) en Europe** | Obligation de certification dispositif medical | Faible (2-3 ans) | Veille reglementaire, positionnement "education" et non "therapeutique", pivot possible vers certification si le marche l'exige. |

### Risques faibles

| Risque | Impact | Probabilite | Mitigation |
|--------|--------|-------------|------------|
| **Complexite technique sous-estimee** | Retard de 2-4 semaines | Moyenne | Scope MVP strict (pas de tracking capteur, pas d'IA). Architecture simple. Features out clairement definies. |
| **Qualite audio insuffisante** | Experience degradee | Faible | Investir dans un micro correct (200-300 EUR) ou faire appel a un voiceover pro (500-800 EUR pour 30 min). |
| **RGPD : donnees de sante** | Amende, reputation | Faible | Supabase EU, pas de partage de donnees, consentement explicite, droit a l'effacement implemente. Les donnees de journal de sommeil auto-declarees ne sont pas des "donnees de sante" au sens strict du RGPD (pas de diagnostic medical). |

---

## ANNEXES

### A. Questionnaire ISI (Insomnia Severity Index)

Le questionnaire ISI est un instrument valide et libre de droits, utilise dans la recherche et la pratique clinique.

**7 questions, echelle 0-4 pour chaque :**

1. Difficulte a vous endormir
2. Difficulte a rester endormi(e)
3. Probleme de reveil trop tot le matin
4. Dans quelle mesure etes-vous satisfait(e) de votre sommeil actuel ?
5. Dans quelle mesure vos difficultes de sommeil interferent-elles avec votre fonctionnement quotidien ?
6. Dans quelle mesure vos difficultes de sommeil sont-elles remarquees par les autres ?
7. Dans quelle mesure etes-vous inquiet(e) / preoccupe(e) par vos difficultes de sommeil actuelles ?

**Interpretation :**
- 0-7 : Pas d'insomnie cliniquement significative
- 8-14 : Insomnie legere (sub-clinique)
- 15-21 : Insomnie moderee (clinique)
- 22-28 : Insomnie severe (clinique)

**Usage dans SleepCoach** : onboarding (baseline), semaine 4 (mi-parcours), semaine 8 (final).

### B. Formule d'efficacite du sommeil

```
Efficacite du Sommeil (%) = (Temps de Sommeil Total / Temps Passe au Lit) x 100

Ou :
- Temps Passe au Lit (TIB) = Heure de lever - Heure de coucher
- Temps de Sommeil Total (TST) = TIB - Latence d'endormissement - Eveils nocturnes

Exemple :
- Coucher : 23h00, Lever : 07h00 → TIB = 8h = 480 min
- Latence : 30 min, Eveils : 45 min → TST = 480 - 30 - 45 = 405 min
- Efficacite = 405/480 = 84.4%
```

**Objectif CBT-I** : efficacite > 85% = sommeil consolide.

### C. Algorithme de restriction de sommeil

```
1. Semaine 1 : collecter les donnees du journal (7 nuits)
2. Calculer TST moyen de la semaine
3. Fenetre initiale = TST moyen + 30 min (minimum 5h00)
4. Heure de lever = fixe (definie par l'utilisateur)
5. Heure de coucher = Heure de lever - Fenetre

Ajustement hebdomadaire (chaque dimanche) :
- Si Efficacite moyenne >= 90% : fenetre + 15 min (coucher 15 min plus tot)
- Si Efficacite moyenne 85-89% : pas de changement
- Si Efficacite moyenne < 85% : fenetre - 15 min (coucher 15 min plus tard)
- Fenetre ne descend JAMAIS en dessous de 5h00

Arret de la restriction :
- Quand efficacite >= 85% ET fenetre >= 7h00 pendant 2 semaines consecutives
- Ou a la fin du programme (S8)
```

### D. References scientifiques cles

1. Morin, C.M. et al. (2006). "Psychological and behavioral treatment of insomnia." *Sleep*, 29(11), 1398-1414.
2. Trauer, J.M. et al. (2015). "Cognitive Behavioral Therapy for Chronic Insomnia: A Systematic Review and Meta-analysis." *Annals of Internal Medicine*, 163(3), 191-204.
3. Espie, C.A. et al. (2012). "A Randomized, Placebo-Controlled Trial of Online Cognitive Behavioral Therapy for Chronic Insomnia Disorder Delivered via an Automated Media-Rich Web Application." *Sleep*, 35(6), 769-781.
4. HAS (2006). "Prise en charge du patient adulte se plaignant d'insomnie en medecine generale." Recommandations de bonne pratique.
5. Bastien, C.H. et al. (2001). "Validation of the Insomnia Severity Index as an outcome measure for insomnia research." *Sleep Medicine*, 2(4), 297-307.
