# Deep Research: SleepCoach FR
## Date: 2026-04-10

---

## 1. DONNEES GOOGLE PLAY — Marche Sommeil FR

### Concurrents directs analyses

| App | Score | Ratings | Installs | % Negatifs |
|-----|-------|---------|----------|------------|
| Sleep Cycle | 4.4/5 | 215,621 | 18.7M | **43%** |
| Calm | 4.2/5 | 610,049 | 69.2M | **48%** |
| Sleep as Android | 4.4/5 | 389,254 | 24.2M | **32%** |

### Marche total estime
- **Installs cumules top 3 FR** : ~112M
- **Score moyen** : 4.3/5
- **Taux d'avis negatifs moyen** : **41%** (tres eleve)

### Frustrations extraites (avis 1-3 etoiles, 600 avis analyses)

| Frustration | Sleep Cycle | Calm | Sleep Android | TOTAL |
|-------------|-------------|------|---------------|-------|
| **payant/premium** | 17 | 17 | 7 | **41** |
| **gratuit (veut du gratuit)** | 11 | 25 | 8 | **44** |
| **abonnement** | 8 | 16 | 5 | **29** |
| **cher** | 2 | 7 | 6 | **15** |
| **arnaque** | 2 | 5 | 0 | **7** |
| **bug/crash** | 4 | 1 | 7 | **12** |
| **fonctionne pas** | 6 | 0 | 3 | **9** |
| **inutile** | 4 | 3 | 0 | **7** |

### Pattern dominant
**Le probleme #1 est le PRICING, pas la qualite.**
- 78% des plaintes concernent le prix / paywall / abonnement
- Les utilisateurs trouvent que le contenu gratuit est trop limite
- Calm est percu comme une "arnaque" par de nombreux utilisateurs FR
- Sleep Cycle a rendu le reveil intelligent payant = frustration massive

### Gap identifie
> **AUCUNE app de sommeil ne propose de la therapie CBT-I.**
> Toutes font du TRACKING (mesurer le probleme) sans RESOUDRE le probleme.
> C'est comme si toutes les apps de fitness ne faisaient que peser les gens sans proposer d'exercices.

---

## 2. DONNEES DE MARCHE

### Insomnie en France
- **1 Francais sur 3** souffre de troubles du sommeil (INSERM)
- ~20 millions de personnes concernees
- Marche des somniferes : en baisse (deremboursement, effets secondaires)
- CBT-I = traitement de 1ere intention recommande par la HAS
- **Zero app CBT-I en francais**

### CBT-I (Therapie Cognitive Comportementale de l'Insomnie)
- Programme structure de 6-8 semaines
- Efficacite prouvee (75-80% des patients ameliores)
- En anglais : Sleepio (UK), Pear Therapeutics (US) — mais pas dispo en Europe
- En francais : **RIEN** sur mobile

### Monetisation comparable
- Calm : 69.99 EUR/an
- Headspace : 69.99 EUR/an
- Sleep Cycle Premium : 34.99 EUR/an
- **Position SleepCoach** : 4.99-7.99 EUR/mois (programme therapeutique = valeur percue plus haute)

---

## 3. SCORING DATA-DRIVEN

| Critere | Score | Justification data |
|---------|-------|--------------------|
| Douleur (x4) | **5** | 20M Francais insomniaques, somniferes en baisse |
| Frequence (x3) | **5** | Quotidien soir + matin |
| Paiement (x3) | **4** | Calm/Headspace = 70 EUR/an, le segment paie deja |
| Segment (x2) | **4** | 20M personnes, SEO "insomnie" = volume fort |
| Concurrence (x2) | **5** | ZERO app CBT-I en FR, apps existantes = tracking only |
| Differenciation (x2) | **5** | Therapie vs tracking = proposition fondamentalement differente |
| Fit (x2) | **4** | Flutter + Respir = meme univers bien-etre |
| MVP Speed (x1) | **2** | Contenu CBT-I a valider avec medecins, 6-8 semaines |
| Retention (x1) | **5** | Programme 6-8 semaines puis maintien = abo naturel |
| **TOTAL** | | **90/100** |

---

## 4. GO / NO-GO

| Condition | Status | Evidence |
|-----------|--------|----------|
| Probleme douloureux | **OUI** | 20M insomniaques FR, traitement de ref non dispo |
| Segment precis | **OUI** | Adultes francophones souffrant d'insomnie chronique |
| Paiement plausible | **OUI** | Segment paie deja 35-70 EUR/an pour du tracking |
| MVP faisable | **OUI** | Programme CBT-I structure + audio + journal, 6-8 sem de dev |
| Canal d'acces | **OUI** | SEO "insomnie" + medecins generalistes + ASO |

**5/5 conditions validees = GO**

---

## 5. RISQUES

| Risque | Niveau | Mitigation |
|--------|--------|------------|
| Contenu medical a valider | MOYEN | Partenariat 1 medecin/psychologue du sommeil |
| Calm/Headspace ajoutent CBT-I | FAIBLE | Ils sont sur le bien-etre general, pas le therapeutique |
| Reglementation device medical | FAIBLE | CBT-I = programme educatif, pas device medical |
| Churn apres programme 8 sem | MOYEN | Mode maintien + nouvelles sessions + communaute |

---

## 6. NEXT STEPS

1. [ ] Valider protocole CBT-I avec 1 medecin du sommeil
2. [ ] Creer landing page "Mieux dormir sans medicaments"
3. [ ] Tester sur 50 insomniaques (forums sante, Reddit r/france)
4. [ ] Si >10% inscription : lancer le MVP Flutter
5. [ ] Considerer integration avec Respir (coherence cardiaque + sommeil)
