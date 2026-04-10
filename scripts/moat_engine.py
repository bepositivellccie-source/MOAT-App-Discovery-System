#!/usr/bin/env python3
"""
MOAT Engine v2 — Orchestrateur Central

Le cerveau du systeme. Enchaine automatiquement :
1. Niche Hunter (scan marche + review analysis)
2. Market Sizer (TAM/SAM/SOM)
3. Cross Validator (multi-source validation)
4. Score MOAT (scoring pondere data-backed)
5. Rapport final avec verdict

Usage:
    python moat_engine.py "SleepCoach FR" \
        --query "sleep insomnia CBT" \
        --competitors "com.northcube.sleepcycle,com.calm.android" \
        --segment-size 20000000 \
        --arpu 60 \
        --angle "CBT-I therapy vs simple tracking"

    python moat_engine.py "CoachCRM" \
        --query "coach fitness management" \
        --segment-size 50000 \
        --arpu 120 \
        --angle "Business CRM vs exercise tracker"
"""

import argparse
import json
import os
import sys
import re
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))

# Import MOAT modules (graceful fallback)
modules = {}

try:
    from niche_hunter import NicheHunter
    modules['niche_hunter'] = True
except ImportError:
    modules['niche_hunter'] = False

try:
    from market_sizer import MarketSizer
    modules['market_sizer'] = True
except ImportError:
    modules['market_sizer'] = False

try:
    from cross_validator import CrossValidator
    modules['cross_validator'] = True
except ImportError:
    modules['cross_validator'] = False

try:
    from playstore_intel import get_app_info, get_reviews_analysis, search_apps
    modules['playstore'] = True
except ImportError:
    modules['playstore'] = False


# ── BODYGUARD — Kill criteria (abort immediately) ──
# If ANY of these triggers, the idea is dead. No further analysis.
BODYGUARD_RULES = [
    {
        'id': 'NO_PAIN',
        'label': 'Pas de douleur reelle',
        'description': 'Le probleme est un desir ou un confort, pas une souffrance. Les gens ne cherchent pas activement une solution.',
        'check': lambda scores: scores.get('pain_intensity', 0) < 3,
    },
    {
        'id': 'NO_FREQUENCY',
        'label': 'Usage trop rare',
        'description': 'Le besoin revient moins d\'une fois par mois. Pas de recurrence = pas de retention = pas d\'abonnement.',
        'check': lambda scores: scores.get('usage_frequency', 0) < 2,
    },
    {
        'id': 'NO_MONEY',
        'label': 'Aucun signal de paiement',
        'description': 'Le segment est habitue au gratuit, aucun concurrent ne monetise, personne ne paie pour ce type de solution.',
        'check': lambda scores: scores.get('willingness_to_pay', 0) < 2,
    },
    {
        'id': 'MARKET_DOMINATED',
        'label': 'Marche domine et satisfait',
        'description': 'Les concurrents ont >4.5/5 de score et <15% d\'avis negatifs. Les gens sont contents. Pas de gap.',
        'check': lambda market: market.get('avg_score', 0) >= 4.5 and market.get('pct_below_4', 100) < 10,
    },
    {
        'id': 'SCORE_TOO_LOW',
        'label': 'Score MOAT insuffisant',
        'description': 'Score total sous 45/100. Trop de faiblesses cumulees, pas viable.',
        'check': lambda scores: scores.get('total', 100) < 45,
    },
]


def bodyguard_check(scores, market_data=None):
    """
    Run bodyguard kill checks. Returns (passed, kills).
    If kills is not empty, the idea should be aborted.
    """
    kills = []

    for rule in BODYGUARD_RULES:
        try:
            # Some rules check scores, some check market data
            if rule['id'] == 'MARKET_DOMINATED':
                if market_data and rule['check'](market_data):
                    kills.append(rule)
            elif rule['id'] == 'SCORE_TOO_LOW':
                if rule['check'](scores):
                    kills.append(rule)
            else:
                if rule['check'](scores):
                    kills.append(rule)
        except:
            pass

    return len(kills) == 0, kills


SCORING_WEIGHTS = {
    'pain_intensity':    4,  # x4 = max 20
    'usage_frequency':   3,  # x3 = max 15
    'willingness_to_pay': 3, # x3 = max 15
    'market_access':     2,  # x2 = max 10
    'competition_gap':   2,  # x2 = max 10
    'differentiation':   2,  # x2 = max 10
    'personal_fit':      2,  # x2 = max 10
    'mvp_speed':         1,  # x1 = max 5
    'retention':         1,  # x1 = max 5
}

# ── V3 UPGRADES ──

# Trend Multiplier — adjusts final score based on Google Trends direction
# Applied AFTER base scoring, as a multiplier on the total
TREND_MULTIPLIERS = {
    'EXPLOSIVE': 1.15,   # Trend en explosion (ex: time tracking freelance +570%)
    'UP': 1.08,          # Tendance montante (ex: anger management +22%)
    'STABLE': 1.00,      # Plateau (ex: highly sensitive person)
    'DOWN': 0.90,        # En decline (ex: hypersensible -33%)
}

# Structural Driver Bonus — when demand is created by law/regulation
# Added as flat bonus points to the final score
STRUCTURAL_DRIVER_BONUS = 8  # +8 points if there's a legal/regulatory driver

# Solo Dev Reality Factor — adjusts SOM to realistic Y1 for a solo developer
# The theoretical SOM is multiplied by this factor
SOLO_DEV_SOM_FACTOR = 0.07  # 7% of theoretical SOM = realistic solo dev Y1 (Sonnet recommande 5-10%, on prend le milieu)

# Conditional Score — when a score depends on an external condition
# If condition is not met, the score falls to the penalty value
# Example: TOCLibre = 80 with psy partner, 60 without
CONDITIONAL_PENALTIES = {
    'partner_medical': -15,     # Needs medical/psy partner validation
    'partner_content': -10,     # Needs content expert (not medical)
    'regulatory_risk': -12,     # RGPD, medical device, legal risk
    'market_education': -10,    # Behavior doesn't exist yet, needs education
}


def data_backed_score(market_data, review_data, tam_data, angle_strength=3,
                      trend_direction='STABLE', structural_driver=False):
    """
    Generate a MOAT score backed by real data instead of gut feeling.
    V3: includes trend multiplier + structural driver bonus.

    Returns scores 1-5 for each criterion based on data signals.
    """
    scores = {}

    # 1. Pain Intensity — based on negative review ratio
    neg_ratio = review_data.get('avg_negative_ratio', 0)
    if neg_ratio >= 45:
        scores['pain_intensity'] = 5
    elif neg_ratio >= 35:
        scores['pain_intensity'] = 4
    elif neg_ratio >= 25:
        scores['pain_intensity'] = 3
    elif neg_ratio >= 15:
        scores['pain_intensity'] = 2
    else:
        scores['pain_intensity'] = 1

    # 2. Usage Frequency — estimated from total competitor installs
    # High installs across competitors = proven frequent usage pattern
    total_installs = market_data.get('total_installs', 0)
    # Also check from review data: if we analyzed competitors, their installs are significant
    if total_installs >= 50_000_000:
        scores['usage_frequency'] = 5
    elif total_installs >= 10_000_000:
        scores['usage_frequency'] = 4
    elif total_installs >= 1_000_000:
        scores['usage_frequency'] = 3
    elif total_installs >= 100_000:
        scores['usage_frequency'] = 2
    else:
        # If we have review data, the market exists even if search failed
        if review_data.get('total_reviews_analyzed', 0) > 100:
            scores['usage_frequency'] = 4  # Market proven via reviews
        else:
            scores['usage_frequency'] = 1

    # 3. Willingness to Pay — based on pricing complaints
    pricing_complaints = review_data.get('pricing_complaint_ratio', 0)
    # Paradox: high pricing complaints = people WANT the product but think it's overpriced
    # This means willingness to pay exists, just needs better value proposition
    if pricing_complaints >= 40:
        scores['willingness_to_pay'] = 4  # Strong signal: they pay but complain
    elif pricing_complaints >= 25:
        scores['willingness_to_pay'] = 3
    elif pricing_complaints >= 10:
        scores['willingness_to_pay'] = 2
    else:
        scores['willingness_to_pay'] = 1

    # 4. Market Access — based on segment size and reachability
    som = tam_data.get('som', 0)
    if som >= 500_000:
        scores['market_access'] = 5
    elif som >= 100_000:
        scores['market_access'] = 4
    elif som >= 50_000:
        scores['market_access'] = 3
    elif som >= 10_000:
        scores['market_access'] = 2
    else:
        scores['market_access'] = 1

    # 5. Competition Gap — based on market quality + frustration
    apps_below_4 = market_data.get('pct_below_4', 0)
    neg_ratio_for_gap = review_data.get('avg_negative_ratio', 0)
    # Use whichever signal is stronger
    gap_signal = max(apps_below_4, neg_ratio_for_gap)
    if gap_signal >= 45:
        scores['competition_gap'] = 5
    elif gap_signal >= 35:
        scores['competition_gap'] = 4
    elif gap_signal >= 25:
        scores['competition_gap'] = 3
    elif gap_signal >= 15:
        scores['competition_gap'] = 2
    else:
        scores['competition_gap'] = 1

    # 6. Differentiation — partially manual (angle strength 1-5)
    scores['differentiation'] = min(max(angle_strength, 1), 5)

    # 7. Personal Fit — manual input (default 3)
    scores['personal_fit'] = 3

    # 8. MVP Speed — based on technical complexity estimate
    scores['mvp_speed'] = 3  # Default medium

    # 9. Retention — based on usage frequency + pricing complaints
    # If people complain about pricing but still use it = high retention value
    if review_data.get('pricing_complaint_ratio', 0) >= 40:
        scores['retention'] = 5  # They keep paying despite complaining = sticky
    elif review_data.get('pricing_complaint_ratio', 0) >= 20:
        scores['retention'] = 4
    else:
        scores['retention'] = min(scores['usage_frequency'], 5)

    # Calculate weighted total
    total = 0
    details = []
    for criterion, weight in SCORING_WEIGHTS.items():
        raw = scores.get(criterion, 3)
        weighted = raw * weight
        total += weighted
        details.append({
            'criterion': criterion,
            'raw': raw,
            'weight': weight,
            'weighted': weighted,
            'max': weight * 5,
        })

    # V3: Apply trend multiplier
    trend_mult = TREND_MULTIPLIERS.get(trend_direction, 1.0)
    total_before_trend = total
    total = round(total * trend_mult)

    # V3: Apply structural driver bonus
    structural_bonus = 0
    if structural_driver:
        structural_bonus = STRUCTURAL_DRIVER_BONUS
        total = min(total + structural_bonus, 100)

    # V3: Calculate Solo Dev SOM
    som_theoretical = tam_data.get('som', 0)
    som_solo_dev = round(som_theoretical * SOLO_DEV_SOM_FACTOR)

    # Store V3 data
    scores['_v3'] = {
        'trend_direction': trend_direction,
        'trend_multiplier': trend_mult,
        'structural_driver': structural_driver,
        'structural_bonus': structural_bonus,
        'total_before_adjustments': total_before_trend,
        'som_theoretical': som_theoretical,
        'som_solo_dev_y1': som_solo_dev,
    }

    # Decision
    if total >= 75:
        decision = "A -- Build now"
    elif total >= 60:
        decision = "B -- Validate"
    elif total >= 45:
        decision = "C -- Watchlist"
    else:
        decision = "D -- Kill"

    return {
        'total': total,
        'max': 100,
        'decision': decision,
        'details': details,
        'raw_scores': scores,
    }


def run_engine(idea_name, query=None, competitors=None, segment_size=None,
               arpu=None, angle=None, angle_strength=3,
               trend_direction='STABLE', structural_driver=False,
               condition=None, condition_met=False,
               lang='fr', country='fr'):
    """Run the full MOAT engine pipeline."""

    report = {
        'idea': idea_name,
        'date': datetime.now().isoformat(),
        'modules_available': modules,
        'phases': {},
    }

    print(f"\n{'#'*70}")
    print(f"  MOAT ENGINE v2 — Full Analysis")
    print(f"  Idea: {idea_name}")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'#'*70}")

    search_query = query or idea_name
    comp_ids = competitors.split(',') if competitors else []

    # ── PHASE 1: Market Scan ──
    market_data = {
        'total_apps': 0, 'avg_score': 0, 'total_installs': 0,
        'pct_below_4': 0, 'opportunity_signal': 'UNKNOWN'
    }

    if modules.get('playstore'):
        print(f"\n{'='*60}")
        print(f"  PHASE 1: Market Scan — Google Play")
        print(f"{'='*60}")

        apps = search_apps(search_query, lang=lang, top=15)
        if apps and 'error' not in apps[0]:
            scores = [a['score'] for a in apps if a.get('score')]
            installs = [a['installs'] for a in apps if isinstance(a.get('installs'), int)]
            below_4 = len([s for s in scores if s < 4.0])

            market_data = {
                'total_apps': len(apps),
                'avg_score': round(sum(scores) / max(len(scores), 1), 2),
                'total_installs': sum(installs[:10]),
                'pct_below_4': round(below_4 / max(len(scores), 1) * 100),
                'opportunity_signal': 'FORT' if below_4 > len(scores)/2 else 'MOYEN' if below_4 > 2 else 'FAIBLE',
            }

            print(f"\n  Apps trouvees       : {market_data['total_apps']}")
            print(f"  Score moyen         : {market_data['avg_score']}/5")
            print(f"  Installs top 10     : {market_data['total_installs']:,}")
            print(f"  % sous 4.0 etoiles  : {market_data['pct_below_4']}%")
            print(f"  Signal opportunite  : {market_data['opportunity_signal']}")

            # Auto-detect competitors if not provided
            if not comp_ids:
                comp_ids = [a['id'] for a in apps[:3] if a.get('id')]

        report['phases']['market_scan'] = market_data

    # ── PHASE 2: Review Deep Dive ──
    review_data = {'avg_negative_ratio': 0, 'pricing_complaint_ratio': 0, 'top_frustrations': []}

    if modules.get('playstore') and comp_ids:
        print(f"\n{'='*60}")
        print(f"  PHASE 2: Review Analysis — {len(comp_ids)} competitors")
        print(f"{'='*60}")

        from collections import Counter
        all_frustrations = Counter()
        total_neg = 0
        total_reviews = 0
        pricing_mentions = 0
        total_neg_reviews = 0

        pricing_words = ['payant', 'cher', 'abonnement', 'premium', 'arnaque',
                         'expensive', 'subscription', 'paywall', 'overpriced', 'gratuit', 'free']
        all_markers = [
            'payant','cher','abonnement','premium','arnaque','bug','crash','plante',
            'lent','complique','confus','inutile','pub','publicite','manque','impossible',
            'expensive','subscription','slow','complicated','useless','missing','ads',
            'broken','frustrating','annoying','gratuit','free',
        ]

        for cid in comp_ids[:5]:
            try:
                info = get_app_info(cid, lang=lang)
                analysis = get_reviews_analysis(cid, lang=lang, count=150)

                if 'error' not in info and 'error' not in analysis:
                    name = info.get('title', cid)[:30]
                    neg = analysis.get('negative_count', 0)
                    total = analysis.get('total_fetched', 0)
                    ratio = analysis.get('negative_ratio', 0)

                    total_neg += neg
                    total_reviews += total

                    print(f"\n  {name}")
                    print(f"    Score: {info.get('score','?')}/5 | Negatifs: {ratio}%")

                    # Count frustrations
                    for marker, count in analysis.get('top_frustrations', []):
                        all_frustrations[marker] += count
                        if marker in pricing_words:
                            pricing_mentions += count
                        total_neg_reviews += count
            except Exception as e:
                print(f"  {cid}: erreur ({str(e)[:40]})")

        avg_neg_ratio = round(total_neg / max(total_reviews, 1) * 100, 1)
        pricing_ratio = round(pricing_mentions / max(total_neg_reviews, 1) * 100, 1) if total_neg_reviews else 0

        review_data = {
            'avg_negative_ratio': avg_neg_ratio,
            'pricing_complaint_ratio': pricing_ratio,
            'total_reviews_analyzed': total_reviews,
            'top_frustrations': all_frustrations.most_common(15),
        }

        print(f"\n  SYNTHESE REVIEWS:")
        print(f"    Ratio negatifs moyen  : {avg_neg_ratio}%")
        print(f"    Plaintes pricing      : {pricing_ratio}%")
        print(f"    Reviews analysees     : {total_reviews}")

        if all_frustrations:
            print(f"\n  TOP FRUSTRATIONS:")
            for marker, count in all_frustrations.most_common(10):
                bar = '#' * min(count, 40)
                print(f"    {marker:20s} {bar} ({count})")

        report['phases']['review_analysis'] = review_data

    # ── PHASE 3: Market Sizing ──
    tam_data = {'tam': 0, 'sam': 0, 'som': 0}

    if segment_size and arpu:
        print(f"\n{'='*60}")
        print(f"  PHASE 3: Market Sizing (TAM/SAM/SOM)")
        print(f"{'='*60}")

        tam = segment_size * arpu
        sam = tam * 0.15  # 15% reachable
        capture_rate = 0.02  # 2% year 1
        som = sam * capture_rate

        tam_data = {
            'segment_size': segment_size,
            'arpu': arpu,
            'tam': tam,
            'sam': sam,
            'som': som,
            'monthly_revenue_est': round(som / 12),
            'capture_rate': capture_rate,
        }

        print(f"\n  Segment             : {segment_size:,} personnes")
        print(f"  ARPU                : {arpu} EUR/an")
        print(f"  TAM                 : {tam:,.0f} EUR")
        print(f"  SAM (15%)           : {sam:,.0f} EUR")
        print(f"  SOM (2% capture)    : {som:,.0f} EUR")
        print(f"  Revenue mensuel est : {som/12:,.0f} EUR/mois")

        if som/12 >= 10000:
            verdict_market = "EXCELLENT — potentiel 10K+ MRR"
        elif som/12 >= 5000:
            verdict_market = "BON — potentiel 5K+ MRR"
        elif som/12 >= 1000:
            verdict_market = "VIABLE — micro-SaaS viable"
        else:
            verdict_market = "PETIT — necessite volume ou ARPU plus eleve"

        print(f"  Verdict marche      : {verdict_market}")
        tam_data['verdict'] = verdict_market

        report['phases']['market_sizing'] = tam_data

    # ── PHASE 4: Data-Backed Scoring ──
    print(f"\n{'='*60}")
    print(f"  PHASE 4: MOAT Scoring (Data-Backed)")
    print(f"{'='*60}")

    scoring = data_backed_score(market_data, review_data, tam_data, angle_strength,
                                trend_direction=trend_direction,
                                structural_driver=structural_driver)

    print(f"\n  SCORING DETAILS:")
    for d in scoring['details']:
        bar = '#' * d['raw'] + '.' * (5 - d['raw'])
        label = d['criterion'].replace('_', ' ').title()
        print(f"    {label:25s} [{bar}] {d['weighted']:2d}/{d['max']} (x{d['weight']})")

    print(f"\n  {'TOTAL':25s}       {scoring['total']}/{scoring['max']}")
    print(f"  {'DECISION':25s}       {scoring['decision']}")

    report['phases']['scoring'] = scoring

    # ── PHASE 4b: BODYGUARD CHECK ──
    print(f"\n{'='*60}")
    print(f"  BODYGUARD — Filtres eliminatoires")
    print(f"{'='*60}")

    bg_passed, bg_kills = bodyguard_check(scoring.get('raw_scores', {}), market_data)

    if bg_kills:
        print(f"\n  !! IDEE ELIMINEE — {len(bg_kills)} critere(s) eliminatoire(s) !!")
        for kill in bg_kills:
            print(f"  [KILL] {kill['label']}")
            print(f"         {kill['description']}")

        print(f"\n  {'X'*50}")
        print(f"  VERDICT: ABORT — Cette idee ne passe pas le bodyguard.")
        print(f"  Ne pas investir de temps supplementaire.")
        print(f"  {'X'*50}")

        report['verdict'] = {
            'score': scoring['total'],
            'decision': 'ABORT',
            'bodyguard_killed': True,
            'kill_reasons': [k['label'] for k in bg_kills],
        }

        # Save report even if killed
        output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'research')
        os.makedirs(output_dir, exist_ok=True)
        slug = re.sub(r'[^\w]', '_', idea_name.lower())
        filepath = os.path.join(output_dir, f"engine_{slug}_{datetime.now():%Y%m%d_%H%M}.json")
        def clean(obj):
            try:
                json.dumps(obj)
                return obj
            except (TypeError, ValueError):
                return str(obj)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2, default=clean)
        print(f"\n  Rapport: {filepath}")
        print(f"{'#'*70}")
        return report
    else:
        print(f"\n  [OK] Tous les filtres passes. Idee viable.")

    # ── PHASE 5: Final Verdict ──
    print(f"\n{'#'*70}")
    print(f"  VERDICT FINAL — {idea_name}")
    print(f"{'#'*70}")

    signals = []
    if market_data.get('opportunity_signal') == 'FORT':
        signals.append("[+] Marche mal servi (forte insatisfaction)")
    if review_data.get('avg_negative_ratio', 0) >= 35:
        signals.append(f"[+] {review_data['avg_negative_ratio']}% avis negatifs = frustration massive")
    if review_data.get('pricing_complaint_ratio', 0) >= 30:
        signals.append(f"[+] {review_data['pricing_complaint_ratio']}% plaintes pricing = volonte de payer")
    if tam_data.get('som', 0) / 12 >= 5000:
        signals.append(f"[+] SOM = {tam_data['som']/12:,.0f} EUR/mois potentiel")
    if scoring['total'] >= 75:
        signals.append(f"[+] Score MOAT {scoring['total']}/100 = Zone A")

    risks = []
    if market_data.get('total_installs', 0) < 100_000:
        risks.append("[-] Marche petit ou naissant (peu d'installs)")
    if review_data.get('avg_negative_ratio', 0) < 20:
        risks.append("[-] Faible frustration = concurrence de qualite")
    if tam_data.get('som', 0) / 12 < 1000:
        risks.append("[-] Revenue potentiel faible")

    print(f"\n  SIGNAUX POSITIFS:")
    for s in signals:
        print(f"    {s}")
    if not signals:
        print(f"    Aucun signal fort detecte")

    print(f"\n  RISQUES:")
    for r in risks:
        print(f"    {r}")
    if not risks:
        print(f"    Aucun risque majeur detecte")

    # Overall
    confidence = len(signals) * 20
    confidence = min(confidence, 100)

    # V3 data
    v3 = scoring.get('raw_scores', {}).get('_v3', {})

    # V3: Conditional score
    score_with_condition = scoring['total']
    score_without_condition = scoring['total']
    condition_label = ''

    if condition and condition in CONDITIONAL_PENALTIES:
        penalty = CONDITIONAL_PENALTIES[condition]
        condition_labels = {
            'partner_medical': 'Partenaire medical/psy requis',
            'partner_content': 'Expert contenu requis',
            'regulatory_risk': 'Risque reglementaire a evaluer',
            'market_education': 'Education marche necessaire',
        }
        condition_label = condition_labels.get(condition, condition)

        if condition_met:
            score_with_condition = scoring['total']  # Score maintenu
            score_without_condition = max(scoring['total'] + penalty, 0)
        else:
            score_without_condition = max(scoring['total'] + penalty, 0)
            score_with_condition = scoring['total']  # Score potentiel si condition remplie

    print(f"\n  {'*'*50}")
    if condition and not condition_met:
        print(f"  SCORE MOAT     : {score_without_condition}/100 (CONDITIONNEL)")
        print(f"  SCORE SI OK    : {score_with_condition}/100 — si {condition_label}")
        # Recalculate decision based on conditional score
        if score_without_condition >= 75:
            cond_decision = "A -- Build now (conditionnel)"
        elif score_without_condition >= 60:
            cond_decision = "B -- Validate (conditionnel)"
        else:
            cond_decision = "C -- Watchlist (bloque par condition)"
        print(f"  DECISION       : {cond_decision}")
        print(f"  CONDITION      : {condition_label}")
        print(f"  PENALITE       : {CONDITIONAL_PENALTIES[condition]} pts si non remplie")
    elif condition and condition_met:
        print(f"  SCORE MOAT     : {scoring['total']}/100 — {scoring['decision']}")
        print(f"  CONDITION      : {condition_label} -- REMPLIE")
    else:
        print(f"  SCORE MOAT     : {scoring['total']}/100 — {scoring['decision']}")

    if v3.get('total_before_adjustments') and v3['total_before_adjustments'] != scoring['total']:
        print(f"  SCORE BASE     : {v3['total_before_adjustments']}/100 (avant ajustements V3)")
    if v3.get('trend_direction') and v3['trend_direction'] != 'STABLE':
        print(f"  TREND          : {v3['trend_direction']} (x{v3['trend_multiplier']})")
    if v3.get('structural_driver'):
        print(f"  DRIVER         : LOI/REGULATION (+{v3['structural_bonus']} pts)")
    print(f"  CONFIDENCE     : {confidence}% (base sur {len(signals)} signaux)")
    if tam_data.get('som'):
        print(f"  SOM THEORIQUE  : {tam_data['som']/12:,.0f} EUR/mois")
        if v3.get('som_solo_dev_y1'):
            print(f"  SOM SOLO DEV Y1: {v3['som_solo_dev_y1']/12:,.0f} EUR/mois (realiste)")
    print(f"  {'*'*50}")

    report['verdict'] = {
        'score': scoring['total'],
        'decision': scoring['decision'],
        'confidence': confidence,
        'signals': signals,
        'risks': risks,
    }

    # Save report
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'research')
    os.makedirs(output_dir, exist_ok=True)
    slug = re.sub(r'[^\w]', '_', idea_name.lower())
    filepath = os.path.join(output_dir, f"engine_{slug}_{datetime.now():%Y%m%d_%H%M}.json")

    def clean(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        try:
            json.dumps(obj)
            return obj
        except (TypeError, ValueError):
            return str(obj)

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2, default=clean)

    print(f"\n  Rapport sauvegarde : {filepath}")
    print(f"{'#'*70}")

    return report


def main():
    parser = argparse.ArgumentParser(description="MOAT Engine v2 — Full Pipeline Analysis")
    parser.add_argument("idea", help="Nom de l'idee")
    parser.add_argument("--query", "-q", help="Search query Google Play")
    parser.add_argument("--competitors", "-c", help="App IDs concurrents (virgule)")
    parser.add_argument("--segment-size", "-s", type=int, help="Taille du segment cible")
    parser.add_argument("--arpu", "-a", type=float, help="Revenue moyen par user/an (EUR)")
    parser.add_argument("--angle", help="Description de la differenciation")
    parser.add_argument("--angle-strength", type=int, default=3, help="Force de la differenciation (1-5)")
    parser.add_argument("--trend", choices=['EXPLOSIVE', 'UP', 'STABLE', 'DOWN'], default='STABLE',
                       help="Direction Google Trends (EXPLOSIVE/UP/STABLE/DOWN)")
    parser.add_argument("--structural-driver", action="store_true",
                       help="Flag si une loi/regulation cree la demande")
    parser.add_argument("--condition", help="Condition bloquante (partner_medical, partner_content, regulatory_risk, market_education)")
    parser.add_argument("--condition-met", action="store_true",
                       help="La condition est remplie (partenaire trouve, etc.)")
    parser.add_argument("--lang", default="fr", help="Langue (default: fr)")
    parser.add_argument("--country", default="fr", help="Pays (default: fr)")
    args = parser.parse_args()

    run_engine(
        idea_name=args.idea,
        query=args.query,
        competitors=args.competitors,
        segment_size=args.segment_size,
        arpu=args.arpu,
        angle=args.angle,
        angle_strength=args.angle_strength,
        trend_direction=args.trend,
        structural_driver=args.structural_driver,
        condition=args.condition,
        condition_met=args.condition_met,
        lang=args.lang,
        country=args.country,
    )


if __name__ == "__main__":
    main()
