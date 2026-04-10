#!/usr/bin/env python3
"""
MOAT App Discovery System - Google Trends Radar

Analyse les tendances de recherche pour valider la demande :
- Volume relatif sur 12 mois
- Tendance (croissante, stable, decroissante)
- Comparaison entre mots-cles
- Requetes associees (related queries)
- Interet par region

Usage:
    python trend_radar.py "meditation app"
    python trend_radar.py "suivi sommeil" "insomnie" "CBT insomnie" --geo FR
    python trend_radar.py "devis artisan" "facturation auto-entrepreneur" --geo FR --compare
"""

import argparse
import sys
import time
from datetime import datetime

try:
    from pytrends.request import TrendReq
    HAS_PYTRENDS = True
except ImportError:
    HAS_PYTRENDS = False
    print("ERREUR: pytrends non installe. Run: pip install pytrends")


def analyze_trend(keywords, geo="FR", timeframe="today 12-m"):
    """Analyze Google Trends for given keywords."""
    pytrends = TrendReq(hl='fr-FR', tz=60)

    # Build payload (max 5 keywords)
    kw_list = keywords[:5]
    pytrends.build_payload(kw_list, cat=0, timeframe=timeframe, geo=geo)

    results = {}

    # Interest over time
    print(f"\n  Fetching interest over time...")
    try:
        iot = pytrends.interest_over_time()
        if not iot.empty:
            for kw in kw_list:
                if kw in iot.columns:
                    values = iot[kw].tolist()
                    current = values[-1] if values else 0
                    avg = sum(values) / len(values) if values else 0
                    peak = max(values) if values else 0
                    trend_start = sum(values[:len(values)//4]) / max(len(values)//4, 1)
                    trend_end = sum(values[-len(values)//4:]) / max(len(values)//4, 1)

                    if trend_end > trend_start * 1.2:
                        direction = "CROISSANTE"
                    elif trend_end < trend_start * 0.8:
                        direction = "DECROISSANTE"
                    else:
                        direction = "STABLE"

                    growth = round((trend_end - trend_start) / max(trend_start, 1) * 100, 1)

                    results[kw] = {
                        "current": current,
                        "average": round(avg, 1),
                        "peak": peak,
                        "direction": direction,
                        "growth_pct": growth,
                        "values": values,
                    }
    except Exception as e:
        print(f"  Erreur interest_over_time: {e}")

    # Related queries
    print(f"  Fetching related queries...")
    try:
        related = pytrends.related_queries()
        for kw in kw_list:
            if kw in related and related[kw]:
                top = related[kw].get("top")
                rising = related[kw].get("rising")
                if kw in results:
                    results[kw]["related_top"] = top.head(10).to_dict('records') if top is not None and not top.empty else []
                    results[kw]["related_rising"] = rising.head(10).to_dict('records') if rising is not None and not rising.empty else []
    except Exception as e:
        print(f"  Erreur related_queries: {e}")

    # Interest by region
    print(f"  Fetching interest by region...")
    try:
        ibr = pytrends.interest_by_region(resolution='COUNTRY', inc_low_vol=False)
        if not ibr.empty:
            for kw in kw_list:
                if kw in ibr.columns and kw in results:
                    top_regions = ibr[kw].sort_values(ascending=False).head(10)
                    results[kw]["top_regions"] = {k: v for k, v in top_regions.items() if v > 0}
    except Exception as e:
        print(f"  Erreur interest_by_region: {e}")

    return results


def display_results(results, keywords):
    """Display trend analysis results."""
    print(f"\n{'='*70}")
    print(f"  MOAT Trend Radar - {datetime.now().strftime('%Y-%m-%d')}")
    print(f"{'='*70}")

    for kw in keywords:
        if kw not in results:
            print(f"\n  [{kw}] - Pas de donnees")
            continue

        data = results[kw]
        direction = data.get("direction", "?")
        arrow = {"CROISSANTE": "/\\", "DECROISSANTE": "\\/", "STABLE": "=="}.get(direction, "?")

        print(f"\n  [{kw}]")
        print(f"  {'Tendance':20s} : {arrow} {direction} ({data.get('growth_pct', 0):+.1f}%)")
        print(f"  {'Index actuel':20s} : {data.get('current', 0)}/100")
        print(f"  {'Moyenne 12 mois':20s} : {data.get('average', 0)}/100")
        print(f"  {'Pic':20s} : {data.get('peak', 0)}/100")

        # Mini sparkline
        values = data.get("values", [])
        if values:
            # Simplify to 12 points (monthly)
            step = max(len(values) // 12, 1)
            monthly = values[::step][:12]
            max_val = max(monthly) if monthly else 1
            sparkline = ""
            for v in monthly:
                level = int(v / max(max_val, 1) * 4)
                chars = [" ", ".", ":", "|", "#"]
                sparkline += chars[min(level, 4)]
            print(f"  {'Sparkline 12 mois':20s} : [{sparkline}]")

        # Related queries
        rising = data.get("related_rising", [])
        if rising:
            print(f"\n  Requetes en hausse:")
            for r in rising[:5]:
                query = r.get("query", "?")
                value = r.get("value", "?")
                print(f"    +{value}  {query}")

        top = data.get("related_top", [])
        if top:
            print(f"\n  Requetes associees populaires:")
            for r in top[:5]:
                query = r.get("query", "?")
                value = r.get("value", "?")
                print(f"    {value:4}  {query}")

        # Top regions
        regions = data.get("top_regions", {})
        if regions:
            print(f"\n  Top regions:")
            for region, val in list(regions.items())[:5]:
                print(f"    {region:20s} {val}")

    print(f"\n{'='*70}")

    # Comparison verdict
    if len(results) > 1:
        print(f"\n  COMPARAISON:")
        sorted_kws = sorted(results.items(), key=lambda x: x[1].get("average", 0), reverse=True)
        for i, (kw, data) in enumerate(sorted_kws, 1):
            dir_icon = {"CROISSANTE": "[UP]", "DECROISSANTE": "[DOWN]", "STABLE": "[==]"}.get(data.get("direction", ""), "[?]")
            print(f"    {i}. {kw:30s} avg={data.get('average',0):5.1f}  {dir_icon}  {data.get('growth_pct',0):+.1f}%")
        print(f"\n  Meilleur signal: {sorted_kws[0][0]} (avg={sorted_kws[0][1].get('average',0):.1f}, {sorted_kws[0][1].get('direction','')})")

    print(f"{'='*70}")
    return results


def main():
    if not HAS_PYTRENDS:
        sys.exit(1)

    parser = argparse.ArgumentParser(description="MOAT Google Trends Radar")
    parser.add_argument("keywords", nargs="+", help="Keywords to analyze (max 5)")
    parser.add_argument("--geo", default="FR", help="Geographic region (default: FR)")
    parser.add_argument("--timeframe", default="today 12-m", help="Timeframe (default: today 12-m)")
    parser.add_argument("--compare", action="store_true", help="Compare mode")
    args = parser.parse_args()

    results = analyze_trend(args.keywords, args.geo, args.timeframe)
    display_results(results, args.keywords)


if __name__ == "__main__":
    main()
