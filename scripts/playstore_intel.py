#!/usr/bin/env python3
"""
MOAT App Discovery System - Google Play Intelligence

Analyse les apps concurrentes sur Google Play :
- Ratings, nombre d'avis, installations
- Extraction des frustrations (avis 1-3 etoiles)
- Patterns de plaintes recurrentes
- Gaps exploitables

Usage:
    python playstore_intel.py "com.calm.android"
    python playstore_intel.py "com.calm.android" "com.headspace.android" --lang fr
    python playstore_intel.py --search "meditation" --lang fr --top 10
    python playstore_intel.py --search "devis artisan" --lang fr --report
"""

import argparse
import json
import os
import sys
import re
from collections import Counter
from datetime import datetime

try:
    from google_play_scraper import app, reviews, search, Sort
    HAS_SCRAPER = True
except ImportError:
    HAS_SCRAPER = False
    print("ERREUR: google-play-scraper non installe. Run: pip install google-play-scraper")


# Frustration keywords
FRUSTRATION_FR = [
    "bug", "plante", "crash", "lent", "lente", "complique", "cher", "chere",
    "payant", "payante", "manque", "impossible", "nul", "nulle", "mauvais",
    "horrible", "decevant", "inutile", "pub", "publicite", "abonnement",
    "force", "oblige", "perdu", "supprime", "disparu", "bloque", "erreur",
    "probleme", "difficile", "confus", "incomprehensible", "arnaque",
    "fonctionne pas", "marche pas", "ne marche", "ne fonctionne",
    "trop cher", "premium", "gratuit", "freemium", "desinstalle",
]

FRUSTRATION_EN = [
    "bug", "crash", "slow", "complicated", "expensive", "missing",
    "useless", "bad", "horrible", "disappointing", "ads", "subscription",
    "forced", "deleted", "lost", "broken", "error", "problem", "difficult",
    "confusing", "frustrating", "doesn't work", "annoying", "waste",
    "uninstall", "scam", "paywall", "premium", "too expensive",
]


def get_app_info(app_id, lang="fr", country="fr"):
    """Get detailed app information."""
    try:
        result = app(app_id, lang=lang, country=country)
        return {
            "id": app_id,
            "title": result.get("title", ""),
            "developer": result.get("developer", ""),
            "score": result.get("score", 0),
            "ratings": result.get("ratings", 0),
            "reviews_count": result.get("reviews", 0),
            "installs": result.get("realInstalls", result.get("installs", "?")),
            "free": result.get("free", True),
            "price": result.get("price", 0),
            "contains_ads": result.get("containsAds", False),
            "iap_range": result.get("inAppProductPrice", ""),
            "genre": result.get("genre", ""),
            "content_rating": result.get("contentRating", ""),
            "updated": result.get("updated", ""),
            "version": result.get("version", ""),
            "description_short": result.get("summary", "")[:200],
            "histogram": result.get("histogram", []),
        }
    except Exception as e:
        return {"id": app_id, "error": str(e)}


def get_reviews_analysis(app_id, lang="fr", country="fr", count=200):
    """Get and analyze reviews for an app."""
    try:
        # Get negative reviews (1-3 stars)
        result_negative, _ = reviews(
            app_id,
            lang=lang,
            country=country,
            sort=Sort.NEWEST,
            count=count,
            filter_score_with=None,
        )

        all_reviews = result_negative
        negative = [r for r in all_reviews if r.get("score", 5) <= 3]
        positive = [r for r in all_reviews if r.get("score", 5) >= 4]

        # Extract frustration patterns
        markers = FRUSTRATION_FR if lang == "fr" else FRUSTRATION_EN
        frustration_counts = Counter()
        frustration_examples = {}

        for review in negative:
            content = review.get("content", "").lower()
            for marker in markers:
                if marker in content:
                    frustration_counts[marker] += 1
                    if marker not in frustration_examples:
                        frustration_examples[marker] = review.get("content", "")[:150]

        # Extract key themes from negative reviews
        negative_texts = [r.get("content", "") for r in negative]

        return {
            "total_fetched": len(all_reviews),
            "negative_count": len(negative),
            "positive_count": len(positive),
            "negative_ratio": round(len(negative) / max(len(all_reviews), 1) * 100, 1),
            "avg_negative_score": round(sum(r.get("score", 0) for r in negative) / max(len(negative), 1), 2),
            "top_frustrations": frustration_counts.most_common(15),
            "frustration_examples": frustration_examples,
            "sample_negative": [r.get("content", "")[:200] for r in negative[:5]],
            "sample_positive": [r.get("content", "")[:200] for r in positive[:3]],
        }
    except Exception as e:
        return {"error": str(e)}


def search_apps(query, lang="fr", country="fr", top=10):
    """Search Google Play for apps."""
    try:
        results = search(query, lang=lang, country=country, n_hits=top)
        apps = []
        for r in results:
            apps.append({
                "id": r.get("appId", ""),
                "title": r.get("title", ""),
                "score": r.get("score", 0),
                "installs": r.get("realInstalls", r.get("installs", "?")),
                "free": r.get("free", True),
                "developer": r.get("developer", ""),
                "genre": r.get("genre", ""),
            })
        return apps
    except Exception as e:
        return [{"error": str(e)}]


def generate_report(app_id, lang="fr", country="fr"):
    """Generate a full intelligence report for an app."""
    print(f"\n{'='*60}")
    print(f"  MOAT Play Store Intelligence Report")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}")

    # App info
    print(f"\n  Fetching app info: {app_id}...")
    info = get_app_info(app_id, lang, country)

    if "error" in info:
        print(f"  ERREUR: {info['error']}")
        return info

    print(f"\n  APP: {info['title']}")
    print(f"  Developer: {info['developer']}")
    print(f"  Score: {info['score']}/5")
    print(f"  Ratings: {info['ratings']:,}")
    print(f"  Installs: {info['installs']:,}")
    print(f"  Free: {'Oui' if info['free'] else 'Non'}")
    print(f"  Contains Ads: {'Oui' if info['contains_ads'] else 'Non'}")
    print(f"  IAP: {info['iap_range']}")
    print(f"  Genre: {info['genre']}")

    if info.get("histogram"):
        h = info["histogram"]
        total = sum(h) if h else 1
        print(f"\n  Distribution des notes:")
        for i, count in enumerate(h):
            stars = i + 1
            pct = round(count / total * 100, 1)
            bar = "#" * int(pct / 2)
            print(f"    {stars} star: {bar} {pct}% ({count:,})")

    # Reviews analysis
    print(f"\n  Analyzing reviews...")
    analysis = get_reviews_analysis(app_id, lang, country)

    if "error" in analysis:
        print(f"  ERREUR reviews: {analysis['error']}")
    else:
        print(f"\n  REVIEWS ANALYSIS:")
        print(f"  Total fetched: {analysis['total_fetched']}")
        print(f"  Negative (1-3): {analysis['negative_count']} ({analysis['negative_ratio']}%)")
        print(f"  Positive (4-5): {analysis['positive_count']}")

        if analysis["top_frustrations"]:
            print(f"\n  TOP FRUSTRATIONS:")
            for marker, count in analysis["top_frustrations"][:10]:
                bar = "#" * min(count, 30)
                print(f"    {marker:25s} {bar} ({count})")

        if analysis["sample_negative"]:
            print(f"\n  EXEMPLES AVIS NEGATIFS:")
            for i, text in enumerate(analysis["sample_negative"], 1):
                print(f"    {i}. {text}")

    print(f"\n{'='*60}")

    return {"info": info, "analysis": analysis}


def competitive_search(query, lang="fr", country="fr", top=10):
    """Search and analyze top competitors for a keyword."""
    print(f"\n{'='*60}")
    print(f"  MOAT Competitive Analysis: '{query}'")
    print(f"{'='*60}")

    apps = search_apps(query, lang, country, top)

    if not apps or "error" in apps[0]:
        print(f"  Erreur de recherche")
        return

    print(f"\n  {len(apps)} apps trouvees:\n")
    print(f"  {'#':3s} {'Score':6s} {'Installs':>12s} {'App':40s} {'Developer'}")
    print(f"  {'-'*3} {'-'*6} {'-'*12} {'-'*40} {'-'*20}")

    for i, a in enumerate(apps, 1):
        installs = f"{a['installs']:,}" if isinstance(a['installs'], int) else str(a['installs'])
        score = f"{a['score']:.1f}" if a['score'] else "N/A"
        title = a['title'][:38]
        dev = a['developer'][:20]
        print(f"  {i:3d} {score:6s} {installs:>12s} {title:40s} {dev}")

    # Analyze top 3 in detail
    print(f"\n  Analyse detaillee des 3 premiers...\n")
    reports = []
    for a in apps[:3]:
        if a.get("id"):
            report = generate_report(a["id"], lang, country)
            reports.append(report)

    # Summary
    print(f"\n{'='*60}")
    print(f"  SYNTHESE COMPETITIVE")
    print(f"{'='*60}")

    scores = [a['score'] for a in apps if a.get('score')]
    if scores:
        print(f"  Score moyen du marche: {sum(scores)/len(scores):.2f}/5")
        print(f"  Score min: {min(scores):.1f} | Score max: {max(scores):.1f}")

    low_rated = [a for a in apps if a.get('score') and a['score'] < 4.0]
    if low_rated:
        print(f"  Apps sous 4.0: {len(low_rated)}/{len(apps)} ({round(len(low_rated)/len(apps)*100)}%)")
        print(f"  -> Signal d'opportunite {'FORT' if len(low_rated) > len(apps)/2 else 'MOYEN'}")

    return {"apps": apps, "reports": reports}


def save_report_json(data, filename):
    """Save report as JSON."""
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "research")
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)

    # Clean data for JSON serialization
    def clean(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return str(obj)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=clean)

    print(f"\n  Rapport sauvegarde: {filepath}")
    return filepath


def main():
    if not HAS_SCRAPER:
        sys.exit(1)

    parser = argparse.ArgumentParser(description="MOAT Google Play Intelligence")
    parser.add_argument("app_ids", nargs="*", help="Google Play app IDs (e.g., com.calm.android)")
    parser.add_argument("--search", "-s", help="Search query on Google Play")
    parser.add_argument("--lang", "-l", default="fr", help="Language (default: fr)")
    parser.add_argument("--country", "-c", default="fr", help="Country (default: fr)")
    parser.add_argument("--top", "-t", type=int, default=10, help="Number of results for search")
    parser.add_argument("--report", "-r", action="store_true", help="Generate full report")
    parser.add_argument("--save", action="store_true", help="Save report as JSON")
    args = parser.parse_args()

    if args.search:
        data = competitive_search(args.search, args.lang, args.country, args.top)
        if args.save and data:
            slug = re.sub(r'[^\w]', '_', args.search.lower())
            save_report_json(data, f"competitive_{slug}_{datetime.now():%Y%m%d}.json")

    elif args.app_ids:
        for app_id in args.app_ids:
            data = generate_report(app_id, args.lang, args.country)
            if args.save and data:
                save_report_json(data, f"app_{app_id}_{datetime.now():%Y%m%d}.json")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
