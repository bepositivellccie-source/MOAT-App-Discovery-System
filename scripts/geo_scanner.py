#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MOAT App Discovery System - Geo Scanner

Scanne la MEME idee sur PLUSIEURS marches geographiques
pour trouver OU l'opportunite est la plus forte.

La meme app peut etre saturee en France mais vierge en Italie.

Usage:
    python geo_scanner.py "com.northcube.sleepcycle" "com.calm.android" --markets fr,es,it,de,us,br
    python geo_scanner.py "com.toggl.giskard" --markets fr,es,it,de --reviews 100
    python geo_scanner.py "com.calm.android" --markets all

Presets:
    --markets europe    = fr,es,it,de,gb,pt,nl,be,ch
    --markets latam     = br,mx,ar,co,cl
    --markets all       = fr,es,it,de,gb,us,br,mx,pt,nl
"""

import argparse
import json
import os
import sys
import time
from collections import Counter
from datetime import datetime

try:
    from google_play_scraper import app, reviews, Sort
    HAS_SCRAPER = True
except ImportError:
    HAS_SCRAPER = False
    print("ERREUR: pip install google-play-scraper")
    sys.exit(1)


# ── Market database ──
MARKETS = {
    'fr': {
        'name': 'France',
        'lang': 'fr',
        'country': 'fr',
        'population': 68_000_000,
        'smartphone_pct': 0.82,
        'app_spend_rank': 5,  # Europe rank
        'growth_2025': '+52%',  # iOS YoY
        'notes': 'Marche mature, forte volonte de payer, francophone',
    },
    'es': {
        'name': 'Espagne',
        'lang': 'es',
        'country': 'es',
        'population': 47_000_000,
        'smartphone_pct': 0.80,
        'app_spend_rank': 6,
        'growth_2025': '+157%',  # iOS YoY — EXPLOSIVE
        'notes': 'Croissance iOS explosive +157%, hispanophones 580M mondial',
    },
    'it': {
        'name': 'Italie',
        'lang': 'it',
        'country': 'it',
        'population': 59_000_000,
        'smartphone_pct': 0.78,
        'app_spend_rank': 7,
        'growth_2025': '+143%',  # iOS YoY — EXPLOSIVE
        'notes': 'Croissance iOS +143%, marche sous-exploite, peu de devs indie',
    },
    'de': {
        'name': 'Allemagne',
        'lang': 'de',
        'country': 'de',
        'population': 84_000_000,
        'smartphone_pct': 0.85,
        'app_spend_rank': 2,
        'growth_2025': '+43%',
        'notes': 'Plus gros marche EU, forte volonte de payer, exigeant en qualite',
    },
    'gb': {
        'name': 'Royaume-Uni',
        'lang': 'en',
        'country': 'gb',
        'population': 67_000_000,
        'smartphone_pct': 0.88,
        'app_spend_rank': 1,
        'growth_2025': '+92%',
        'notes': 'Marche #1 EU en depense, anglophone, forte concurrence',
    },
    'us': {
        'name': 'Etats-Unis',
        'lang': 'en',
        'country': 'us',
        'population': 335_000_000,
        'smartphone_pct': 0.90,
        'app_spend_rank': 1,
        'growth_2025': '+15%',
        'notes': 'Plus gros marche mondial, tres concurrentiel, ARPU eleve',
    },
    'br': {
        'name': 'Bresil',
        'lang': 'pt',
        'country': 'br',
        'population': 215_000_000,
        'smartphone_pct': 0.72,
        'app_spend_rank': 3,
        'growth_2025': '+85%',
        'notes': 'Android dominant 90%, enorme volume, ARPU faible, croissance forte',
    },
    'mx': {
        'name': 'Mexique',
        'lang': 'es',
        'country': 'mx',
        'population': 130_000_000,
        'smartphone_pct': 0.70,
        'app_spend_rank': 8,
        'growth_2025': '+65%',
        'notes': 'Hispanophones, Android dominant, croissance rapide',
    },
    'pt': {
        'name': 'Portugal',
        'lang': 'pt',
        'country': 'pt',
        'population': 10_000_000,
        'smartphone_pct': 0.78,
        'app_spend_rank': 15,
        'growth_2025': '+40%',
        'notes': 'Petit marche mais lusophone (passerelle Bresil)',
    },
    'nl': {
        'name': 'Pays-Bas',
        'lang': 'nl',
        'country': 'nl',
        'population': 17_000_000,
        'smartphone_pct': 0.90,
        'app_spend_rank': 8,
        'growth_2025': '+35%',
        'notes': 'Tres tech-savvy, bon ARPU, parle anglais',
    },
    'ar': {
        'name': 'Argentine',
        'lang': 'es',
        'country': 'ar',
        'population': 46_000_000,
        'smartphone_pct': 0.68,
        'app_spend_rank': 12,
        'growth_2025': '+70%',
        'notes': 'Hispanophones, ARPU faible mais volume',
    },
    'co': {
        'name': 'Colombie',
        'lang': 'es',
        'country': 'co',
        'population': 52_000_000,
        'smartphone_pct': 0.65,
        'app_spend_rank': 14,
        'growth_2025': '+60%',
        'notes': 'Hispanophones, marche emergent',
    },
    'cl': {
        'name': 'Chili',
        'lang': 'es',
        'country': 'cl',
        'population': 19_000_000,
        'smartphone_pct': 0.75,
        'app_spend_rank': 11,
        'growth_2025': '+55%',
        'notes': 'ARPU le plus eleve LATAM, stable, tech-friendly',
    },
    'ch': {
        'name': 'Suisse',
        'lang': 'fr',
        'country': 'ch',
        'population': 9_000_000,
        'smartphone_pct': 0.92,
        'app_spend_rank': 3,
        'growth_2025': '+25%',
        'notes': 'ARPU tres eleve, multi-lingue (fr/de/it), exigeant',
    },
    'be': {
        'name': 'Belgique',
        'lang': 'fr',
        'country': 'be',
        'population': 11_500_000,
        'smartphone_pct': 0.85,
        'app_spend_rank': 10,
        'growth_2025': '+30%',
        'notes': 'Francophone (60%), bon ARPU',
    },
}

MARKET_PRESETS = {
    'europe': ['fr', 'es', 'it', 'de', 'gb', 'pt', 'nl', 'be', 'ch'],
    'latam': ['br', 'mx', 'ar', 'co', 'cl'],
    'francophone': ['fr', 'be', 'ch'],
    'hispanophone': ['es', 'mx', 'ar', 'co', 'cl'],
    'all': ['fr', 'es', 'it', 'de', 'gb', 'us', 'br', 'mx', 'pt', 'nl'],
}

FRUSTRATION_WORDS = {
    'fr': ['payant','cher','abonnement','premium','arnaque','bug','crash','plante',
           'lent','complique','inutile','pub','gratuit','fonctionne pas','manque'],
    'en': ['expensive','subscription','premium','scam','bug','crash','slow',
           'complicated','useless','ads','free','doesnt work','missing'],
    'es': ['caro','pago','suscripcion','premium','estafa','bug','lento',
           'complicado','inutil','publicidad','gratis','no funciona','falta'],
    'it': ['caro','pagamento','abbonamento','premium','truffa','bug','lento',
           'complicato','inutile','pubblicita','gratis','non funziona','manca'],
    'de': ['teuer','abo','abonnement','premium','betrug','bug','langsam',
           'kompliziert','nutzlos','werbung','kostenlos','funktioniert nicht','fehlt'],
    'pt': ['caro','pago','assinatura','premium','golpe','bug','lento',
           'complicado','inutil','publicidade','gratis','nao funciona','falta'],
    'nl': ['duur','abonnement','premium','oplichting','bug','traag',
           'ingewikkeld','nutteloos','reclame','gratis','werkt niet','ontbreekt'],
}


def analyze_market(app_id, market_code, review_count=100):
    """Analyze a single app in a specific market."""
    market = MARKETS.get(market_code, {})
    lang = market.get('lang', 'en')
    country = market.get('country', market_code)

    result = {
        'market': market_code,
        'market_name': market.get('name', market_code),
        'app_id': app_id,
    }

    # Get app info
    try:
        info = app(app_id, lang=lang, country=country)
        result['title'] = info.get('title', '')
        result['score'] = info.get('score', 0)
        result['ratings'] = info.get('ratings', 0)
        result['installs'] = info.get('realInstalls', 0)
        result['free'] = info.get('free', True)
        result['iap'] = info.get('inAppProductPrice', '')
    except Exception as e:
        result['error'] = f"App info: {str(e)[:50]}"
        return result

    # Get reviews
    try:
        revs, _ = reviews(app_id, lang=lang, country=country,
                         sort=Sort.NEWEST, count=review_count)
        negative = [r for r in revs if r.get('score', 5) <= 3]
        result['reviews_fetched'] = len(revs)
        result['negative_count'] = len(negative)
        result['negative_ratio'] = round(len(negative) / max(len(revs), 1) * 100, 1)

        # Frustration analysis
        markers = FRUSTRATION_WORDS.get(lang, FRUSTRATION_WORDS.get('en', []))
        frustrations = Counter()
        for r in negative:
            content = r.get('content', '').lower()
            for m in markers:
                if m in content:
                    frustrations[m] += 1

        result['top_frustrations'] = frustrations.most_common(10)
        result['total_frustration_mentions'] = sum(frustrations.values())

    except Exception as e:
        result['reviews_fetched'] = 0
        result['negative_ratio'] = 0
        result['error_reviews'] = str(e)[:50]

    return result


def geo_scan(app_ids, market_codes, review_count=100):
    """Scan multiple apps across multiple markets."""

    print(f"\n{'#'*70}")
    print(f"  MOAT GEO SCANNER")
    print(f"  {len(app_ids)} app(s) x {len(market_codes)} marche(s)")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'#'*70}")

    # Show market profiles
    print(f"\n  MARCHES CIBLES:")
    print(f"  {'Code':5s} {'Pays':15s} {'Pop':>12s} {'Mobile':>7s} {'Growth':>8s} {'Notes'}")
    print(f"  {'-'*5} {'-'*15} {'-'*12} {'-'*7} {'-'*8} {'-'*35}")
    for mc in market_codes:
        m = MARKETS.get(mc, {})
        pop = f"{m.get('population', 0):,}"
        mobile = f"{m.get('smartphone_pct', 0)*100:.0f}%"
        growth = m.get('growth_2025', '?')
        notes = m.get('notes', '')[:35]
        print(f"  {mc:5s} {m.get('name', mc):15s} {pop:>12s} {mobile:>7s} {growth:>8s} {notes}")

    # Scan each market
    all_results = {}
    market_scores = {}

    for mc in market_codes:
        market = MARKETS.get(mc, {})
        print(f"\n{'='*60}")
        print(f"  SCANNING: {market.get('name', mc)} ({mc})")
        print(f"{'='*60}")

        market_results = []
        total_neg_ratio = 0
        total_frustrations = 0
        total_installs = 0
        app_count = 0

        for aid in app_ids:
            print(f"    {aid}...", end=" ")
            result = analyze_market(aid, mc, review_count)
            market_results.append(result)

            if 'error' not in result:
                app_count += 1
                total_neg_ratio += result.get('negative_ratio', 0)
                total_frustrations += result.get('total_frustration_mentions', 0)
                total_installs += result.get('installs', 0)
                print(f"score={result.get('score', '?'):.1f} neg={result.get('negative_ratio', '?')}% installs={result.get('installs', 0):,}")
            else:
                print(f"SKIP ({result.get('error', '?')[:30]})")

            time.sleep(0.5)  # Rate limit protection

        # Calculate market opportunity score
        if app_count > 0:
            avg_neg = total_neg_ratio / app_count
            opp_score = 0
            # Frustration signal (max 35)
            opp_score += min(avg_neg * 0.7, 35)
            # Market growth signal (max 25)
            growth_str = market.get('growth_2025', '+0%')
            growth_pct = int(growth_str.replace('+', '').replace('%', '')) if growth_str else 0
            opp_score += min(growth_pct * 0.15, 25)
            # Market size signal (max 20)
            pop = market.get('population', 0) * market.get('smartphone_pct', 0.5)
            if pop >= 100_000_000:
                opp_score += 20
            elif pop >= 30_000_000:
                opp_score += 15
            elif pop >= 10_000_000:
                opp_score += 10
            elif pop >= 5_000_000:
                opp_score += 5
            # Competition weakness (max 20)
            opp_score += min(total_frustrations * 0.3, 20)

            opp_score = round(min(opp_score, 100))
        else:
            avg_neg = 0
            opp_score = 0

        market_scores[mc] = {
            'name': market.get('name', mc),
            'opportunity_score': opp_score,
            'avg_negative_ratio': round(avg_neg, 1),
            'total_frustrations': total_frustrations,
            'total_installs': total_installs,
            'apps_analyzed': app_count,
            'growth': market.get('growth_2025', '?'),
            'population': market.get('population', 0),
            'results': market_results,
        }

        all_results[mc] = market_results

    # ── RANKING ──
    print(f"\n{'#'*70}")
    print(f"  GEO RANKING — Ou lancer en priorite ?")
    print(f"{'#'*70}")

    ranked = sorted(market_scores.items(), key=lambda x: -x[1]['opportunity_score'])

    print(f"\n  {'#':3s} {'Pays':15s} {'Score':>7s} {'Neg%':>6s} {'Frust':>7s} {'Growth':>8s} {'Pop':>12s} {'Signal'}")
    print(f"  {'-'*3} {'-'*15} {'-'*7} {'-'*6} {'-'*7} {'-'*8} {'-'*12} {'-'*20}")

    for i, (mc, data) in enumerate(ranked, 1):
        score = data['opportunity_score']
        if score >= 70:
            signal = "*** FORTE OPPORTUNITE"
        elif score >= 50:
            signal = "** OPPORTUNITE"
        elif score >= 30:
            signal = "* A EXPLORER"
        else:
            signal = "- FAIBLE"

        pop_str = f"{data['population']:,}"
        print(f"  {i:3d} {data['name']:15s} {score:>5d}/100 {data['avg_negative_ratio']:>5.1f}% {data['total_frustrations']:>7d} {data['growth']:>8s} {pop_str:>12s} {signal}")

    # Best market
    best_mc, best_data = ranked[0]
    print(f"\n  {'*'*50}")
    print(f"  MEILLEUR MARCHE: {best_data['name']} ({best_mc})")
    print(f"  Score: {best_data['opportunity_score']}/100")
    print(f"  Raison: {MARKETS.get(best_mc, {}).get('notes', '')}")
    print(f"  {'*'*50}")

    # Language clusters
    print(f"\n  CLUSTERS LINGUISTIQUES:")
    lang_clusters = {}
    for mc, data in ranked:
        lang = MARKETS.get(mc, {}).get('lang', '?')
        if lang not in lang_clusters:
            lang_clusters[lang] = []
        lang_clusters[lang].append((mc, data))

    for lang, markets in lang_clusters.items():
        total_pop = sum(MARKETS.get(mc, {}).get('population', 0) for mc, _ in markets)
        avg_score = sum(d['opportunity_score'] for _, d in markets) / len(markets)
        countries = ', '.join(MARKETS.get(mc, {}).get('name', mc) for mc, _ in markets)
        print(f"    {lang:3s} : {countries}")
        print(f"         Pop totale: {total_pop:,} | Score moyen: {avg_score:.0f}/100")

    # Strategy recommendation
    print(f"\n  STRATEGIE RECOMMANDEE:")
    top3 = ranked[:3]
    print(f"    1. Lancer en {top3[0][1]['name']} (score {top3[0][1]['opportunity_score']})")
    if len(top3) > 1:
        print(f"    2. Expansion rapide vers {top3[1][1]['name']} (score {top3[1][1]['opportunity_score']})")
    if len(top3) > 2:
        print(f"    3. Puis {top3[2][1]['name']} (score {top3[2][1]['opportunity_score']})")

    # Check if same language = easy expansion
    best_lang = MARKETS.get(best_mc, {}).get('lang', '')
    same_lang = [mc for mc, _ in ranked if MARKETS.get(mc, {}).get('lang', '') == best_lang and mc != best_mc]
    if same_lang:
        names = ', '.join(MARKETS.get(mc, {}).get('name', mc) for mc in same_lang)
        print(f"    --> Expansion facile (meme langue): {names}")

    print(f"{'#'*70}")

    # Save report
    report = {
        'date': datetime.now().isoformat(),
        'app_ids': app_ids,
        'markets_scanned': market_codes,
        'ranking': [(mc, data) for mc, data in ranked],
        'best_market': best_mc,
        'strategy': {
            'primary': ranked[0][1]['name'] if ranked else '',
            'secondary': ranked[1][1]['name'] if len(ranked) > 1 else '',
            'tertiary': ranked[2][1]['name'] if len(ranked) > 2 else '',
        }
    }

    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'research')
    os.makedirs(output_dir, exist_ok=True)
    slug = '_'.join(app_ids[:2])[:30].replace('.', '_')
    filepath = os.path.join(output_dir, f"geo_{slug}_{datetime.now():%Y%m%d_%H%M}.json")

    def clean(obj):
        try:
            json.dumps(obj)
            return obj
        except (TypeError, ValueError):
            return str(obj)

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2, default=clean)

    print(f"\n  Rapport: {filepath}")

    return report


def main():
    parser = argparse.ArgumentParser(description="MOAT Geo Scanner — Multi-market opportunity finder")
    parser.add_argument("app_ids", nargs="+", help="Google Play app IDs to analyze")
    parser.add_argument("--markets", "-m", default="fr,es,it,de,us",
                       help="Market codes (comma-separated) or preset: europe, latam, francophone, hispanophone, all")
    parser.add_argument("--reviews", "-r", type=int, default=100, help="Reviews per app per market (default: 100)")
    parser.add_argument("--list-markets", action="store_true", help="List all available markets")
    args = parser.parse_args()

    if args.list_markets:
        print(f"\n  Available markets:")
        print(f"  {'Code':5s} {'Pays':15s} {'Pop':>12s} {'Growth':>8s} {'Lang':>5s}")
        print(f"  {'-'*50}")
        for code, m in sorted(MARKETS.items()):
            print(f"  {code:5s} {m['name']:15s} {m['population']:>12,} {m['growth_2025']:>8s} {m['lang']:>5s}")
        print(f"\n  Presets: {', '.join(MARKET_PRESETS.keys())}")
        return

    # Resolve market preset
    market_str = args.markets
    if market_str in MARKET_PRESETS:
        market_codes = MARKET_PRESETS[market_str]
    else:
        market_codes = [m.strip() for m in market_str.split(',')]

    # Validate markets
    valid = [m for m in market_codes if m in MARKETS]
    invalid = [m for m in market_codes if m not in MARKETS]
    if invalid:
        print(f"  WARNING: Unknown markets ignored: {invalid}")
    if not valid:
        print(f"  ERROR: No valid markets. Use --list-markets to see options.")
        return

    geo_scan(args.app_ids, valid, args.reviews)


if __name__ == "__main__":
    main()
