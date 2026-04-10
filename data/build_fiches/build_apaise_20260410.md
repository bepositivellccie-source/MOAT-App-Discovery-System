# FICHE BUILD — Apaise
*Generee automatiquement par MOAT Build Index*
*Date : 2026-04-10*
*BRI : 75.5/100 — FICHE BUILD AUTO*

---

## Indices de faisabilite

| Dimension | Score | Max | Detail |
|-----------|-------|-----|--------|
| Potentiel marche (MOAT) | 19.5 | 25 | Score MOAT 78/100 |
| Faisabilite technique | 20.0 | 20 | Stack match 5/5 |
| Vitesse de livraison | 9.0 | 15 | MVP 8 semaines |
| Avantage personnel | 12.0 | 15 | Synergie 4/5 |
| Clarte du MVP | 9.0 | 15 | Clarte 3/5 |
| Risque maitrisable | 6.0 | 10 | Risque 3/5 |
| **TOTAL BRI** | **75.5** | **100** | **FICHE BUILD AUTO** |

## Identite

- **Segment** : 600K deces/an FR
- **Monetisation** : Freemium
- **Contenu necessaire** : Oui
- **Partenaire necessaire** : Oui

## Stack technique

Identique a Respir — reutilisation maximale :
- **Framework** : Flutter + Dart + Riverpod 2.x + go_router
- **Backend** : Supabase (nouveau projet, meme compte)
- **Monetisation** : RevenueCat
- **Monitoring** : Sentry (nouvelle orga)
- **Analytics** : Firebase Analytics
- **Distribution** : Google Play Console (meme compte dev)
- **Email** : Brevo (API existante)
- **Site** : Hostinger + Cloudflare

## MVP — 8 semaines

### Estimation effort
- **Duree** : 8 semaines
- **Heures estimees** : ~48h (6h/semaine)

### Deploiement (copier le process Respir)
1. `flutter create --org com.xxx apaise`
2. Setup Supabase (nouveau projet)
3. Setup Sentry (nouveau projet, meme orga bepositive-al)
4. Config RevenueCat (nouveau projet)
5. Dev sprints
6. `flutter analyze` -> 0 issues
7. Test Samsung S23 (R5CW72R5S1P)
8. `flutter build appbundle --release`
9. Play Console -> upload AAB
10. Fiches Play Store FR + EN
11. Soumission -> validation <24h

## Cout estime

| Poste | Cout |
|-------|------|
| Infrastructure | ~0 EUR (stack existante) |
| Domaine | ~10-15 EUR/an |
| Supabase | Gratuit (<500MB) |
| RevenueCat | Gratuit (<2.5K$ MRR) |
| Contenu (si applicable) | 0-200 EUR |
| **Total an 1** | **~15-215 EUR** |

## Prochaines actions

1. Rechercher protocole + partenaire specialiste
2. Creer le contenu (scripts, audio)
3. Creer une landing page test
4. Si >10% inscription -> lancer le dev
5. Sprint 1 : Setup projet Flutter

---
*Fiche generee par MOAT Build Index v1 — 2026-04-10 14:04*
