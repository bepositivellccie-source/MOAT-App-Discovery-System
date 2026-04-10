# Guide d'Execution Realiste — Top 3 MOAT
## Base sur ta stack Respir existante

---

## TON SETUP ACTUEL (deja paye, deja configure)

| Outil | Role | Cout | Status |
|-------|------|------|--------|
| **Flutter + Dart** | Framework app | Gratuit | Expert (Respir live) |
| **Riverpod 2.x** | State management | Gratuit | En prod |
| **go_router** | Navigation | Gratuit | En prod |
| **Supabase** | Backend (BDD, auth, storage) | Gratuit <500MB | En prod |
| **RevenueCat** | Abonnements | Gratuit <2.5K$ MRR | En prod |
| **Firebase Analytics** | Metriques | Gratuit | Sprint 4 |
| **Sentry** | Crash monitoring | Gratuit | En prod |
| **Google Play Console** | Distribution Android | 25$ one-time (paye) | En prod |
| **Hostinger** | Hebergement site | ~3 EUR/mois | En prod |
| **Cloudflare** | DNS + CDN | Gratuit | En prod |
| **Brevo** | Email marketing | Gratuit <300/jour | En prod |
| **Jotform** | Formulaires | Gratuit | En prod |
| **Notion** | Documentation projet | Gratuit/Pro | En prod |
| **Asana** | Gestion taches/bugs | Gratuit | En prod |
| **Airtable** | Pipeline MOAT | Gratuit | En prod |
| **Claude Code** | Dev assistant | Abo existant | En prod |
| **Samsung S23** | Device test physique | Deja possede | En prod |

**Cout additionnel pour lancer une 2e app : quasi ZERO.**
Tu reutilises toute la stack. Seuls couts : nouveau domaine (~10 EUR/an) + temps.

---

## COMPARATIF D'EFFORT — Top 3

### 1. SleepCoach FR (Score: 90)

| Dimension | Detail |
|-----------|--------|
| **Difficulte technique** | MOYENNE |
| **Temps dev MVP** | 8 semaines (40-50h) |
| **Temps contenu** | +3-4 semaines (scripts CBT-I, audio) |
| **Temps total avant lancement** | ~12 semaines |
| **Energie/semaine** | 5-8h si a cote de Respir |
| **Risque principal** | Validation medicale du contenu |

#### Ce qui est FACILE (tu sais deja faire)
- App Flutter + Riverpod + go_router = ta stack exacte
- Backend Supabase (nouveau projet, meme compte)
- Audio (just_audio, meme que Respir)
- RevenueCat (copier la config Respir)
- Sentry (nouveau projet, meme orga)
- Google Play (meme compte dev, nouvelle app)
- Landing page + formulaire Brevo

#### Ce qui est NOUVEAU
- Contenu CBT-I (necessite 1 medecin partenaire)
- Journal du sommeil (questionnaire ISI + saisie quotidienne)
- Systeme de notifications programmees (rappels soir/matin)
- Programme progressif sur 8 semaines (logique de progression)

#### Ce qui est DUR
- Trouver et convaincre 1 specialiste du sommeil
- Creer le contenu therapeutique (scripts, audio guidage)
- Retention sur 8 semaines (UX critique)

#### Planning realiste semaine par semaine

| Semaine | Focus | Heures | Livrable |
|---------|-------|--------|----------|
| S1 | Setup projet Flutter + Supabase + data model | 6h | Squelette app + BDD |
| S2 | Onboarding + questionnaire ISI + profil | 6h | Flow inscription fonctionnel |
| S3 | Journal du sommeil (saisie matin + historique) | 8h | Journal complet |
| S4 | Dashboard sommeil (score, streak, graphiques) | 6h | Dashboard fonctionnel |
| S5 | Programme CBT-I (timeline 8 semaines, sessions) | 8h | Navigation programme |
| S6 | Audio relaxation (reutiliser archi Respir) | 5h | Player audio + contenu |
| S7 | RevenueCat + paywall + notifications | 6h | Monetisation active |
| S8 | Polish, tests S23, flutter analyze, build AAB | 5h | AAB pret |
| S9-S12 | Contenu CBT-I (scripts + enregistrements audio) | 3h/sem | 8 semaines de contenu |
| S12 | Soumission Google Play + landing page live | 4h | APP LIVE |

**Total : ~65 heures sur 12 semaines = ~5.5h/semaine**

#### Deploiement — Checklist

| Etape | Outil | Temps | Difficulte |
|-------|-------|-------|------------|
| Creer projet Supabase | supabase.com | 15min | Facile |
| Schema BDD (users, sleep_diary, programs, sessions) | Supabase SQL | 1h | Facile |
| Creer projet Sentry | sentry.io | 10min | Facile |
| Config RevenueCat (nouveau projet, memes offres) | revenuecat.com | 30min | Facile |
| Creer app Google Play Console | play.google.com/console | 1h | Deja fait |
| Domaine + DNS (sleepcoach.fr ou similar) | Hostinger + Cloudflare | 30min | Facile |
| Landing page | Hostinger upload | 20min | Deja pret |
| Brevo liste "SleepCoach" | API Brevo | 10min | Facile |
| AAB build + soumission Play Store | flutter build appbundle | 30min | Deja fait |
| Fiches Play Store FR + EN | Play Console | 2h | Deja fait |

---

### 2. CoachCRM (Score: 79)

| Dimension | Detail |
|-----------|--------|
| **Difficulte technique** | MOYENNE-HAUTE |
| **Temps dev MVP** | 6 semaines (45-55h) |
| **Temps contenu** | Quasi nul (pas de contenu editorial) |
| **Temps total avant lancement** | ~7 semaines |
| **Energie/semaine** | 7-9h |
| **Risque principal** | Scope creep (trop de features CRM) |

#### Ce qui est FACILE
- Toute la stack technique (identique a Respir)
- CRUD clients (Supabase + Riverpod)
- Profil coach
- Liste clients + recherche

#### Ce qui est NOUVEAU
- Builder de programme d'exercices (UI complexe)
- Systeme de facturation (generation PDF)
- Suivi de seances (timer + notes)
- Dashboard KPIs coach (CA, clients actifs, seances)

#### Ce qui est DUR
- UX de creation de programme (drag & drop exercices)
- Generation de factures conformes FR
- Equilibre entre simplicite et completude (CRM trap)

#### Planning realiste

| Semaine | Focus | Heures | Livrable |
|---------|-------|--------|----------|
| S1 | Setup + data model + auth | 6h | Squelette + BDD |
| S2 | Dashboard coach + liste clients | 8h | Vue principale |
| S3 | Fiche client + historique seances | 8h | Gestion client complete |
| S4 | Builder programme (simplifie) | 10h | Creation programme |
| S5 | Suivi seance + facturation basique | 8h | Tracking + PDF |
| S6 | RevenueCat + paywall + polish + build | 6h | AAB pret |
| S7 | Landing page + soumission Play Store | 4h | APP LIVE |

**Total : ~50 heures sur 7 semaines = ~7h/semaine**

---

### 3. Exercice Builder (Score: 81)

| Dimension | Detail |
|-----------|--------|
| **Difficulte technique** | FAIBLE-MOYENNE |
| **Temps dev MVP** | 4-5 semaines (30-35h) |
| **Temps contenu** | 1 semaine (exercices types) |
| **Temps total avant lancement** | ~6 semaines |
| **Energie/semaine** | 6-7h |
| **Risque principal** | Trop proche de CoachCRM (cannibalisation) |

**Note : Exercice Builder et CoachCRM pourraient etre la MEME APP.**
Exercice Builder = feature core de CoachCRM.

---

## MATRICE DE DECISION

| Critere | SleepCoach FR | CoachCRM | Exercice Builder |
|---------|--------------|----------|-----------------|
| Score MOAT | **90** | 79 | 81 |
| Signal data | **TRES FORT** | FORT | FORT |
| Temps avant lancement | 12 sem | 7 sem | 6 sem |
| Effort total | 65h | 50h | 35h |
| Difficulte technique | Moyenne | Moy-Haute | Faible |
| Contenu necessaire | **Beaucoup** | Peu | Moyen |
| Besoin partenaire | **Oui** (medecin) | Non | Non |
| Synergie avec Respir | **FORTE** | Faible | Faible |
| Potentiel revenu/user | **Eleve** (therapeutique) | Moyen (SaaS) | Moyen |
| Concurrence FR | **ZERO** | Faible | Faible |
| Risque | Moyen | Moyen | Faible |

---

## MA RECOMMANDATION

### Option A — Le pari fort (recommande)
**Lancer SleepCoach FR** comme projet principal.
- Meilleur score, zero concurrence, synergie Respir
- Plus long mais potentiel bien plus eleve
- Commence par la landing page (DEJA PRETE) pour valider

### Option B — Le quick win
**Lancer CoachCRM** comme premier projet.
- Plus rapide (7 semaines), pas besoin de partenaire medical
- Validable avec 5 interviews de coachs cette semaine
- Revenue plus previsible (SaaS)

### Option C — Les deux en parallele
- Semaines 1-7 : CoachCRM (7 semaines, ship)
- Semaines 1-12 : SleepCoach (en parallele, contenu + dev)
- Lancer CoachCRM d'abord, SleepCoach 5 semaines apres

**Option C est la meilleure si tu as 10-12h/semaine de disponible.**

---

## COUT TOTAL ESTIMÉ

| Poste | Cout | Frequence |
|-------|------|-----------|
| Domaine(s) | 10-20 EUR | /an |
| Supabase (si >500MB) | 25$/mois | Si besoin |
| RevenueCat | Gratuit | <2.5K$ MRR |
| Google Play | Deja paye | - |
| Hostinger | Deja paye | - |
| Brevo | Gratuit | <300 emails/jour |
| Sentry | Gratuit | - |
| Contenu audio SleepCoach | 0-200 EUR | Si voix pro |
| **TOTAL an 1** | **~30-250 EUR** | |

Tu as deja l'infrastructure. Le vrai investissement c'est ton TEMPS, pas l'argent.

---

## WORKFLOW DE DEPLOIEMENT (identique a Respir)

```
1. flutter create --org com.xxx nom_app
2. Setup Supabase (nouveau projet)
3. Setup Sentry (nouveau projet, meme orga)
4. Setup RevenueCat (nouveau projet)
5. Dev sprints (meme protocole que Respir)
6. flutter analyze → 0 issues
7. Test S23 → validation visuelle
8. flutter build appbundle --release
9. Play Console → nouvelle app → upload AAB
10. Fiches Play Store FR + EN (+ ES si pertinent)
11. Soumission → attente validation (<24h)
12. Sentry monitoring 48h
13. Landing page live + Brevo capture
14. Repondre aux avis Play Store sous 48h
```

Tu connais ce process par coeur. C'est le meme que Respir.
La seule difference : le contenu de l'app.
