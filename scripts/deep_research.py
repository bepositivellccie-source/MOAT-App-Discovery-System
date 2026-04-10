#!/usr/bin/env python3
"""
MOAT App Discovery System - Deep Research

Recherche approfondie complete pour une idee d'app.
Combine : Google Play intel + Google Trends + scoring + rapport.

Usage:
    python deep_research.py "sleep coach" --keywords "insomnie,CBT-I,sommeil app" --competitors "com.northcube.sleepcycle,com.calm.android"
    python deep_research.py "devis artisan" --keywords "devis artisan,facture auto-entrepreneur" --competitors "fr.zenartisan"
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime

# Import MOAT modules
sys.path.insert(0, os.path.dirname(__file__))

try:
    from playstore_intel import search_apps, get_app_info, get_reviews_analysis
    HAS_PLAYSTORE = True
except ImportError:
    HAS_PLAYSTORE = False

try:
    from trend_radar import analyze_trend
    HAS_TRENDS = True
except ImportError:
    HAS_TRENDS = False


def deep_research(idea_name, search_query=None, keywords=None, competitor_ids=None, lang="fr", geo="FR"):
    """Run complete deep research for an app idea."""
    report = {
        "idea": idea_name,
        "date": datetime.now().isoformat(),
        "search_query": search_query or idea_name,
        "playstore": {},
        "trends": {},
        "competitors": [],
        "gaps": [],
        "verdict": {},
    }

    print(f"\n{'#'*70}")
    print(f"  MOAT DEEP RESEARCH: {idea_name}")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'#'*70}")

    # ── PHASE 1: Google Play Market Scan ──
    if HAS_PLAYSTORE:
        query = search_query or idea_name
        print(f"\n{'='*60}")
        print(f"  PHASE 1: Google Play Market Scan")
        print(f"  Query: '{query}'")
        print(f"{'='*60}")

        # Search for competitors
        apps = search_apps(query, lang=lang, top=15)
        report["playstore"]["search_results"] = apps

        if apps and "error" not in apps[0]:
            # Market overview
            scores = [a["score"] for a in apps if a.get("score")]
            installs = [a["installs"] for a in apps if isinstance(a.get("installs"), int)]

            market = {
                "total_apps_found": len(apps),
                "avg_score": round(sum(scores) / max(len(scores), 1), 2),
                "min_score": round(min(scores), 1) if scores else 0,
                "max_score": round(max(scores), 1) if scores else 0,
                "apps_below_4": len([s for s in scores if s < 4.0]),
                "total_installs_top10": sum(installs[:10]) if installs else 0,
            }
            report["playstore"]["market"] = market

            print(f"\n  MARCHE:")
            print(f"    Apps trouvees          : {market['total_apps_found']}")
            print(f"    Score moyen            : {market['avg_score']}/5")
            print(f"    Score min/max          : {market['min_score']} / {market['max_score']}")
            print(f"    Apps sous 4.0 etoiles  : {market['apps_below_4']}/{len(scores)} ({round(market['apps_below_4']/max(len(scores),1)*100)}%)")
            print(f"    Installs cumules Top10 : {market['total_installs_top10']:,}")

            opp_level = "FORT" if market["apps_below_4"] > len(scores) / 2 else "MOYEN" if market["apps_below_4"] > 2 else "FAIBLE"
            print(f"    Signal d'opportunite   : {opp_level}")
            report["playstore"]["opportunity_signal"] = opp_level

            # Show top apps
            print(f"\n  TOP APPS:")
            print(f"  {'#':3s} {'Score':6s} {'Installs':>12s} {'App'}")
            print(f"  {'-'*3} {'-'*6} {'-'*12} {'-'*40}")
            for i, a in enumerate(apps[:10], 1):
                inst = f"{a['installs']:,}" if isinstance(a.get('installs'), int) else "?"
                score = f"{a['score']:.1f}" if a.get('score') else "N/A"
                print(f"  {i:3d} {score:6s} {inst:>12s} {a.get('title', '?')[:40]}")

        # Analyze specific competitors
        comp_ids = competitor_ids or []
        if not comp_ids and apps:
            # Auto-select top 3 from search
            comp_ids = [a["id"] for a in apps[:3] if a.get("id")]

        if comp_ids:
            print(f"\n{'='*60}")
            print(f"  PHASE 1b: Analyse detaillee des concurrents")
            print(f"{'='*60}")

            for cid in comp_ids[:5]:
                print(f"\n  --- {cid} ---")
                info = get_app_info(cid, lang=lang)
                reviews_data = get_reviews_analysis(cid, lang=lang, count=150)

                competitor = {"info": info, "reviews": reviews_data}
                report["competitors"].append(competitor)

                if "error" not in info:
                    print(f"  {info.get('title', '?')}")
                    print(f"    Score     : {info.get('score', '?')}/5 ({info.get('ratings', '?'):,} avis)")
                    print(f"    Installs  : {info.get('installs', '?'):,}")
                    print(f"    Free      : {'Oui' if info.get('free') else 'Non'}")
                    print(f"    Ads       : {'Oui' if info.get('contains_ads') else 'Non'}")

                if "error" not in reviews_data:
                    print(f"    Negatifs  : {reviews_data.get('negative_ratio', '?')}%")
                    if reviews_data.get("top_frustrations"):
                        print(f"    Top frustrations:")
                        for marker, count in reviews_data["top_frustrations"][:5]:
                            print(f"      - {marker} ({count}x)")
                        # Extract gaps
                        for marker, count in reviews_data["top_frustrations"][:3]:
                            report["gaps"].append({
                                "app": info.get("title", cid),
                                "frustration": marker,
                                "count": count,
                            })

    else:
        print("\n  [SKIP] Google Play (google-play-scraper non installe)")

    # ── PHASE 2: Google Trends ──
    if HAS_TRENDS and keywords:
        kw_list = [k.strip() for k in keywords.split(",")]

        print(f"\n{'='*60}")
        print(f"  PHASE 2: Google Trends Analysis")
        print(f"  Keywords: {kw_list}")
        print(f"{'='*60}")

        try:
            trends = analyze_trend(kw_list, geo=geo)
            report["trends"] = {}

            for kw in kw_list:
                if kw in trends:
                    data = trends[kw]
                    direction = data.get("direction", "?")
                    arrow = {"CROISSANTE": "/\\", "DECROISSANTE": "\\/", "STABLE": "=="}.get(direction, "?")

                    print(f"\n  [{kw}]")
                    print(f"    Tendance  : {arrow} {direction} ({data.get('growth_pct', 0):+.1f}%)")
                    print(f"    Index     : {data.get('current', 0)}/100 (avg: {data.get('average', 0):.0f})")

                    report["trends"][kw] = {
                        "direction": direction,
                        "growth_pct": data.get("growth_pct", 0),
                        "current": data.get("current", 0),
                        "average": data.get("average", 0),
                        "peak": data.get("peak", 0),
                    }

                    rising = data.get("related_rising", [])
                    if rising:
                        print(f"    En hausse :")
                        for r in rising[:3]:
                            print(f"      +{r.get('value', '?')}  {r.get('query', '?')}")
        except Exception as e:
            print(f"  Erreur Trends: {e}")

    else:
        print("\n  [SKIP] Google Trends (pytrends non installe ou pas de keywords)")

    # ── PHASE 3: Verdict ──
    print(f"\n{'='*60}")
    print(f"  VERDICT")
    print(f"{'='*60}")

    # Score components
    market_opp = report.get("playstore", {}).get("opportunity_signal", "INCONNU")
    trend_signals = report.get("trends", {})
    gaps = report.get("gaps", [])

    growing_keywords = [k for k, v in trend_signals.items() if v.get("direction") == "CROISSANTE"]
    declining_keywords = [k for k, v in trend_signals.items() if v.get("direction") == "DECROISSANTE"]

    print(f"\n  Signal marche Play Store : {market_opp}")
    print(f"  Keywords en hausse       : {len(growing_keywords)}/{len(trend_signals)}")
    if growing_keywords:
        for k in growing_keywords:
            print(f"    + {k} ({trend_signals[k].get('growth_pct', 0):+.1f}%)")
    if declining_keywords:
        print(f"  Keywords en baisse       :")
        for k in declining_keywords:
            print(f"    - {k} ({trend_signals[k].get('growth_pct', 0):+.1f}%)")

    print(f"  Gaps concurrentiels      : {len(gaps)}")
    if gaps:
        for g in gaps[:5]:
            print(f"    {g['app']}: {g['frustration']} ({g['count']}x)")

    # Overall verdict
    score = 0
    if market_opp == "FORT":
        score += 3
    elif market_opp == "MOYEN":
        score += 2
    score += min(len(growing_keywords), 3)
    score += min(len(gaps), 3)
    score -= len(declining_keywords)

    if score >= 6:
        verdict = "GO - Signaux tres forts, lancer la validation"
    elif score >= 4:
        verdict = "PROMETTEUR - Creuser les hypotheses"
    elif score >= 2:
        verdict = "MITIGE - Besoin de plus d'evidence"
    else:
        verdict = "FAIBLE - Revoir l'angle ou abandonner"

    report["verdict"] = {
        "score": score,
        "label": verdict,
        "market_signal": market_opp,
        "growing_keywords": growing_keywords,
        "declining_keywords": declining_keywords,
        "gaps_found": len(gaps),
    }

    print(f"\n  {'*'*50}")
    print(f"  VERDICT: {verdict}")
    print(f"  Score data: {score}/9")
    print(f"  {'*'*50}")

    # Save
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "research")
    os.makedirs(output_dir, exist_ok=True)
    slug = re.sub(r'[^\w]', '_', idea_name.lower())
    filepath = os.path.join(output_dir, f"deep_{slug}_{datetime.now():%Y%m%d_%H%M}.json")

    def clean(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        try:
            json.dumps(obj)
            return obj
        except (TypeError, ValueError):
            return str(obj)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2, default=clean)

    print(f"\n  Rapport complet sauvegarde: {filepath}")
    print(f"{'#'*70}")

    return report


def main():
    parser = argparse.ArgumentParser(description="MOAT Deep Research")
    parser.add_argument("idea", help="Nom de l'idee a rechercher")
    parser.add_argument("--search", "-s", help="Search query Google Play (defaut: nom de l'idee)")
    parser.add_argument("--keywords", "-k", help="Keywords Google Trends (separes par virgule)")
    parser.add_argument("--competitors", "-c", help="App IDs concurrents (separes par virgule)")
    parser.add_argument("--lang", default="fr", help="Langue (defaut: fr)")
    parser.add_argument("--geo", default="FR", help="Region Google Trends (defaut: FR)")
    args = parser.parse_args()

    comp_ids = args.competitors.split(",") if args.competitors else None

    deep_research(
        idea_name=args.idea,
        search_query=args.search,
        keywords=args.keywords,
        competitor_ids=comp_ids,
        lang=args.lang,
        geo=args.geo,
    )


if __name__ == "__main__":
    main()
