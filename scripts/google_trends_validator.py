#!/usr/bin/env python3
"""
MOAT App Discovery System — Google Trends Validator

Compare 3 territoires sur 5 ans via Google Trends.
Donnees brutes uniquement. Pas d'analyse, pas de recommandation.

Usage:
    python scripts/google_trends_validator.py
"""

import sys
import time
import os
from datetime import datetime

try:
    from pytrends.request import TrendReq
except ImportError:
    print("Installing pytrends...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pytrends", "--quiet"])
    from pytrends.request import TrendReq

import csv


# ── 3 territoires, termes FR + EN pour maximiser le signal ──
TERRITORIES = {
    'T1 - Hypersensibilite / HSP': {
        'terms': ['highly sensitive person', 'hypersensible'],
        'description': 'Hypersensibilite / HSP',
    },
    'T2 - Gestion colere': {
        'terms': ['anger management', 'gestion colere'],
        'description': 'Gestion de la colere',
    },
    'T3 - Facturation freelance': {
        'terms': ['time tracking freelance', 'facturation freelance'],
        'description': 'Facturation / time tracking freelance',
    },
}


def fetch_trends(terms, timeframe='today 5-y', geo=''):
    """Fetch Google Trends data for a list of terms."""
    pytrends = TrendReq(hl='fr-FR', tz=60)

    # pytrends max 5 terms per request
    pytrends.build_payload(terms, cat=0, timeframe=timeframe, geo=geo)
    df = pytrends.interest_over_time()

    if df.empty:
        return None

    # Drop isPartial column if exists
    if 'isPartial' in df.columns:
        df = df.drop(columns=['isPartial'])

    return df


def analyze_term(df, term):
    """Calculate stats for a single term."""
    if term not in df.columns:
        return None

    values = df[term].tolist()
    if not values:
        return None

    avg_total = sum(values) / len(values)
    current = values[-1]
    peak = max(values)

    # Last 6 months average
    last_6m = values[-26:]  # ~6 months of weekly data
    avg_6m = sum(last_6m) / len(last_6m)

    # Direction
    if avg_6m > avg_total * 1.1:
        direction = 'UP'
    elif avg_6m < avg_total * 0.9:
        direction = 'DOWN'
    else:
        direction = 'STABLE'

    return {
        'term': term,
        'avg_5y': round(avg_total, 1),
        'current': current,
        'peak': peak,
        'avg_6m': round(avg_6m, 1),
        'direction': direction,
    }


def main():
    print(f"\n{'='*70}")
    print(f"  MOAT TRENDS VALIDATOR")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"  Timeframe: 5 ans | Geo: Monde entier")
    print(f"{'='*70}")

    all_data = {}
    all_stats = []

    for territory_name, config in TERRITORIES.items():
        terms = config['terms']
        print(f"\n  Fetching: {territory_name}")
        print(f"  Terms: {terms}")

        try:
            df = fetch_trends(terms)

            if df is None:
                print(f"  [WARN] No data returned for {terms}")
                continue

            for term in terms:
                stats = analyze_term(df, term)
                if stats:
                    all_stats.append({**stats, 'territory': territory_name})
                    all_data[term] = df[term]

                    dir_icon = {'UP': '/\\', 'DOWN': '\\/', 'STABLE': '=='}[stats['direction']]
                    print(f"    {term:35s} avg={stats['avg_5y']:5.1f}  now={stats['current']:3d}  peak={stats['peak']:3d}  6m={stats['avg_6m']:5.1f}  {dir_icon} {stats['direction']}")

        except Exception as e:
            print(f"  [ERROR] {str(e)[:60]}")

        # Rate limit protection
        print(f"  Waiting 5s...")
        time.sleep(5)

    # ── Export CSV ──
    if all_data:
        output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'trends_output.csv')

        # Build DataFrame manually for CSV
        # Get dates from first available term
        first_term = list(all_data.keys())[0]
        dates = all_data[first_term].index

        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            header = ['date'] + list(all_data.keys())
            writer.writerow(header)

            for date in dates:
                row = [date.strftime('%Y-%m-%d')]
                for term in all_data:
                    try:
                        row.append(all_data[term][date])
                    except:
                        row.append('')
                writer.writerow(row)

        print(f"\n  CSV exported: {output_path}")

    # ── Summary ──
    print(f"\n{'='*70}")
    print(f"  RESUME — Donnees brutes")
    print(f"{'='*70}")
    print(f"\n  {'Terme':35s} {'Moy 5a':>7s} {'Actuel':>7s} {'Pic':>5s} {'Moy 6m':>7s} {'Dir':>8s}")
    print(f"  {'-'*35} {'-'*7} {'-'*7} {'-'*5} {'-'*7} {'-'*8}")

    for s in all_stats:
        dir_icon = {'UP': '/\\  UP', 'DOWN': '\\/  DOWN', 'STABLE': '==  STABLE'}[s['direction']]
        print(f"  {s['term']:35s} {s['avg_5y']:>6.1f} {s['current']:>7d} {s['peak']:>5d} {s['avg_6m']:>6.1f} {dir_icon:>8s}")

    print(f"\n  Pas d'analyse. Pas de recommandation. Juste les donnees.")
    print(f"  L'analyse se fait avec le MOAT Engine.\n")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
