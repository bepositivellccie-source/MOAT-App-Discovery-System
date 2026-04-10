#!/usr/bin/env python3
"""
MOAT App Discovery System — Build Readiness Index (BRI)

Indice automatique qui determine si une idee merite une fiche build.
Evalue 6 dimensions de faisabilite et genere la fiche si le seuil est atteint.

BRI = Score composite sur 100 base sur :
  1. MOAT Score (25%) — potentiel marche
  2. Faisabilite technique (20%) — peut-on le builder avec notre stack ?
  3. Vitesse de livraison (15%) — combien de temps avant le lancement ?
  4. Avantage personnel (15%) — ai-je un edge sur ce projet ?
  5. Clarte du MVP (15%) — sait-on exactement quoi builder ?
  6. Risque maitrisable (10%) — les risques sont-ils gereables ?

Seuils :
  BRI >= 75 : FICHE BUILD GENEREE AUTOMATIQUEMENT
  BRI 60-74 : Fiche partielle, validation supplementaire requise
  BRI < 60  : Pas de fiche, idee pas assez mature

Usage:
    python build_index.py --idea "SleepCoach FR" --moat-score 90 --stack-match 5 --mvp-weeks 12 --synergy 5 --mvp-clarity 5 --risk 2
    python build_index.py --from-airtable "NeuroCalm"
    python build_index.py --scan-all
"""

import argparse
import json
import os
import sys
from datetime import datetime


# ── Stack de reference (ta stack Respir) ──
REFERENCE_STACK = {
    'framework': 'Flutter + Dart',
    'state': 'Riverpod 2.x',
    'navigation': 'go_router',
    'audio': 'just_audio',
    'backend': 'Supabase',
    'monetization': 'RevenueCat',
    'monitoring': 'Sentry',
    'analytics': 'Firebase Analytics',
    'distribution': 'Google Play Console',
    'email': 'Brevo',
    'hosting': 'Hostinger + Cloudflare',
}

# ── Presets d'idees connues ──
IDEA_PRESETS = {
    'NeuroCalm': {
        'moat_score': 94,
        'stack_match': 5,       # 5/5 — identique a Respir (audio + respiration + guidage)
        'mvp_weeks': 8,
        'synergy': 5,           # 5/5 — extension directe de Respir
        'mvp_clarity': 4,       # 4/5 — protocole polyvagal a structurer
        'risk_level': 2,        # 2/5 — pas de validation medicale obligatoire
        'content_needed': True,
        'partner_needed': False,
        'segment': 'Adultes stresses, regulation systeme nerveux',
        'monetization': 'Freemium 6.99/mois',
    },
    'SleepCoach FR': {
        'moat_score': 90,
        'stack_match': 5,
        'mvp_weeks': 12,
        'synergy': 5,
        'mvp_clarity': 5,
        'risk_level': 3,        # Besoin partenaire medical
        'content_needed': True,
        'partner_needed': True,
        'segment': '20M insomniaques FR',
        'monetization': '6.99/mois ou 49.99/an',
    },
    'DoctAfter': {
        'moat_score': 88,
        'stack_match': 4,       # 4/5 — pas d'audio, mais CRUD + notifications
        'mvp_weeks': 8,
        'synergy': 2,           # 2/5 — pas de lien direct avec Respir
        'mvp_clarity': 4,
        'risk_level': 3,        # Donnees medicales = RGPD attention
        'content_needed': False,
        'partner_needed': False,
        'segment': '40M patients Doctolib',
        'monetization': '2.99/mois ou 24.99/an',
    },
    'Exercice Builder': {
        'moat_score': 81,
        'stack_match': 5,
        'mvp_weeks': 6,
        'synergy': 3,
        'mvp_clarity': 4,
        'risk_level': 1,
        'content_needed': False,
        'partner_needed': False,
        'segment': 'Kines/coachs independants',
        'monetization': 'Abonnement ~7.99/mois',
    },
    'CoachCRM': {
        'moat_score': 79,
        'stack_match': 4,
        'mvp_weeks': 7,
        'synergy': 2,
        'mvp_clarity': 4,
        'risk_level': 2,
        'content_needed': False,
        'partner_needed': False,
        'segment': '50K coachs FR',
        'monetization': 'Freemium, Pro 9.99/mois',
    },
    'PetitsBouts': {
        'moat_score': 80,
        'stack_match': 4,
        'mvp_weeks': 10,
        'synergy': 1,
        'mvp_clarity': 3,
        'risk_level': 3,
        'content_needed': True,
        'partner_needed': True,
        'segment': '750K grossesses/an FR',
        'monetization': '3.99/mois ou 29.99/an',
    },
    'Apaise': {
        'moat_score': 78,
        'stack_match': 5,
        'mvp_weeks': 8,
        'synergy': 4,           # Bien-etre / sante mentale
        'mvp_clarity': 3,       # Protocole deuil a definir
        'risk_level': 3,        # Contenu sensible, validation psy
        'content_needed': True,
        'partner_needed': True,
        'segment': '600K deces/an FR',
        'monetization': 'Freemium',
    },
    'RituelZen': {
        'moat_score': 70,
        'stack_match': 4,
        'mvp_weeks': 6,
        'synergy': 3,
        'mvp_clarity': 4,
        'risk_level': 1,
        'content_needed': False,
        'partner_needed': False,
        'segment': 'Anti-Fabulous, routines bien-etre',
        'monetization': 'Freemium',
    },
}


def calculate_bri(moat_score, stack_match, mvp_weeks, synergy, mvp_clarity, risk_level):
    """
    Calculate Build Readiness Index (0-100).

    Parameters (all 1-5 except moat_score which is 0-100):
        moat_score: MOAT score (0-100)
        stack_match: compatibility with existing stack (1-5)
        mvp_weeks: weeks to MVP (lower = better)
        synergy: synergy with existing apps (1-5)
        mvp_clarity: how clear is what to build (1-5)
        risk_level: risk level (1=low, 5=high — inverted for score)
    """

    # 1. MOAT Score (25%) — normalize to 0-25
    moat_component = (moat_score / 100) * 25

    # 2. Faisabilite technique (20%) — stack_match 1-5 -> 0-20
    tech_component = (stack_match / 5) * 20

    # 3. Vitesse de livraison (15%) — mvp_weeks inversed (less = better)
    if mvp_weeks <= 4:
        speed_score = 5
    elif mvp_weeks <= 6:
        speed_score = 4
    elif mvp_weeks <= 8:
        speed_score = 3
    elif mvp_weeks <= 12:
        speed_score = 2
    else:
        speed_score = 1
    speed_component = (speed_score / 5) * 15

    # 4. Avantage personnel (15%) — synergy 1-5 -> 0-15
    synergy_component = (synergy / 5) * 15

    # 5. Clarte MVP (15%) — mvp_clarity 1-5 -> 0-15
    clarity_component = (mvp_clarity / 5) * 15

    # 6. Risque maitrisable (10%) — risk inverted (low risk = high score)
    risk_score = 6 - risk_level  # 1->5, 2->4, 3->3, 4->2, 5->1
    risk_component = (risk_score / 5) * 10

    total = moat_component + tech_component + speed_component + synergy_component + clarity_component + risk_component
    total = round(min(total, 100), 1)

    return {
        'total': total,
        'components': {
            'moat_score': round(moat_component, 1),
            'tech_feasibility': round(tech_component, 1),
            'delivery_speed': round(speed_component, 1),
            'personal_edge': round(synergy_component, 1),
            'mvp_clarity': round(clarity_component, 1),
            'risk_control': round(risk_component, 1),
        },
        'decision': 'FICHE BUILD AUTO' if total >= 75 else 'VALIDATION REQUISE' if total >= 60 else 'PAS PRET',
        'generate_fiche': total >= 75,
    }


def generate_build_fiche(idea_name, preset, bri):
    """Generate a Markdown build fiche automatically."""

    md = f"""# FICHE BUILD — {idea_name}
*Generee automatiquement par MOAT Build Index*
*Date : {datetime.now().strftime('%Y-%m-%d')}*
*BRI : {bri['total']}/100 — {bri['decision']}*

---

## Indices de faisabilite

| Dimension | Score | Max | Detail |
|-----------|-------|-----|--------|
| Potentiel marche (MOAT) | {bri['components']['moat_score']} | 25 | Score MOAT {preset['moat_score']}/100 |
| Faisabilite technique | {bri['components']['tech_feasibility']} | 20 | Stack match {preset['stack_match']}/5 |
| Vitesse de livraison | {bri['components']['delivery_speed']} | 15 | MVP {preset['mvp_weeks']} semaines |
| Avantage personnel | {bri['components']['personal_edge']} | 15 | Synergie {preset['synergy']}/5 |
| Clarte du MVP | {bri['components']['mvp_clarity']} | 15 | Clarte {preset['mvp_clarity']}/5 |
| Risque maitrisable | {bri['components']['risk_control']} | 10 | Risque {preset['risk_level']}/5 |
| **TOTAL BRI** | **{bri['total']}** | **100** | **{bri['decision']}** |

## Identite

- **Segment** : {preset.get('segment', '--')}
- **Monetisation** : {preset.get('monetization', '--')}
- **Contenu necessaire** : {'Oui' if preset.get('content_needed') else 'Non'}
- **Partenaire necessaire** : {'Oui' if preset.get('partner_needed') else 'Non'}

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

## MVP — {preset['mvp_weeks']} semaines

### Estimation effort
- **Duree** : {preset['mvp_weeks']} semaines
- **Heures estimees** : ~{preset['mvp_weeks'] * 6}h ({preset['mvp_weeks'] * 6 // preset['mvp_weeks']}h/semaine)

### Deploiement (copier le process Respir)
1. `flutter create --org com.xxx {idea_name.lower().replace(' ', '')}`
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

1. {'Rechercher protocole + partenaire specialiste' if preset.get('partner_needed') else 'Definir les ecrans MVP'}
2. {'Creer le contenu (scripts, audio)' if preset.get('content_needed') else 'Creer le data model Supabase'}
3. Creer une landing page test
4. Si >10% inscription -> lancer le dev
5. Sprint 1 : Setup projet Flutter

---
*Fiche generee par MOAT Build Index v1 — {datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""
    return md


def run_build_index(idea_name, preset=None, **kwargs):
    """Run the Build Readiness Index for an idea."""

    if preset is None:
        preset = {
            'moat_score': kwargs.get('moat_score', 50),
            'stack_match': kwargs.get('stack_match', 3),
            'mvp_weeks': kwargs.get('mvp_weeks', 8),
            'synergy': kwargs.get('synergy', 3),
            'mvp_clarity': kwargs.get('mvp_clarity', 3),
            'risk_level': kwargs.get('risk_level', 3),
            'content_needed': kwargs.get('content_needed', False),
            'partner_needed': kwargs.get('partner_needed', False),
            'segment': kwargs.get('segment', '--'),
            'monetization': kwargs.get('monetization', '--'),
        }

    bri = calculate_bri(
        preset['moat_score'],
        preset['stack_match'],
        preset['mvp_weeks'],
        preset['synergy'],
        preset['mvp_clarity'],
        preset['risk_level'],
    )

    # Display
    print(f"\n{'='*60}")
    print(f"  BUILD READINESS INDEX — {idea_name}")
    print(f"  {datetime.now().strftime('%Y-%m-%d')}")
    print(f"{'='*60}")

    print(f"\n  {'Dimension':25s} {'Score':>6s} {'Max':>5s} {'Barre'}")
    print(f"  {'-'*25} {'-'*6} {'-'*5} {'-'*20}")

    for name, score in bri['components'].items():
        max_val = {'moat_score': 25, 'tech_feasibility': 20, 'delivery_speed': 15,
                   'personal_edge': 15, 'mvp_clarity': 15, 'risk_control': 10}[name]
        pct = score / max_val
        bar_len = int(pct * 15)
        bar = '#' * bar_len + '.' * (15 - bar_len)
        label = name.replace('_', ' ').title()
        print(f"  {label:25s} {score:>5.1f} /{max_val:<4d} [{bar}]")

    print(f"\n  {'TOTAL BRI':25s} {bri['total']:>5.1f} /100")

    # Decision
    if bri['total'] >= 75:
        print(f"\n  {'*'*50}")
        print(f"  DECISION : FICHE BUILD GENEREE AUTOMATIQUEMENT")
        print(f"  BRI {bri['total']}/100 >= 75 -> GO")
        print(f"  {'*'*50}")
    elif bri['total'] >= 60:
        print(f"\n  DECISION : VALIDATION SUPPLEMENTAIRE REQUISE")
        print(f"  BRI {bri['total']}/100 (60-74) -> APPROFONDIR")
    else:
        print(f"\n  DECISION : PAS PRET POUR UNE FICHE BUILD")
        print(f"  BRI {bri['total']}/100 < 60 -> CONTINUER LA RECHERCHE")

    # Generate fiche if threshold met
    if bri['generate_fiche']:
        fiche = generate_build_fiche(idea_name, preset, bri)
        output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'build_fiches')
        os.makedirs(output_dir, exist_ok=True)
        slug = idea_name.lower().replace(' ', '_')[:20]
        filepath = os.path.join(output_dir, f"build_{slug}_{datetime.now():%Y%m%d}.md")

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(fiche)

        print(f"\n  Fiche build generee : {filepath}")

    return bri


def scan_all():
    """Scan all presets and rank by BRI."""
    print(f"\n{'#'*60}")
    print(f"  SCAN COMPLET — Build Readiness Index")
    print(f"{'#'*60}")

    results = []
    for name, preset in IDEA_PRESETS.items():
        bri = calculate_bri(
            preset['moat_score'], preset['stack_match'],
            preset['mvp_weeks'], preset['synergy'],
            preset['mvp_clarity'], preset['risk_level'],
        )
        results.append((name, bri, preset))

    # Sort by BRI
    results.sort(key=lambda x: -x[1]['total'])

    print(f"\n  {'#':3s} {'Idee':20s} {'BRI':>6s} {'MOAT':>6s} {'Tech':>5s} {'Speed':>6s} {'Edge':>5s} {'MVP':>5s} {'Risk':>5s} {'Decision'}")
    print(f"  {'-'*3} {'-'*20} {'-'*6} {'-'*6} {'-'*5} {'-'*6} {'-'*5} {'-'*5} {'-'*5} {'-'*25}")

    for i, (name, bri, preset) in enumerate(results, 1):
        c = bri['components']
        decision = 'FICHE AUTO' if bri['total'] >= 75 else 'VALIDER' if bri['total'] >= 60 else 'PAS PRET'
        marker = ' <<<' if bri['total'] >= 75 else ''
        print(f"  {i:3d} {name:20s} {bri['total']:>5.1f} {c['moat_score']:>5.1f} {c['tech_feasibility']:>5.1f} {c['delivery_speed']:>5.1f} {c['personal_edge']:>5.1f} {c['mvp_clarity']:>5.1f} {c['risk_control']:>5.1f} {decision}{marker}")

    # Auto-generate fiches for qualifying ideas
    auto_generated = [r for r in results if r[1]['total'] >= 75]
    if auto_generated:
        print(f"\n  {len(auto_generated)} fiches build a generer automatiquement:")
        for name, bri, preset in auto_generated:
            fiche = generate_build_fiche(name, preset, bri)
            output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'build_fiches')
            os.makedirs(output_dir, exist_ok=True)
            slug = name.lower().replace(' ', '_')[:20]
            filepath = os.path.join(output_dir, f"build_{slug}_{datetime.now():%Y%m%d}.md")
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(fiche)
            print(f"    [OK] {name} (BRI {bri['total']}) -> {filepath}")

    print(f"\n{'#'*60}")
    return results


def main():
    parser = argparse.ArgumentParser(description="MOAT Build Readiness Index")
    parser.add_argument("--idea", help="Nom de l'idee (utilise un preset si disponible)")
    parser.add_argument("--moat-score", type=int, help="Score MOAT (0-100)")
    parser.add_argument("--stack-match", type=int, help="Compatibilite stack (1-5)")
    parser.add_argument("--mvp-weeks", type=int, help="Semaines pour le MVP")
    parser.add_argument("--synergy", type=int, help="Synergie avec apps existantes (1-5)")
    parser.add_argument("--mvp-clarity", type=int, help="Clarte du MVP (1-5)")
    parser.add_argument("--risk", type=int, help="Niveau de risque (1-5)")
    parser.add_argument("--scan-all", action="store_true", help="Scanner tous les presets")
    parser.add_argument("--list", action="store_true", help="Lister les presets")
    args = parser.parse_args()

    if args.list:
        print(f"\n  Presets disponibles:")
        for name, p in sorted(IDEA_PRESETS.items(), key=lambda x: -x[1]['moat_score']):
            print(f"    {name:20s} MOAT={p['moat_score']} stack={p['stack_match']} mvp={p['mvp_weeks']}sem synergy={p['synergy']}")
        return

    if args.scan_all:
        scan_all()
        return

    if args.idea:
        preset = IDEA_PRESETS.get(args.idea)
        if preset:
            run_build_index(args.idea, preset)
        elif args.moat_score:
            run_build_index(args.idea,
                moat_score=args.moat_score,
                stack_match=args.stack_match or 3,
                mvp_weeks=args.mvp_weeks or 8,
                synergy=args.synergy or 3,
                mvp_clarity=args.mvp_clarity or 3,
                risk_level=args.risk or 3,
            )
        else:
            print(f"  Preset '{args.idea}' non trouve. Utilise --moat-score pour un calcul custom.")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
