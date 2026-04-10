#!/usr/bin/env python3
"""
MOAT App Discovery System - Niche Hunter (Core Intelligence Engine)

Automated niche discovery that scans Google Play to find app opportunities.
Combines market scanning, review analysis, gap extraction, and opportunity
scoring into a single actionable report.

Usage:
    python niche_hunter.py "meditation sommeil" --lang fr --top 15
    python niche_hunter.py "invoice freelance" --lang fr --report
    python niche_hunter.py "coach fitness CRM" --lang en --country us
    python niche_hunter.py "pomodoro timer" --lang fr --arpu 4.99 --segment 500000

Author: MOAT System
"""

import argparse
import json
import os
import re
import sys
import time
from collections import Counter
from datetime import datetime

try:
    from google_play_scraper import app, reviews, search, Sort
    HAS_SCRAPER = True
except ImportError:
    HAS_SCRAPER = False


# ---------------------------------------------------------------------------
# FRUSTRATION KEYWORD DICTIONARIES (French + English)
# ---------------------------------------------------------------------------

FRUSTRATION_KEYWORDS = {
    "pricing": {
        "fr": [
            "payant", "cher", "chere", "abonnement", "premium", "arnaque",
            "trop cher", "gratuit", "freemium", "prix", "cout", "payer",
            "desinstalle", "rembourse", "remboursement", "vol", "escroc",
            "hors de prix", "ruineux",
        ],
        "en": [
            "expensive", "subscription", "paywall", "overpriced", "costly",
            "rip off", "ripoff", "scam", "money grab", "not worth",
            "pay to win", "in-app purchase", "too much", "free version",
            "premium only", "price", "pricing", "charge", "charged",
        ],
    },
    "quality": {
        "fr": [
            "bug", "crash", "plante", "lent", "lente", "erreur", "freeze",
            "gele", "rame", "lag", "bloque", "ferme tout seul", "instable",
            "ne repond pas", "batterie", "chauffe", "memoire", "lourd",
            "plantage", "defaillance",
        ],
        "en": [
            "bug", "crash", "slow", "glitch", "broken", "freeze", "lag",
            "laggy", "hang", "error", "force close", "unstable", "battery",
            "drain", "memory", "heavy", "unresponsive", "loading",
            "stuck", "fails",
        ],
    },
    "ux": {
        "fr": [
            "complique", "confus", "difficile", "interface", "ergonomie",
            "incomprehensible", "pas intuitif", "mal concu", "navigation",
            "design", "moche", "illisible", "mal foutu", "galere",
            "impossible a utiliser", "usine a gaz",
        ],
        "en": [
            "complicated", "confusing", "unintuitive", "hard to use",
            "cluttered", "ugly", "bad design", "poor ux", "not intuitive",
            "user unfriendly", "messy", "overwhelming", "clunky",
            "counterintuitive", "terrible ui",
        ],
    },
    "missing": {
        "fr": [
            "manque", "impossible", "pas de", "il manque", "absent",
            "ne permet pas", "fonctionnalite", "option manquante",
            "devrait avoir", "dommage", "pourquoi pas", "limite",
            "limité", "basique", "insuffisant",
        ],
        "en": [
            "missing", "no option", "wish", "need", "lacking", "limited",
            "basic", "incomplete", "doesn't have", "should have",
            "would be nice", "feature request", "not available",
            "can't even", "why can't",
        ],
    },
    "ads": {
        "fr": [
            "pub", "publicite", "publicites", "intrusif", "envahissant",
            "plein de pubs", "trop de pub", "pub a chaque", "spam",
            "notification", "notifications", "harcelement",
        ],
        "en": [
            "ads", "advertisement", "intrusive", "ad-filled", "popup",
            "pop-up", "spam", "notification", "notifications", "banner",
            "full screen ad", "too many ads", "ad every",
        ],
    },
}

# ---------------------------------------------------------------------------
# GAP DETECTION PATTERNS (what users WANT but don't have)
# ---------------------------------------------------------------------------

GAP_PATTERNS_FR = [
    r"j'aimerais\s+(.{10,80})",
    r"il manque\s+(.{10,80})",
    r"pourquoi pas\s+(.{10,80})",
    r"si seulement\s+(.{10,80})",
    r"dommage qu[e']\s*(.{10,80})",
    r"il faudrait\s+(.{10,80})",
    r"ca serait bien\s+(.{10,80})",
    r"devrait permettre\s+(.{10,80})",
    r"on ne peut pas\s+(.{10,80})",
    r"je voudrais\s+(.{10,80})",
    r"ajouter\s+(.{10,60})",
    r"besoin de\s+(.{10,60})",
]

GAP_PATTERNS_EN = [
    r"i wish\s+(.{10,80})",
    r"it would be great if\s+(.{10,80})",
    r"missing feature[s]?\s*[:\-]?\s*(.{5,80})",
    r"needs?\s+(.{10,80})",
    r"should have\s+(.{10,80})",
    r"why (can't|doesn't|isn't)\s+(.{10,80})",
    r"would love\s+(.{10,80})",
    r"please add\s+(.{10,80})",
    r"if only\s+(.{10,80})",
    r"no way to\s+(.{10,80})",
    r"can't even\s+(.{10,80})",
    r"looking for\s+(.{10,60})",
]


# ---------------------------------------------------------------------------
# DISPLAY HELPERS (ASCII-safe, no unicode)
# ---------------------------------------------------------------------------

SEPARATOR = "=" * 72
SEPARATOR_THIN = "-" * 72


def bar_chart(value, max_value, width=30, fill="#", empty="."):
    """Render a simple ASCII bar chart."""
    if max_value == 0:
        ratio = 0
    else:
        ratio = min(value / max_value, 1.0)
    filled = int(ratio * width)
    return "[" + fill * filled + empty * (width - filled) + "]"


def format_number(n):
    """Format large numbers with K/M suffixes."""
    if n is None:
        return "N/A"
    if n >= 1_000_000_000:
        return "%.1fB" % (n / 1_000_000_000)
    if n >= 1_000_000:
        return "%.1fM" % (n / 1_000_000)
    if n >= 1_000:
        return "%.1fK" % (n / 1_000)
    return str(n)


def safe_str(text):
    """Ensure string is safe for cp1252 / ASCII output on Windows."""
    if text is None:
        return ""
    # Replace common unicode chars with ASCII equivalents
    replacements = {
        "\u2019": "'", "\u2018": "'",
        "\u201c": '"', "\u201d": '"',
        "\u2013": "-", "\u2014": "--",
        "\u2026": "...", "\u00e9": "e",
        "\u00e8": "e", "\u00ea": "e",
        "\u00e0": "a", "\u00e2": "a",
        "\u00ee": "i", "\u00ef": "i",
        "\u00f4": "o", "\u00fb": "u",
        "\u00fc": "u", "\u00e7": "c",
        "\u2605": "*", "\u2606": ".",
        "\u25cf": "*", "\u25cb": "o",
        "\u2588": "#", "\u2591": ".",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    # Strip any remaining non-ASCII
    return text.encode("ascii", errors="replace").decode("ascii")


# ---------------------------------------------------------------------------
# NICHE HUNTER CLASS
# ---------------------------------------------------------------------------

class NicheHunter:
    """Core intelligence engine for MOAT App Discovery System."""

    def __init__(self, lang="fr", country="fr"):
        """
        Initialize the NicheHunter.

        Args:
            lang: Language for Play Store queries (fr, en, es, de, etc.)
            country: Country code for Play Store queries (fr, us, uk, etc.)
        """
        self.lang = lang
        self.country = country
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

        if not HAS_SCRAPER:
            print("[!] google-play-scraper not installed.")
            print("    Install with: pip install google-play-scraper")
            print("    The script will run but return empty results.")

    # ------------------------------------------------------------------
    # 1. MARKET SCANNING
    # ------------------------------------------------------------------

    def scan_market(self, query, top=15):
        """
        Search Google Play for apps matching a query and build a market overview.

        Args:
            query: Search keywords (e.g. "meditation sommeil")
            top: Number of top results to analyze

        Returns:
            dict with keys: query, apps, stats, weakest_competitors
        """
        print("\n" + SEPARATOR)
        print("  MARKET SCAN: %s" % query)
        print("  Lang: %s | Country: %s | Top: %d" % (self.lang, self.country, top))
        print(SEPARATOR)

        if not HAS_SCRAPER:
            return self._empty_market(query)

        # Search Play Store
        try:
            results = search(query, lang=self.lang, country=self.country, n_hits=top)
        except Exception as e:
            print("[ERROR] Search failed: %s" % str(e))
            return self._empty_market(query)

        if not results:
            print("[!] No results found for '%s'" % query)
            return self._empty_market(query)

        # Collect detailed app info
        apps_data = []
        for i, r in enumerate(results[:top]):
            app_id = r.get("appId", "")
            try:
                detail = app(app_id, lang=self.lang, country=self.country)
                app_info = {
                    "appId": app_id,
                    "title": safe_str(detail.get("title", "Unknown")),
                    "score": detail.get("score") or 0,
                    "ratings": detail.get("ratings") or 0,
                    "reviews": detail.get("reviews") or 0,
                    "installs": detail.get("realInstalls") or detail.get("minInstalls") or 0,
                    "free": detail.get("free", True),
                    "price": detail.get("price") or 0,
                    "developer": safe_str(detail.get("developer", "")),
                    "genre": safe_str(detail.get("genre", "")),
                    "contentRating": detail.get("contentRating", ""),
                    "lastUpdated": str(detail.get("updated", "")),
                    "size": detail.get("size", ""),
                }
                apps_data.append(app_info)

                # Progress display
                status = "  [%d/%d] %-40s  %.1f*  %s installs" % (
                    i + 1, len(results[:top]),
                    app_info["title"][:40],
                    app_info["score"],
                    format_number(app_info["installs"]),
                )
                print(status)

                # Rate limit courtesy
                time.sleep(0.3)

            except Exception as e:
                print("  [%d/%d] SKIP %s (%s)" % (i + 1, top, app_id, str(e)))
                continue

        # Calculate market stats
        stats = self._calculate_market_stats(apps_data)

        # Identify weakest competitors
        weakest = sorted(
            [a for a in apps_data if a["score"] > 0],
            key=lambda x: x["score"]
        )[:5]

        # Display summary
        self._display_market_summary(stats, weakest)

        return {
            "query": query,
            "timestamp": self.timestamp,
            "lang": self.lang,
            "country": self.country,
            "apps": apps_data,
            "stats": stats,
            "weakest_competitors": weakest,
        }

    def _calculate_market_stats(self, apps):
        """Compute market-level statistics from a list of apps."""
        if not apps:
            return {
                "count": 0, "avg_score": 0, "median_score": 0,
                "pct_below_4": 0, "total_installs": 0,
                "avg_installs": 0, "max_installs": 0,
                "free_pct": 0, "saturation": "unknown",
            }

        scores = [a["score"] for a in apps if a["score"] > 0]
        installs = [a["installs"] for a in apps]
        free_count = sum(1 for a in apps if a["free"])

        avg_score = sum(scores) / len(scores) if scores else 0
        sorted_scores = sorted(scores)
        median_score = sorted_scores[len(sorted_scores) // 2] if sorted_scores else 0
        below_4 = sum(1 for s in scores if s < 4.0)
        pct_below_4 = (below_4 / len(scores) * 100) if scores else 0

        total_installs = sum(installs)
        avg_installs = total_installs // len(apps) if apps else 0
        max_installs = max(installs) if installs else 0

        # Saturation level
        if avg_score >= 4.5 and pct_below_4 < 10:
            saturation = "HIGH (tough market, high quality)"
        elif avg_score >= 4.0 and pct_below_4 < 30:
            saturation = "MEDIUM (competitive but with gaps)"
        elif avg_score >= 3.5:
            saturation = "LOW-MEDIUM (room for a better product)"
        else:
            saturation = "LOW (weak competition, big opportunity)"

        return {
            "count": len(apps),
            "avg_score": round(avg_score, 2),
            "median_score": round(median_score, 2),
            "pct_below_4": round(pct_below_4, 1),
            "total_installs": total_installs,
            "avg_installs": avg_installs,
            "max_installs": max_installs,
            "free_pct": round(free_count / len(apps) * 100, 1) if apps else 0,
            "saturation": saturation,
        }

    def _display_market_summary(self, stats, weakest):
        """Print a formatted market summary to stdout."""
        print("\n" + SEPARATOR_THIN)
        print("  MARKET OVERVIEW")
        print(SEPARATOR_THIN)
        print("  Apps analyzed      : %d" % stats["count"])
        print("  Average score      : %.2f / 5.0  %s" % (
            stats["avg_score"],
            bar_chart(stats["avg_score"], 5.0, width=20),
        ))
        print("  Median score       : %.2f / 5.0" % stats["median_score"])
        print("  %% below 4.0 stars : %.1f%%  %s" % (
            stats["pct_below_4"],
            bar_chart(stats["pct_below_4"], 100, width=20),
        ))
        print("  Total installs     : %s" % format_number(stats["total_installs"]))
        print("  Avg installs/app   : %s" % format_number(stats["avg_installs"]))
        print("  Largest player     : %s installs" % format_number(stats["max_installs"]))
        print("  Free apps          : %.1f%%" % stats["free_pct"])
        print("  Saturation         : %s" % stats["saturation"])

        if weakest:
            print("\n  WEAKEST COMPETITORS (easiest to beat):")
            for i, w in enumerate(weakest, 1):
                print("    %d. %-35s  %.1f*  %s installs" % (
                    i, w["title"][:35], w["score"],
                    format_number(w["installs"]),
                ))

    def _empty_market(self, query):
        """Return an empty market data structure."""
        return {
            "query": query, "timestamp": self.timestamp,
            "lang": self.lang, "country": self.country,
            "apps": [], "stats": self._calculate_market_stats([]),
            "weakest_competitors": [],
        }

    # ------------------------------------------------------------------
    # 2. COMPETITOR REVIEW ANALYSIS
    # ------------------------------------------------------------------

    def analyze_competitors(self, app_ids, review_count=200):
        """
        Fetch and analyze reviews from competitor apps.

        Args:
            app_ids: List of app IDs to analyze
            review_count: Number of reviews to fetch per app

        Returns:
            dict with frustration_analysis, sentiment, pain_points, raw_reviews
        """
        print("\n" + SEPARATOR_THIN)
        print("  REVIEW ANALYSIS (%d apps, %d reviews each)" % (
            len(app_ids), review_count))
        print(SEPARATOR_THIN)

        if not HAS_SCRAPER:
            return self._empty_review_analysis()

        all_reviews = []
        per_app_data = {}

        for app_id in app_ids:
            try:
                print("  Fetching reviews for: %s ..." % app_id)
                result, _ = reviews(
                    app_id,
                    lang=self.lang,
                    country=self.country,
                    sort=Sort.NEWEST,
                    count=review_count,
                )

                app_reviews = []
                for r in result:
                    review_text = safe_str(r.get("content", ""))
                    score = r.get("score", 0)
                    app_reviews.append({
                        "text": review_text,
                        "score": score,
                        "appId": app_id,
                        "thumbsUp": r.get("thumbsUpCount", 0),
                    })

                all_reviews.extend(app_reviews)
                per_app_data[app_id] = app_reviews
                print("    -> Got %d reviews (avg score: %.1f)" % (
                    len(app_reviews),
                    sum(r["score"] for r in app_reviews) / max(len(app_reviews), 1),
                ))

                time.sleep(0.5)

            except Exception as e:
                print("    [ERROR] %s: %s" % (app_id, str(e)))
                per_app_data[app_id] = []

        if not all_reviews:
            print("  [!] No reviews collected.")
            return self._empty_review_analysis()

        # Frustration analysis
        frustrations = self._analyze_frustrations(all_reviews)

        # Sentiment ratio
        sentiment = self._calculate_sentiment(all_reviews)

        # Top pain points
        pain_points = self._extract_pain_points(all_reviews)

        # Gap extraction
        gaps = self.extract_gaps(all_reviews)

        # Display
        self._display_review_analysis(frustrations, sentiment, pain_points, gaps)

        return {
            "total_reviews": len(all_reviews),
            "apps_analyzed": len(app_ids),
            "frustrations": frustrations,
            "sentiment": sentiment,
            "pain_points": pain_points,
            "gaps": gaps,
            "per_app": {
                aid: {
                    "count": len(revs),
                    "avg_score": round(
                        sum(r["score"] for r in revs) / max(len(revs), 1), 2
                    ),
                }
                for aid, revs in per_app_data.items()
            },
        }

    def _analyze_frustrations(self, reviews_list):
        """Count frustration keyword hits across all categories."""
        category_counts = {}
        keyword_details = {}

        for category, langs in FRUSTRATION_KEYWORDS.items():
            total = 0
            details = Counter()

            # Combine keywords for both languages
            all_kw = langs.get("fr", []) + langs.get("en", [])

            for rev in reviews_list:
                text = rev["text"].lower()
                for kw in all_kw:
                    if kw in text:
                        details[kw] += 1
                        total += 1

            category_counts[category] = total
            keyword_details[category] = dict(details.most_common(10))

        return {
            "by_category": category_counts,
            "top_keywords": keyword_details,
            "total_frustration_mentions": sum(category_counts.values()),
        }

    def _calculate_sentiment(self, reviews_list):
        """Calculate sentiment distribution from review scores."""
        if not reviews_list:
            return {"positive": 0, "neutral": 0, "negative": 0, "ratio": 0}

        positive = sum(1 for r in reviews_list if r["score"] >= 4)
        neutral = sum(1 for r in reviews_list if r["score"] == 3)
        negative = sum(1 for r in reviews_list if r["score"] <= 2)
        total = len(reviews_list)

        return {
            "positive": positive,
            "positive_pct": round(positive / total * 100, 1),
            "neutral": neutral,
            "neutral_pct": round(neutral / total * 100, 1),
            "negative": negative,
            "negative_pct": round(negative / total * 100, 1),
            "ratio": round(negative / max(positive, 1), 2),
            "total": total,
        }

    def _extract_pain_points(self, reviews_list, top_n=5):
        """
        Extract top recurring pain points with example quotes.

        Groups negative reviews by frustration category and picks the
        most upvoted/representative quotes.
        """
        # Only analyze negative reviews (1-2 stars)
        negative = [r for r in reviews_list if r["score"] <= 2]
        if not negative:
            negative = [r for r in reviews_list if r["score"] <= 3]

        pain_points = []

        for category, langs in FRUSTRATION_KEYWORDS.items():
            all_kw = langs.get("fr", []) + langs.get("en", [])
            matching_reviews = []

            for rev in negative:
                text = rev["text"].lower()
                matched_kw = [kw for kw in all_kw if kw in text]
                if matched_kw:
                    matching_reviews.append({
                        "text": rev["text"],
                        "score": rev["score"],
                        "thumbsUp": rev["thumbsUp"],
                        "matched": matched_kw,
                    })

            if matching_reviews:
                # Sort by thumbsUp (most agreed-upon complaints)
                matching_reviews.sort(key=lambda x: x["thumbsUp"], reverse=True)

                # Pick best example quote (truncated)
                best_quote = matching_reviews[0]["text"][:200]
                if len(matching_reviews[0]["text"]) > 200:
                    best_quote += "..."

                pain_points.append({
                    "category": category,
                    "mention_count": len(matching_reviews),
                    "example_quote": safe_str(best_quote),
                    "top_keywords": [
                        kw for kw, _ in Counter(
                            kw for r in matching_reviews
                            for kw in r["matched"]
                        ).most_common(5)
                    ],
                })

        # Sort by frequency
        pain_points.sort(key=lambda x: x["mention_count"], reverse=True)
        return pain_points[:top_n]

    def _display_review_analysis(self, frustrations, sentiment, pain_points, gaps):
        """Print formatted review analysis."""
        print("\n  SENTIMENT DISTRIBUTION:")
        total = sentiment.get("total", 1)
        print("    Positive (4-5*) : %3d (%5.1f%%)  %s" % (
            sentiment["positive"], sentiment["positive_pct"],
            bar_chart(sentiment["positive"], total),
        ))
        print("    Neutral  (3*)   : %3d (%5.1f%%)  %s" % (
            sentiment["neutral"], sentiment["neutral_pct"],
            bar_chart(sentiment["neutral"], total),
        ))
        print("    Negative (1-2*) : %3d (%5.1f%%)  %s" % (
            sentiment["negative"], sentiment["negative_pct"],
            bar_chart(sentiment["negative"], total),
        ))
        print("    Neg/Pos ratio   : %.2f" % sentiment["ratio"])

        print("\n  FRUSTRATION BY CATEGORY:")
        max_cat = max(frustrations["by_category"].values()) if frustrations["by_category"] else 1
        for cat, count in sorted(
            frustrations["by_category"].items(), key=lambda x: x[1], reverse=True
        ):
            print("    %-12s : %4d  %s" % (
                cat.upper(), count, bar_chart(count, max_cat, width=25),
            ))

        if pain_points:
            print("\n  TOP PAIN POINTS:")
            for i, pp in enumerate(pain_points, 1):
                print("    %d. [%s] %d mentions" % (
                    i, pp["category"].upper(), pp["mention_count"],
                ))
                print("       Keywords: %s" % ", ".join(pp["top_keywords"]))
                print('       Quote: "%s"' % pp["example_quote"][:120])

        if gaps:
            print("\n  USER WISHES (gap signals):")
            for i, gap in enumerate(gaps[:8], 1):
                print('    %d. "%s"' % (i, safe_str(gap)[:100]))

    def _empty_review_analysis(self):
        """Return empty review analysis structure."""
        return {
            "total_reviews": 0, "apps_analyzed": 0,
            "frustrations": {"by_category": {}, "top_keywords": {}, "total_frustration_mentions": 0},
            "sentiment": {"positive": 0, "neutral": 0, "negative": 0, "ratio": 0, "total": 0},
            "pain_points": [], "gaps": [], "per_app": {},
        }

    # ------------------------------------------------------------------
    # 3. GAP EXTRACTION
    # ------------------------------------------------------------------

    def extract_gaps(self, reviews_list):
        """
        Find what users explicitly want but don't have.

        Scans reviews for wish/request patterns in French and English.

        Args:
            reviews_list: List of review dicts with 'text' key

        Returns:
            List of extracted gap strings, deduplicated and ranked
        """
        gaps = []
        patterns = GAP_PATTERNS_FR + GAP_PATTERNS_EN

        for rev in reviews_list:
            text = rev.get("text", "") if isinstance(rev, dict) else str(rev)
            text_lower = text.lower()

            for pattern in patterns:
                matches = re.findall(pattern, text_lower, re.IGNORECASE)
                for match in matches:
                    # Handle tuple results from groups
                    if isinstance(match, tuple):
                        match = match[-1]
                    cleaned = match.strip().rstrip(".!?,;:")
                    if len(cleaned) > 10:
                        gaps.append(cleaned)

        # Deduplicate by similarity (simple approach: normalize and count)
        gap_counter = Counter()
        normalized_gaps = {}
        for gap in gaps:
            # Simple normalization: lowercase, strip extra spaces
            key = re.sub(r"\s+", " ", gap.lower().strip())
            gap_counter[key] += 1
            if key not in normalized_gaps:
                normalized_gaps[key] = gap

        # Return ranked by frequency
        ranked = [
            normalized_gaps[key]
            for key, _ in gap_counter.most_common(20)
        ]
        return ranked

    # ------------------------------------------------------------------
    # 4. OPPORTUNITY SCORING
    # ------------------------------------------------------------------

    def calculate_opportunity_score(self, market_data, review_data):
        """
        Calculate a 0-100 opportunity score combining multiple signals.

        Components:
        - market_gap (0-30): How weak is the current competition?
        - frustration_level (0-25): How frustrated are current users?
        - market_size (0-25): How big is the market?
        - trend_signal (0-20): Growth signals

        Args:
            market_data: Output from scan_market()
            review_data: Output from analyze_competitors()

        Returns:
            dict with total score and component breakdown
        """
        stats = market_data.get("stats", {})
        sentiment = review_data.get("sentiment", {})
        frustrations = review_data.get("frustrations", {})

        # --- Market Gap Score (0-30) ---
        # Higher score = weaker competition
        avg_score = stats.get("avg_score", 4.5)
        pct_below_4 = stats.get("pct_below_4", 0)

        # Below 4.0 avg = great opportunity
        if avg_score < 3.5:
            gap_score = 30
        elif avg_score < 4.0:
            gap_score = 25
        elif avg_score < 4.2:
            gap_score = 18
        elif avg_score < 4.5:
            gap_score = 10
        else:
            gap_score = 5

        # Bonus for high % of weak apps
        gap_score = min(30, gap_score + pct_below_4 * 0.1)

        # --- Frustration Level (0-25) ---
        neg_pct = sentiment.get("negative_pct", 0)
        total_mentions = frustrations.get("total_frustration_mentions", 0)
        total_reviews = review_data.get("total_reviews", 1)

        frustration_density = total_mentions / max(total_reviews, 1)

        if neg_pct > 40:
            frust_score = 25
        elif neg_pct > 30:
            frust_score = 20
        elif neg_pct > 20:
            frust_score = 15
        elif neg_pct > 10:
            frust_score = 10
        else:
            frust_score = 5

        # Bonus for high frustration density
        frust_score = min(25, frust_score + frustration_density * 3)

        # --- Market Size (0-25) ---
        total_installs = stats.get("total_installs", 0)

        if total_installs > 50_000_000:
            size_score = 25
        elif total_installs > 10_000_000:
            size_score = 20
        elif total_installs > 1_000_000:
            size_score = 15
        elif total_installs > 100_000:
            size_score = 10
        else:
            size_score = 5

        # --- Trend / Freshness Signal (0-20) ---
        # Based on gap signals and review recency as a proxy
        gap_count = len(review_data.get("gaps", []))
        pain_count = len(review_data.get("pain_points", []))

        if gap_count >= 10:
            trend_score = 20
        elif gap_count >= 5:
            trend_score = 15
        elif gap_count >= 2:
            trend_score = 10
        else:
            trend_score = 5

        # Bonus for diverse pain points (more categories = more opportunity)
        trend_score = min(20, trend_score + pain_count * 2)

        # --- TOTAL ---
        total = round(gap_score + frust_score + size_score + trend_score)
        total = min(100, max(0, total))

        # Verdict
        if total >= 75:
            verdict = "EXCELLENT - Strong opportunity, move fast!"
        elif total >= 60:
            verdict = "GOOD - Solid opportunity with clear gaps"
        elif total >= 45:
            verdict = "MODERATE - Opportunity exists but needs differentiation"
        elif total >= 30:
            verdict = "CAUTIOUS - Limited opportunity, niche positioning needed"
        else:
            verdict = "WEAK - Saturated market or small audience"

        result = {
            "total_score": total,
            "verdict": verdict,
            "breakdown": {
                "market_gap": round(gap_score, 1),
                "frustration_level": round(frust_score, 1),
                "market_size": round(size_score, 1),
                "trend_signal": round(trend_score, 1),
            },
            "max_scores": {
                "market_gap": 30,
                "frustration_level": 25,
                "market_size": 25,
                "trend_signal": 20,
            },
        }

        # Display
        self._display_opportunity_score(result)

        return result

    def _display_opportunity_score(self, result):
        """Print formatted opportunity score."""
        print("\n" + SEPARATOR)
        print("  OPPORTUNITY SCORE: %d / 100" % result["total_score"])
        print(SEPARATOR)

        bd = result["breakdown"]
        mx = result["max_scores"]
        for key in ["market_gap", "frustration_level", "market_size", "trend_signal"]:
            label = key.replace("_", " ").title()
            val = bd[key]
            maxv = mx[key]
            print("    %-22s : %5.1f / %2d  %s" % (
                label, val, maxv, bar_chart(val, maxv, width=20),
            ))

        print("\n  VERDICT: %s" % result["verdict"])
        print(SEPARATOR)

    # ------------------------------------------------------------------
    # 5. TAM ESTIMATION
    # ------------------------------------------------------------------

    def estimate_tam(self, segment_size, arpu, conversion_rate=0.02):
        """
        Bottom-up TAM/SAM/SOM estimation.

        Args:
            segment_size: Total addressable users in the segment
            arpu: Average Revenue Per User (monthly, in EUR/USD)
            conversion_rate: Expected free-to-paid conversion rate

        Returns:
            dict with TAM, SAM, SOM figures (annual)
        """
        annual_arpu = arpu * 12

        # TAM = Total Addressable Market (everyone in the segment)
        tam = segment_size * annual_arpu

        # SAM = Serviceable Addressable Market (realistic reach ~20-30% of TAM)
        sam_ratio = 0.25
        sam = tam * sam_ratio

        # SOM = Serviceable Obtainable Market (what you can capture in year 1)
        # Based on conversion rate applied to a fraction of SAM
        som = segment_size * sam_ratio * conversion_rate * annual_arpu

        result = {
            "segment_size": segment_size,
            "arpu_monthly": arpu,
            "arpu_annual": annual_arpu,
            "conversion_rate": conversion_rate,
            "tam_annual": round(tam),
            "sam_annual": round(sam),
            "som_annual": round(som),
            "som_monthly": round(som / 12),
        }

        # Display
        print("\n" + SEPARATOR_THIN)
        print("  TAM ESTIMATION (Bottom-Up)")
        print(SEPARATOR_THIN)
        print("  Segment size     : %s users" % format_number(segment_size))
        print("  ARPU             : %.2f/month (%.2f/year)" % (arpu, annual_arpu))
        print("  Conversion rate  : %.1f%%" % (conversion_rate * 100))
        print("")
        print("  TAM (total)      : %s EUR/year" % format_number(tam))
        print("  SAM (reachable)  : %s EUR/year" % format_number(sam))
        print("  SOM (year 1)     : %s EUR/year (%s/month)" % (
            format_number(som), format_number(som / 12),
        ))
        print(SEPARATOR_THIN)

        return result

    # ------------------------------------------------------------------
    # 6. MARKET CONCENTRATION (HHI)
    # ------------------------------------------------------------------

    def calculate_hhi(self, apps_data):
        """
        Calculate the Herfindahl-Hirschman Index from install distribution.

        HHI < 1500: Competitive market
        HHI 1500-2500: Moderately concentrated
        HHI > 2500: Highly concentrated (dominated by few players)

        Args:
            apps_data: List of app dicts with 'installs' key

        Returns:
            dict with hhi value and interpretation
        """
        installs = [a.get("installs", 0) for a in apps_data if a.get("installs", 0) > 0]
        if not installs:
            return {"hhi": 0, "interpretation": "No data", "shares": []}

        total = sum(installs)
        shares = [(i / total * 100) for i in installs]
        hhi = sum(s ** 2 for s in shares)

        if hhi < 1500:
            interp = "COMPETITIVE - No dominant player, room for new entrants"
        elif hhi < 2500:
            interp = "MODERATE - A few strong players but still accessible"
        else:
            interp = "CONCENTRATED - Market dominated by 1-2 players"

        result = {
            "hhi": round(hhi),
            "interpretation": interp,
            "top_shares": sorted(shares, reverse=True)[:5],
        }

        print("\n  MARKET CONCENTRATION (HHI):")
        print("    HHI Index : %d" % result["hhi"])
        print("    Status    : %s" % interp)
        if result["top_shares"]:
            print("    Top shares: %s" % ", ".join(
                "%.1f%%" % s for s in result["top_shares"]
            ))

        return result

    # ------------------------------------------------------------------
    # 7. FULL HUNT (orchestrator)
    # ------------------------------------------------------------------

    def full_hunt(self, query, keywords=None, top=15, review_count=200,
                  segment_size=None, arpu=None, conversion_rate=0.02):
        """
        Run a complete niche hunt: scan, analyze, score, and report.

        Args:
            query: Main search query
            keywords: Additional keywords (list) to expand the search
            top: Number of apps to scan
            review_count: Reviews per competitor to analyze
            segment_size: (optional) Target user base for TAM
            arpu: (optional) Avg revenue per user for TAM
            conversion_rate: Free-to-paid conversion estimate

        Returns:
            Complete report dict
        """
        print("\n" + SEPARATOR)
        print("  MOAT NICHE HUNTER - FULL ANALYSIS")
        print("  Query    : %s" % query)
        print("  Date     : %s" % self.timestamp)
        print("  Language : %s | Country: %s" % (self.lang, self.country))
        print(SEPARATOR)

        report = {
            "meta": {
                "query": query,
                "keywords": keywords or [],
                "timestamp": self.timestamp,
                "lang": self.lang,
                "country": self.country,
            },
        }

        # Step 1: Market Scan
        print("\n[STEP 1/4] Scanning market...")
        market_data = self.scan_market(query, top=top)
        report["market"] = market_data

        # Step 2: Competitor Analysis
        # Pick top competitors + weakest to analyze
        app_ids_to_analyze = []
        if market_data["apps"]:
            # Take top 5 by installs + weakest 3
            by_installs = sorted(
                market_data["apps"],
                key=lambda x: x["installs"],
                reverse=True,
            )[:5]
            weakest = market_data.get("weakest_competitors", [])[:3]

            seen = set()
            for a in by_installs + weakest:
                if a["appId"] not in seen:
                    app_ids_to_analyze.append(a["appId"])
                    seen.add(a["appId"])

        if app_ids_to_analyze:
            print("\n[STEP 2/4] Analyzing %d competitors..." % len(app_ids_to_analyze))
            review_data = self.analyze_competitors(app_ids_to_analyze, review_count)
        else:
            print("\n[STEP 2/4] No competitors to analyze (no apps found).")
            review_data = self._empty_review_analysis()
        report["reviews"] = review_data

        # Step 3: Market Concentration
        print("\n[STEP 3/4] Calculating market concentration...")
        hhi_data = self.calculate_hhi(market_data.get("apps", []))
        report["concentration"] = hhi_data

        # Step 4: Opportunity Score
        print("\n[STEP 4/4] Computing opportunity score...")
        score_data = self.calculate_opportunity_score(market_data, review_data)
        report["opportunity"] = score_data

        # Optional: TAM Estimation
        if segment_size and arpu:
            print("\n[BONUS] TAM Estimation...")
            tam_data = self.estimate_tam(segment_size, arpu, conversion_rate)
            report["tam"] = tam_data

        # Final Verdict
        self._display_final_verdict(report)

        return report

    def _display_final_verdict(self, report):
        """Display the final hunt verdict."""
        score = report.get("opportunity", {}).get("total_score", 0)
        verdict = report.get("opportunity", {}).get("verdict", "N/A")
        stats = report.get("market", {}).get("stats", {})
        gaps = report.get("reviews", {}).get("gaps", [])
        pain_points = report.get("reviews", {}).get("pain_points", [])

        print("\n" + SEPARATOR)
        print("  FINAL VERDICT")
        print(SEPARATOR)
        print("")
        print("  Query             : %s" % report["meta"]["query"])
        print("  Opportunity Score : %d / 100" % score)
        print("  Verdict           : %s" % verdict)
        print("")
        print("  Market saturation : %s" % stats.get("saturation", "N/A"))
        print("  HHI concentration : %s" % report.get("concentration", {}).get("interpretation", "N/A"))
        print("  User frustration  : %d categories with pain" % len(pain_points))
        print("  Gap signals found : %d" % len(gaps))
        print("")

        if pain_points:
            print("  KEY PAIN POINTS TO EXPLOIT:")
            for pp in pain_points[:3]:
                print("    -> [%s] %d mentions" % (pp["category"].upper(), pp["mention_count"]))

        if gaps:
            print("")
            print("  TOP USER WISHES TO ADDRESS:")
            for g in gaps[:5]:
                print('    -> "%s"' % safe_str(g)[:80])

        # Recommendation
        print("")
        if score >= 60:
            print("  RECOMMENDATION: GO - Build an MVP targeting the top pain points.")
            print("  Focus on: %s" % ", ".join(
                pp["category"] for pp in pain_points[:3]
            ) if pain_points else "quality and UX")
        elif score >= 40:
            print("  RECOMMENDATION: EXPLORE - Validate demand with a landing page test.")
            print("  Find a niche angle that competitors are ignoring.")
        else:
            print("  RECOMMENDATION: PASS - Look for a less saturated market.")
            print("  Or find a very specific underserved sub-niche.")

        print("")
        print(SEPARATOR)

    # ------------------------------------------------------------------
    # 8. REPORT EXPORT
    # ------------------------------------------------------------------

    def save_report(self, report, filename=None):
        """
        Save the full report as a JSON file.

        Args:
            report: The report dict from full_hunt()
            filename: Output filename (auto-generated if None)

        Returns:
            Path to the saved file
        """
        if filename is None:
            query_slug = re.sub(r"[^a-zA-Z0-9]+", "_", report.get("meta", {}).get("query", "hunt"))
            date_str = datetime.now().strftime("%Y%m%d_%H%M")
            filename = "hunt_%s_%s.json" % (query_slug, date_str)

        # Ensure data directory exists
        data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
        os.makedirs(data_dir, exist_ok=True)

        filepath = os.path.join(data_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=True, default=str)

        print("\n  Report saved: %s" % filepath)
        return filepath


# ---------------------------------------------------------------------------
# CLI ENTRY POINT
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="MOAT Niche Hunter - Find app market opportunities on Google Play",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python niche_hunter.py "meditation sommeil" --lang fr --top 15
  python niche_hunter.py "invoice freelance" --lang fr --report
  python niche_hunter.py "coach fitness CRM" --lang en --country us
  python niche_hunter.py "pomodoro" --lang fr --arpu 4.99 --segment 500000
        """,
    )

    parser.add_argument(
        "query",
        help="Search query (keywords or category)",
    )
    parser.add_argument(
        "--lang", default="fr",
        help="Language code (default: fr)",
    )
    parser.add_argument(
        "--country", default="fr",
        help="Country code (default: fr)",
    )
    parser.add_argument(
        "--top", type=int, default=15,
        help="Number of top apps to scan (default: 15)",
    )
    parser.add_argument(
        "--reviews", type=int, default=200,
        help="Number of reviews to fetch per app (default: 200)",
    )
    parser.add_argument(
        "--report", action="store_true",
        help="Save a JSON report to data/ directory",
    )
    parser.add_argument(
        "--segment", type=int, default=None,
        help="Target segment size (users) for TAM estimation",
    )
    parser.add_argument(
        "--arpu", type=float, default=None,
        help="Average Revenue Per User (monthly) for TAM estimation",
    )
    parser.add_argument(
        "--conversion", type=float, default=0.02,
        help="Free-to-paid conversion rate for TAM (default: 0.02)",
    )
    parser.add_argument(
        "--scan-only", action="store_true",
        help="Only run market scan (skip reviews analysis)",
    )

    args = parser.parse_args()

    # Initialize hunter
    hunter = NicheHunter(lang=args.lang, country=args.country)

    if args.scan_only:
        # Quick market scan only
        market = hunter.scan_market(args.query, top=args.top)
        if args.report:
            hunter.save_report({"meta": {"query": args.query}, "market": market})
    else:
        # Full hunt
        report = hunter.full_hunt(
            query=args.query,
            top=args.top,
            review_count=args.reviews,
            segment_size=args.segment,
            arpu=args.arpu,
            conversion_rate=args.conversion,
        )

        if args.report:
            hunter.save_report(report)

    print("\nDone.")


if __name__ == "__main__":
    main()
