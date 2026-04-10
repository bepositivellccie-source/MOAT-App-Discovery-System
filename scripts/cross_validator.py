#!/usr/bin/env python3
# -*- coding: cp1252 -*-
"""
MOAT App Discovery System -- Multi-Source Cross-Validator

Validates an app idea against 5 independent axes and produces
a confidence score (0-100) with detailed justification.

Axes:
  1. Demand Validation       (Google Play search data)       0-20 pts
  2. Frustration Validation   (Review sentiment analysis)     0-20 pts
  3. Differentiation Valid.   (Proposed angle vs market)      0-20 pts
  4. Monetization Validation  (Pricing & willingness to pay)  0-20 pts
  5. Execution Validation     (MVP complexity & risk)         0-20 pts

Usage:
    python cross_validator.py "SleepCoach FR" --query "sleep insomnia CBT" \\
        --competitors "com.northcube.sleepcycle,com.calm.android" \\
        --angle "CBT-I therapy vs tracking" --price 6.99

    python cross_validator.py "CoachCRM" --query "coach fitness management" \\
        --angle "CRM vs exercise tracker" --price 9.99

    python cross_validator.py "MyIdea" --query "keyword" --quick
"""

import argparse
import json
import os
import sys
from collections import Counter
from datetime import datetime

try:
    from google_play_scraper import app as gp_app, reviews, search, Sort
    HAS_SCRAPER = True
except ImportError:
    HAS_SCRAPER = False

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

FRUSTRATION_KEYWORDS = [
    "bug", "crash", "slow", "lent", "complicated", "complique", "expensive",
    "cher", "payant", "missing", "manque", "useless", "inutile", "ads", "pub",
    "subscription", "abonnement", "forced", "force", "broken", "error",
    "erreur", "problem", "probleme", "frustrating", "annoying", "scam",
    "arnaque", "doesn't work", "marche pas", "fonctionne pas", "horrible",
    "disappointing", "decevant", "confusing", "confus", "difficult",
    "difficile", "uninstall", "desinstalle", "paywall", "premium",
    "too expensive", "trop cher", "nul", "waste",
]

PRICE_COMPLAINT_KEYWORDS = [
    "expensive", "cher", "trop cher", "too expensive", "overpriced",
    "not worth", "paywall", "premium", "abonnement", "subscription",
    "money", "argent", "prix", "price", "refund", "rembourse",
]

CONFIDENCE_LEVELS = [
    (80, "HIGH CONFIDENCE -- strong multi-source validation"),
    (60, "MODERATE -- some signals strong, others need verification"),
    (40, "LOW -- mixed signals, more research needed"),
    (0,  "VERY LOW -- insufficient evidence"),
]


# ---------------------------------------------------------------------------
# Data collection helpers
# ---------------------------------------------------------------------------

def safe_search(query, lang="fr", country="fr", n_hits=20):
    """Search Google Play, return list of app dicts or empty list on error."""
    if not HAS_SCRAPER:
        return []
    try:
        results = search(query, lang=lang, country=country, n_hits=n_hits)
        return results or []
    except Exception as e:
        print(f"  [WARN] Play Store search failed: {e}")
        return []


def safe_app_info(app_id, lang="fr", country="fr"):
    """Fetch app metadata, return dict or None on error."""
    if not HAS_SCRAPER:
        return None
    try:
        return gp_app(app_id, lang=lang, country=country)
    except Exception as e:
        print(f"  [WARN] Could not fetch app {app_id}: {e}")
        return None


def safe_reviews(app_id, lang="fr", country="fr", count=150):
    """Fetch reviews for an app, return list or empty list on error."""
    if not HAS_SCRAPER:
        return []
    try:
        result, _ = reviews(
            app_id, lang=lang, country=country,
            sort=Sort.NEWEST, count=count, filter_score_with=None,
        )
        return result or []
    except Exception as e:
        print(f"  [WARN] Could not fetch reviews for {app_id}: {e}")
        return []


# ---------------------------------------------------------------------------
# Axis 1: Demand Validation (0-20)
# ---------------------------------------------------------------------------

def validate_demand(query, competitors, lang="fr", country="fr"):
    """Score demand based on search results and install volumes."""
    info = {
        "search_results": 0,
        "total_installs": 0,
        "avg_installs": 0,
        "top_app_installs": 0,
        "competitor_data": [],
        "justification": [],
    }

    # Search Play Store
    results = safe_search(query, lang, country, n_hits=20)
    info["search_results"] = len(results)

    # Gather install data from search results
    installs_list = []
    for r in results:
        inst = r.get("realInstalls", r.get("installs", 0))
        if isinstance(inst, str):
            inst = int(inst.replace(",", "").replace("+", "").strip() or "0")
        installs_list.append(inst)

    if installs_list:
        info["total_installs"] = sum(installs_list)
        info["avg_installs"] = int(sum(installs_list) / len(installs_list))
        info["top_app_installs"] = max(installs_list)

    # Also check named competitors
    for comp_id in competitors:
        comp = safe_app_info(comp_id, lang, country)
        if comp:
            inst = comp.get("realInstalls", comp.get("installs", 0))
            if isinstance(inst, str):
                inst = int(inst.replace(",", "").replace("+", "").strip() or "0")
            info["competitor_data"].append({
                "id": comp_id,
                "title": comp.get("title", comp_id),
                "installs": inst,
                "score": comp.get("score", 0),
            })

    # Scoring logic
    score = 0
    top = info["top_app_installs"]
    n_results = info["search_results"]

    # Market exists?
    if n_results >= 10:
        score += 4
        info["justification"].append("Strong market presence: %d+ apps found" % n_results)
    elif n_results >= 5:
        score += 2
        info["justification"].append("Moderate market: %d apps found" % n_results)
    else:
        score += 1
        info["justification"].append("Thin market: only %d apps found" % n_results)

    # Install volume = demand proof
    if top >= 10_000_000:
        score += 8
        info["justification"].append("Massive demand: top app has %s+ installs" % _fmt_number(top))
    elif top >= 1_000_000:
        score += 6
        info["justification"].append("Strong demand: top app has %s+ installs" % _fmt_number(top))
    elif top >= 100_000:
        score += 4
        info["justification"].append("Moderate demand: top app has %s installs" % _fmt_number(top))
    elif top >= 10_000:
        score += 2
        info["justification"].append("Low demand signal: top app has %s installs" % _fmt_number(top))
    else:
        score += 0
        info["justification"].append("Very low demand: top app under 10k installs")

    # Average installs across results
    avg = info["avg_installs"]
    if avg >= 500_000:
        score += 5
        info["justification"].append("High avg installs across market (%s)" % _fmt_number(avg))
    elif avg >= 100_000:
        score += 4
        info["justification"].append("Good avg installs (%s)" % _fmt_number(avg))
    elif avg >= 10_000:
        score += 2
        info["justification"].append("Moderate avg installs (%s)" % _fmt_number(avg))
    else:
        score += 1
        info["justification"].append("Low avg installs (%s)" % _fmt_number(avg))

    # Named competitors boost
    if info["competitor_data"]:
        big_comps = [c for c in info["competitor_data"] if c["installs"] >= 100_000]
        if big_comps:
            score += 3
            info["justification"].append(
                "Named competitors with traction: %s"
                % ", ".join(c["title"] for c in big_comps)
            )

    score = min(score, 20)
    return score, info


# ---------------------------------------------------------------------------
# Axis 2: Frustration Validation (0-20)
# ---------------------------------------------------------------------------

def validate_frustration(competitors, lang="fr", country="fr"):
    """Score frustration level from competitor reviews."""
    info = {
        "apps_analyzed": 0,
        "total_reviews": 0,
        "total_negative": 0,
        "negative_ratio": 0.0,
        "top_complaints": [],
        "price_complaints": 0,
        "per_app": [],
        "justification": [],
    }

    all_frustrations = Counter()
    price_count = 0
    total_reviews = 0
    total_negative = 0

    for comp_id in competitors:
        rev_list = safe_reviews(comp_id, lang, country, count=150)
        if not rev_list:
            continue

        info["apps_analyzed"] += 1
        negative = [r for r in rev_list if r.get("score", 5) <= 3]

        app_frustrations = Counter()
        app_price = 0
        for r in negative:
            content = r.get("content", "").lower()
            for kw in FRUSTRATION_KEYWORDS:
                if kw in content:
                    all_frustrations[kw] += 1
                    app_frustrations[kw] += 1
            for kw in PRICE_COMPLAINT_KEYWORDS:
                if kw in content:
                    price_count += 1
                    app_price += 1
                    break  # count once per review

        info["per_app"].append({
            "id": comp_id,
            "reviews_fetched": len(rev_list),
            "negative": len(negative),
            "ratio": round(len(negative) / max(len(rev_list), 1) * 100, 1),
            "top_issues": app_frustrations.most_common(5),
        })

        total_reviews += len(rev_list)
        total_negative += len(negative)

    info["total_reviews"] = total_reviews
    info["total_negative"] = total_negative
    info["negative_ratio"] = round(total_negative / max(total_reviews, 1) * 100, 1)
    info["top_complaints"] = all_frustrations.most_common(10)
    info["price_complaints"] = price_count

    # Scoring
    score = 0
    ratio = info["negative_ratio"]

    if ratio >= 40:
        score += 10
        info["justification"].append("Very high frustration: %.1f%% negative reviews" % ratio)
    elif ratio >= 30:
        score += 8
        info["justification"].append("High frustration: %.1f%% negative reviews" % ratio)
    elif ratio >= 20:
        score += 5
        info["justification"].append("Moderate frustration: %.1f%% negative reviews" % ratio)
    elif ratio >= 10:
        score += 3
        info["justification"].append("Low frustration: %.1f%% negative reviews" % ratio)
    else:
        score += 1
        info["justification"].append("Minimal frustration: %.1f%% negative" % ratio)

    # Recurring specific complaints = exploitable gap
    recurring = [kw for kw, cnt in info["top_complaints"] if cnt >= 5]
    if len(recurring) >= 5:
        score += 6
        info["justification"].append(
            "Many recurring complaints (%d themes with 5+ mentions)" % len(recurring)
        )
    elif len(recurring) >= 3:
        score += 4
        info["justification"].append(
            "%d recurring complaint themes found" % len(recurring)
        )
    elif len(recurring) >= 1:
        score += 2
        info["justification"].append("Some recurring complaints detected")
    else:
        score += 0
        info["justification"].append("No strong recurring complaint pattern")

    # Price complaints = monetization opportunity
    if price_count >= 10:
        score += 4
        info["justification"].append(
            "Strong price frustration (%d mentions) -- users willing to pay, want better value" % price_count
        )
    elif price_count >= 5:
        score += 2
        info["justification"].append("Moderate price complaints (%d)" % price_count)

    score = min(score, 20)
    return score, info


# ---------------------------------------------------------------------------
# Axis 3: Differentiation Validation (0-20)
# ---------------------------------------------------------------------------

def validate_differentiation(angle, competitors, search_results, quick=False):
    """Score differentiation of the proposed angle vs market.
    Requires manual input unless --quick is used."""
    info = {
        "proposed_angle": angle,
        "justification": [],
    }

    if not angle:
        info["justification"].append("No angle provided -- cannot assess differentiation")
        return 5, info

    if quick:
        # Auto-score: give moderate score, flag for manual review
        score = 10
        info["justification"].append("Quick mode: angle provided ('%s')" % angle)
        info["justification"].append("Auto-scored at 10/20 -- manual review recommended")
        info["justification"].append(
            "Compare against %d competitors to verify uniqueness" % len(competitors)
        )
        return score, info

    # Interactive mode
    print("\n  --- DIFFERENTIATION ASSESSMENT ---")
    print("  Proposed angle: %s" % angle)
    if competitors:
        print("  Competitors: %s" % ", ".join(competitors))
    print()

    questions = [
        (
            "Is this angle genuinely different from what exists? (1=me-too, 5=unique)",
            "uniqueness",
        ),
        (
            "Can competitors easily copy this angle? (1=trivial copy, 5=hard to replicate)",
            "defensibility",
        ),
        (
            "Does the target audience care about this difference? (1=irrelevant, 5=critical)",
            "relevance",
        ),
        (
            "Is the differentiation visible in first 30 seconds of use? (1=hidden, 5=obvious)",
            "visibility",
        ),
    ]

    total = 0
    for question, label in questions:
        val = _ask_score(question)
        total += val
        info["justification"].append("%s: %d/5" % (label.capitalize(), val))

    # Scale from 4-20 range to 0-20
    score = int(round((total / 20) * 20))
    score = max(0, min(score, 20))

    if score >= 16:
        info["justification"].append("Strong differentiation signal")
    elif score >= 10:
        info["justification"].append("Moderate differentiation -- needs sharpening")
    else:
        info["justification"].append("Weak differentiation -- risk of being a me-too")

    return score, info


# ---------------------------------------------------------------------------
# Axis 4: Monetization Validation (0-20)
# ---------------------------------------------------------------------------

def validate_monetization(price, competitors, frustration_info, quick=False):
    """Score monetization potential based on market pricing and user signals."""
    info = {
        "proposed_price": price,
        "competitor_pricing": [],
        "revenue_models": [],
        "justification": [],
    }

    # Gather competitor pricing
    free_count = 0
    paid_count = 0
    has_iap = 0
    has_ads = 0

    for comp_id in competitors:
        comp = safe_app_info(comp_id)
        if not comp:
            continue
        is_free = comp.get("free", True)
        comp_price = comp.get("price", 0)
        iap = comp.get("inAppProductPrice", "")
        ads = comp.get("containsAds", False)

        info["competitor_pricing"].append({
            "id": comp_id,
            "title": comp.get("title", comp_id),
            "free": is_free,
            "price": comp_price,
            "iap": iap,
            "ads": ads,
        })

        if is_free:
            free_count += 1
        else:
            paid_count += 1
        if iap:
            has_iap += 1
        if ads:
            has_ads += 1

    total_comps = free_count + paid_count

    # Identify revenue models in the market
    if has_iap > 0:
        info["revenue_models"].append("In-app purchases (freemium)")
    if has_ads > 0:
        info["revenue_models"].append("Ad-supported")
    if paid_count > 0:
        info["revenue_models"].append("Paid upfront")
    if has_iap > 0 and has_ads > 0:
        info["revenue_models"].append("Hybrid (ads + IAP)")

    # Scoring
    score = 0

    # Existing monetization in market = validation
    if total_comps > 0:
        paid_ratio = (paid_count + has_iap) / total_comps
        if paid_ratio >= 0.5:
            score += 6
            info["justification"].append(
                "Strong monetization signal: %.0f%% of competitors charge" % (paid_ratio * 100)
            )
        elif paid_ratio >= 0.2:
            score += 4
            info["justification"].append(
                "Moderate monetization: %.0f%% of competitors charge" % (paid_ratio * 100)
            )
        else:
            score += 2
            info["justification"].append("Weak monetization signal in market")
    else:
        score += 1
        info["justification"].append("No competitor pricing data available")

    # Price complaints from frustration = willing to pay, want value
    price_complaints = frustration_info.get("price_complaints", 0)
    if price_complaints >= 10:
        score += 5
        info["justification"].append(
            "Users complain about price (%d mentions) = willing to pay, seek better value"
            % price_complaints
        )
    elif price_complaints >= 5:
        score += 3
        info["justification"].append("Some price complaints (%d) = payment willingness exists" % price_complaints)
    elif price_complaints > 0:
        score += 1
        info["justification"].append("Few price complaints")

    # Proposed price sanity check
    if price and price > 0:
        score += 3
        info["justification"].append("Price point defined: %.2f" % price)
        if total_comps > 0 and paid_count == 0 and has_iap == 0:
            info["justification"].append(
                "WARNING: market is mostly free -- paid model may face resistance"
            )
    else:
        score += 1
        info["justification"].append("No price point defined yet")

    # Interactive questions for deeper assessment
    if not quick:
        print("\n  --- MONETIZATION ASSESSMENT ---")
        q1 = _ask_score(
            "How clear is the value proposition for paying? (1=unclear, 5=obvious ROI)"
        )
        q2 = _ask_score(
            "How established is paid behavior in this category? (1=everything free, 5=users expect to pay)"
        )
        combined = q1 + q2
        bonus = int(round((combined / 10) * 6))
        score += bonus
        info["justification"].append("Value clarity: %d/5, Payment culture: %d/5" % (q1, q2))
    else:
        score += 3  # default mid-range for quick mode
        info["justification"].append("Quick mode: monetization details skipped")

    score = min(score, 20)
    return score, info


# ---------------------------------------------------------------------------
# Axis 5: Execution Validation (0-20)
# ---------------------------------------------------------------------------

def validate_execution(idea_name, angle, quick=False):
    """Score execution feasibility: MVP complexity, time to market, tech risk."""
    info = {
        "justification": [],
    }

    if quick:
        score = 10
        info["justification"].append("Quick mode: execution scored at 10/20 by default")
        info["justification"].append("Manual assessment recommended for accurate scoring")
        return score, info

    print("\n  --- EXECUTION ASSESSMENT ---")
    print("  Idea: %s" % idea_name)
    if angle:
        print("  Angle: %s" % angle)
    print()

    questions = [
        ("MVP core feature count estimate? (1=10+ features, 5=1-2 features)", "mvp_simplicity"),
        ("Time to functional MVP? (1=6+ months, 5=under 2 weeks)", "time_to_market"),
        ("Technical complexity? (1=AI/ML/hardware needed, 5=standard CRUD)", "tech_simplicity"),
        ("Do you have the skills to build this? (1=need to learn everything, 5=expert)", "skill_fit"),
        ("Regulatory or legal risk? (1=heavy regulation, 5=no constraints)", "regulatory_risk"),
    ]

    total = 0
    for question, label in questions:
        val = _ask_score(question)
        total += val
        info["justification"].append("%s: %d/5" % (label.replace("_", " ").capitalize(), val))

    # Scale from 5-25 range to 0-20
    score = int(round(((total - 5) / 20) * 20))
    score = max(0, min(score, 20))

    if score >= 16:
        info["justification"].append("Low execution risk -- fast path to MVP")
    elif score >= 10:
        info["justification"].append("Moderate execution complexity")
    else:
        info["justification"].append("High execution risk -- consider simplifying scope")

    return score, info


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def generate_report(idea_name, scores, infos, data_sources):
    """Print the full validation report."""
    total = sum(scores.values())

    # Determine confidence level
    confidence_label = "UNKNOWN"
    for threshold, label in CONFIDENCE_LEVELS:
        if total >= threshold:
            confidence_label = label
            break

    print("\n")
    print("=" * 70)
    print("  MOAT CROSS-VALIDATION REPORT")
    print("  %s" % idea_name)
    print("  Generated: %s" % datetime.now().strftime("%Y-%m-%d %H:%M"))
    print("=" * 70)

    # Per-axis results
    axes = [
        ("1. DEMAND", "demand"),
        ("2. FRUSTRATION", "frustration"),
        ("3. DIFFERENTIATION", "differentiation"),
        ("4. MONETIZATION", "monetization"),
        ("5. EXECUTION", "execution"),
    ]

    for label, key in axes:
        s = scores[key]
        bar = _make_bar(s, 20)
        print("\n  %s: %d/20  %s" % (label, s, bar))
        for j in infos[key].get("justification", []):
            print("    - %s" % j)

    # Overall score
    print("\n" + "-" * 70)
    bar = _make_bar(total, 100)
    print("\n  OVERALL SCORE: %d / 100  %s" % (total, bar))
    print("  CONFIDENCE: %s" % confidence_label)

    # Key risks
    print("\n  KEY RISKS:")
    risks = _identify_risks(scores, infos)
    if risks:
        for risk in risks:
            print("    [!] %s" % risk)
    else:
        print("    None identified -- all axes strong")

    # Recommended next steps
    print("\n  RECOMMENDED NEXT STEPS:")
    steps = _recommend_steps(scores, infos)
    for i, step in enumerate(steps, 1):
        print("    %d. %s" % (i, step))

    # Data sources
    print("\n  DATA SOURCES:")
    for src in data_sources:
        print("    - %s" % src)

    print("\n" + "=" * 70)

    return {
        "idea": idea_name,
        "scores": scores,
        "total": total,
        "confidence": confidence_label,
        "risks": risks,
        "next_steps": steps,
        "timestamp": datetime.now().isoformat(),
    }


def _identify_risks(scores, infos):
    """Identify key risks from low-scoring axes."""
    risks = []
    if scores["demand"] < 8:
        risks.append("Demand unproven -- market may be too niche or nascent")
    if scores["frustration"] < 8:
        risks.append("Low frustration signal -- users may be satisfied with current solutions")
    if scores["differentiation"] < 8:
        risks.append("Weak differentiation -- risk of being perceived as a me-too")
    if scores["monetization"] < 8:
        risks.append("Monetization unclear -- revenue model needs validation")
    if scores["execution"] < 8:
        risks.append("High execution complexity -- scope may need reduction")

    # Check for specific warning patterns
    for j in infos.get("monetization", {}).get("justification", []):
        if "WARNING" in j:
            risks.append(j.replace("WARNING: ", ""))

    return risks


def _recommend_steps(scores, infos):
    """Generate recommended next validation steps."""
    steps = []

    if scores["demand"] < 12:
        steps.append("Run deeper keyword research (Google Trends, keyword tools)")
    if scores["frustration"] < 12:
        steps.append("Manually read 50+ competitor reviews to find specific pain points")
    if scores["differentiation"] < 12:
        steps.append("Sharpen your unique angle -- interview 5 potential users")
    if scores["monetization"] < 12:
        steps.append("Survey target users on willingness to pay and price sensitivity")
    if scores["execution"] < 12:
        steps.append("Prototype the core feature in a weekend to validate feasibility")

    # General next steps based on overall score
    total = sum(scores.values())
    if total >= 80:
        steps.append("Strong validation -- proceed to MVP build")
    elif total >= 60:
        steps.append("Create a landing page to test conversion before building")
    elif total >= 40:
        steps.append("Conduct 10 user interviews before investing development time")
    else:
        steps.append("Consider pivoting to a higher-signal opportunity")

    return steps


# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------

def _fmt_number(n):
    """Format a number with K/M suffix."""
    if n >= 1_000_000:
        return "%.1fM" % (n / 1_000_000)
    if n >= 1_000:
        return "%.0fK" % (n / 1_000)
    return str(n)


def _make_bar(value, maximum, width=20):
    """Create an ASCII progress bar."""
    filled = int(round(value / max(maximum, 1) * width))
    filled = min(filled, width)
    return "[%s%s]" % ("#" * filled, "." * (width - filled))


def _ask_score(question):
    """Ask the user for a 1-5 score interactively."""
    while True:
        try:
            val = int(input("  %s\n  > " % question))
            if 1 <= val <= 5:
                return val
            print("  Please enter a number between 1 and 5.")
        except ValueError:
            print("  Please enter a number between 1 and 5.")
        except (EOFError, KeyboardInterrupt):
            print("\n  Defaulting to 3.")
            return 3


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="MOAT Cross-Validator -- Multi-source app idea validation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            '  python cross_validator.py "SleepCoach FR" --query "sleep insomnia CBT" \\\n'
            '      --competitors "com.northcube.sleepcycle,com.calm.android" \\\n'
            '      --angle "CBT-I therapy vs tracking" --price 6.99\n'
            "\n"
            '  python cross_validator.py "CoachCRM" --query "coach fitness management" \\\n'
            '      --angle "CRM vs exercise tracker" --price 9.99 --quick\n'
        ),
    )
    parser.add_argument("idea", help="Name of the app idea to validate")
    parser.add_argument("--query", "-q", required=True, help="Search query for Play Store")
    parser.add_argument(
        "--competitors", "-c", default="",
        help="Comma-separated competitor app IDs (e.g., com.calm.android,com.headspace.android)"
    )
    parser.add_argument("--angle", "-a", default="", help="Proposed differentiation angle")
    parser.add_argument("--price", "-p", type=float, default=0, help="Proposed price point (e.g., 6.99)")
    parser.add_argument("--lang", default="fr", help="Language for Play Store queries (default: fr)")
    parser.add_argument("--country", default="fr", help="Country for Play Store queries (default: fr)")
    parser.add_argument("--quick", action="store_true", help="Skip interactive questions, use defaults")
    parser.add_argument("--save", action="store_true", help="Save report as JSON")

    args = parser.parse_args()

    if not HAS_SCRAPER:
        print("ERROR: google-play-scraper is required.")
        print("Install it with: pip install google-play-scraper")
        sys.exit(1)

    competitors = [c.strip() for c in args.competitors.split(",") if c.strip()]
    data_sources = ["Google Play Store (search + app metadata + reviews)"]
    if competitors:
        data_sources.append("Competitor analysis: %s" % ", ".join(competitors))
    if not args.quick:
        data_sources.append("Manual expert assessment (interactive)")

    print("\n" + "=" * 70)
    print("  MOAT Cross-Validator")
    print("  Validating: %s" % args.idea)
    print("  Query: %s" % args.query)
    if competitors:
        print("  Competitors: %s" % ", ".join(competitors))
    if args.angle:
        print("  Angle: %s" % args.angle)
    if args.price:
        print("  Price: %.2f" % args.price)
    print("  Mode: %s" % ("QUICK (automated)" if args.quick else "FULL (interactive)"))
    print("=" * 70)

    scores = {}
    infos = {}

    # --- Axis 1: Demand ---
    print("\n  [1/5] Analyzing DEMAND...")
    scores["demand"], infos["demand"] = validate_demand(
        args.query, competitors, args.lang, args.country
    )
    print("  -> Demand score: %d/20" % scores["demand"])

    # --- Axis 2: Frustration ---
    print("\n  [2/5] Analyzing FRUSTRATION...")
    if competitors:
        scores["frustration"], infos["frustration"] = validate_frustration(
            competitors, args.lang, args.country
        )
    else:
        # Try to use top search results as proxies
        print("  No competitors specified -- using top search results as proxies...")
        results = safe_search(args.query, args.lang, args.country, n_hits=5)
        proxy_ids = [r.get("appId", "") for r in results[:3] if r.get("appId")]
        if proxy_ids:
            scores["frustration"], infos["frustration"] = validate_frustration(
                proxy_ids, args.lang, args.country
            )
        else:
            scores["frustration"] = 5
            infos["frustration"] = {
                "justification": ["No competitor data available -- default score applied"]
            }
    print("  -> Frustration score: %d/20" % scores["frustration"])

    # --- Axis 3: Differentiation ---
    print("\n  [3/5] Assessing DIFFERENTIATION...")
    search_results = safe_search(args.query, args.lang, args.country, n_hits=10)
    scores["differentiation"], infos["differentiation"] = validate_differentiation(
        args.angle, competitors, search_results, quick=args.quick
    )
    print("  -> Differentiation score: %d/20" % scores["differentiation"])

    # --- Axis 4: Monetization ---
    print("\n  [4/5] Analyzing MONETIZATION...")
    scores["monetization"], infos["monetization"] = validate_monetization(
        args.price, competitors, infos.get("frustration", {}), quick=args.quick
    )
    print("  -> Monetization score: %d/20" % scores["monetization"])

    # --- Axis 5: Execution ---
    print("\n  [5/5] Assessing EXECUTION...")
    scores["execution"], infos["execution"] = validate_execution(
        args.idea, args.angle, quick=args.quick
    )
    print("  -> Execution score: %d/20" % scores["execution"])

    # --- Generate report ---
    report = generate_report(args.idea, scores, infos, data_sources)

    # Save if requested
    if args.save:
        output_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "data", "validations"
        )
        os.makedirs(output_dir, exist_ok=True)
        slug = args.idea.lower().replace(" ", "_")
        filename = "validation_%s_%s.json" % (slug, datetime.now().strftime("%Y%m%d_%H%M"))
        filepath = os.path.join(output_dir, filename)

        # Add detailed info to saved report
        report["details"] = {}
        for key in infos:
            detail = dict(infos[key])
            # Convert Counter objects for JSON serialization
            for k, v in detail.items():
                if isinstance(v, list):
                    detail[k] = [
                        (list(item) if isinstance(item, tuple) else item)
                        for item in v
                    ]
            report["details"][key] = detail

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2, default=str)

        print("\n  Report saved: %s" % filepath)


if __name__ == "__main__":
    main()
