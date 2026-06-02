#!/usr/bin/env python3
"""
MOAT App Discovery System — Community Signal Detector

Mesure la demande organique REELLE sur les forums francophones
en cherchant des signaux de frustration et de demande non satisfaite.

Contrairement à MiroFish (simulation de personas LLM), ce module lit
des données réelles : posts Reddit, résultats de recherche, forums FR.
Pas de Neo4j. Pas d'Ollama. Pas d'API payante. 15-30 secondes d'exécution.

Sources :
  - Reddit (API publique JSON, sans auth)
    Subreddits FR : r/france, r/sante, r/travail, r/medecine,
                    r/emploi, r/JFR, r/franceculture, r/informatique
  - Fallback PRAW (optionnel, si .env configure avec client_id/secret)

Scoring (0-100) :
  - demand_volume    (0-40) : volume de posts sur le problème
  - solution_gap     (0-35) : proportion de posts sans solution trouvée
  - recency_boost    (0-15) : concentration des posts récents (30j vs 90j)
  - multi_channel    (0-10) : signal détecté sur plusieurs subreddits

Sortie :
  - community_signal_score (0-100)
  - verdict : FORT / MOYEN / FAIBLE / INEXISTANT
  - adjustment : +3 / +1 / 0 / -3 (appliqué au score V3)
  - top_posts : 5 posts les plus représentatifs
  - top_gap_phrases : phrases indiquant une demande non satisfaite

Usage :
    python community_signal.py "burn-out" "stress travail" --idea "BurnoutDetect"
    python community_signal.py "diabète type 2" "glycémie" --idea "DiabèteCoach FR"
    python community_signal.py "facturation électronique" --idea "TimeToInvoice" --validate
    python community_signal.py "insomnie" "sommeil" --idea "SleepCoach FR" --top 10
"""

import argparse
import json
import os
import re
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime, timedelta

import requests

# ── Optional PRAW (Reddit Python API Wrapper) ──
# Needed only if REDDIT_CLIENT_ID is set in env (deeper search, higher rate limit)
try:
    import praw
    HAS_PRAW = True
except ImportError:
    HAS_PRAW = False

# ── Reddit public API — no auth required ──
REDDIT_BASE = "https://www.reddit.com"
REDDIT_HEADERS = {
    "User-Agent": "MOAT-AppHunter/1.0 (community signal detector; solo dev research tool)"
}
REDDIT_REQUEST_DELAY = 1.2   # seconds between requests (respect rate limit)

# ── Target subreddits FR ──
# Ordered by relevance for FR app ideas
SUBREDDITS_FR = [
    "france",
    "sante",
    "travail",
    "medecine",
    "emploi",
    "JFR",            # Je finance ma retraite / finances perso
    "informatique",
    "apprendrefrancais",
]

SUBREDDITS_WELLNESS = [
    "france",
    "sante",
    "travail",
    "medecine",
    "emploi",
    "psychologie",
]

SUBREDDITS_TECH = [
    "france",
    "informatique",
    "developpement",
    "emploi",
    "JFR",
]

# ── Signal markers ──

# Phrases indiquant que le problème existe et qu'aucune solution n'a été trouvée
GAP_MARKERS_FR = [
    "pas d'app",
    "aucune app",
    "pas d'application",
    "aucune application",
    "je cherche",
    "quelqu'un connaît",
    "quelqu'un connait",
    "est-ce qu'il existe",
    "existe-t-il",
    "y a-t-il une app",
    "y a t il",
    "je n'arrive pas",
    "j'arrive pas",
    "personne ne",
    "rien de satisfaisant",
    "rien ne fait",
    "pas de solution",
    "pas trouvé",
    "pas trouve",
    "sans outil",
    "galérer",
    "galerer",
    "problème",
    "probleme",
    "frustrant",
    "impossible de",
    "comment faire pour",
    "comment gérer",
    "comment gerer",
    "besoin d'aide",
    "besoin aide",
    "aide svp",
    "conseil",
    "recommande",
    "recommandes",
    "suggestion",
    "alternative à",
    "alternative a",
    "remplacer",
    "mieux que",
]

# Phrases indiquant qu'une solution satisfaisante a DÉJÀ été trouvée (mauvais signal)
SOLUTION_FOUND_MARKERS = [
    "j'utilise",
    "j utilise",
    "je recommande",
    "parfait pour",
    "fonctionne très bien",
    "fonctionne tres bien",
    "super app",
    "excellente app",
    "vraiment bien",
    "très satisfait",
    "tres satisfait",
    "exactement ce qu'il faut",
    "résolu grâce",
    "resolu grace",
]

# Marqueurs de douleur/frustration (signal positif = problème réel)
PAIN_MARKERS_FR = [
    "épuisé", "epuise", "burn-out", "burnout", "burn out",
    "stressé", "stresse", "anxieux", "anxiété", "anxiete",
    "insomnies", "insomnie", "dors mal", "sommeil",
    "diabète", "diabete", "glycémie", "glycemie", "insuline",
    "douleur", "mal au dos", "fatigue chronique",
    "perte de poids", "régime", "regime",
    "facturation", "facture", "devis", "comptabilité", "compta",
    "organisation", "planning", "gestion",
]

# ── Q1 — Astroturfing soft detection ──
# Seuil upvotes/comments suspect (campagne payée ≠ discussion organique)
# Soft warning uniquement — pas de blocage dur (faux positifs fréquents sur posts viraux)
ASTROTURFING_UPVOTE_RATIO_THRESHOLD = 50   # upvotes / max(comments, 1) > 50 = suspect
ASTROTURFING_MIN_UPVOTES = 100             # Only flag if upvotes >= 100 (bruit < 100)

# ── Q4 — Verticals à communauté privée ──
# Sur ces verticales, Reddit FR est non représentatif : communautés sur groupes FB,
# forums spécialisés, WhatsApp. Un score faible ne signifie pas un marché inexistant.
# Conséquence : l'ajustement passe automatiquement à 0 (neutre, pas -3).
PRIVATE_COMMUNITY_VERTICALS = {
    "sante_feminine": {
        "keywords": ["endometriose", "endométriose", "menopause", "ménopause",
                     "fertilite", "fertilité", "regles", "règles", "ovaires",
                     "syndrome premenstruel", "spf", "fiv", "grossesse"],
        "reason": "Santé féminine : groupes FB privés dominants, sous-représentée Reddit FR",
    },
    "deuil_addictions": {
        "keywords": ["deuil", "addiction", "alcoolisme", "sevrage", "desintox",
                     "depression severe", "depression sévère"],
        "reason": "Deuil/addictions : tabou Reddit FR, communautés spécialisées hors Reddit",
    },
    "sante_mentale_severe": {
        "keywords": ["suicide", "automutilation", "schizophrenie", "schizophrénie",
                     "bipolaire", "psychose", "tdah adulte"],
        "reason": "Santé mentale sévère : modération stricte Reddit, communautés privées",
    },
    "sexualite": {
        "keywords": ["sexualite", "sexualité", "dysfonction erectile", "libido",
                     "intimite", "intimité"],
        "reason": "Sexualité : tabou sur Reddit FR public",
    },
    "parentalite_nourrisson": {
        "keywords": ["nourrisson", "allaitement", "maternite", "maternité",
                     "bebe de moins de 2 ans", "bebe de 1 an"],
        "reason": "Nourrissons : communautés Instagram/Facebook dominantes, pas Reddit FR",
    },
    "seniors": {
        "keywords": ["ehpad", "alzheimer", "senior de 70 ans", "senior de 80 ans",
                     "maison de retraite", "aide soignant"],
        "reason": "Population âgée : sous-représentée sur Reddit FR",
    },
}


def detect_private_vertical(keywords):
    """
    Détecte si les mots-clés de recherche tombent dans une verticale à communauté privée.

    Returns (vertical_name, reason) ou (None, None).

    Conséquence sur le scoring : adjustment = 0 (ni bonus ni pénalité).
    Le faible signal Reddit est ATTENDU et non informatif pour ces verticales.
    """
    kw_lower = " ".join(keywords).lower()
    kw_lower = re.sub(r'[àâä]', 'a', kw_lower)
    kw_lower = re.sub(r'[éèêë]', 'e', kw_lower)
    kw_lower = re.sub(r'[îï]', 'i', kw_lower)
    kw_lower = re.sub(r'[ôö]', 'o', kw_lower)
    kw_lower = re.sub(r'[ùûü]', 'u', kw_lower)
    kw_lower = re.sub(r'[ç]', 'c', kw_lower)

    for vertical_name, meta in PRIVATE_COMMUNITY_VERTICALS.items():
        for trigger in meta["keywords"]:
            trigger_norm = trigger.lower()
            trigger_norm = re.sub(r'[àâä]', 'a', trigger_norm)
            trigger_norm = re.sub(r'[éèêë]', 'e', trigger_norm)
            trigger_norm = re.sub(r'[îï]', 'i', trigger_norm)
            trigger_norm = re.sub(r'[ôö]', 'o', trigger_norm)
            trigger_norm = re.sub(r'[ùûü]', 'u', trigger_norm)
            trigger_norm = re.sub(r'[ç]', 'c', trigger_norm)
            if trigger_norm in kw_lower:
                return vertical_name, meta["reason"]

    return None, None


def detect_astroturfing(posts):
    """
    Détection soft d'astroturfing (Q1).

    Retourne une liste d'anomaly_warnings (texte) pour les posts suspects.
    Ne bloque PAS le scoring — signal informatif uniquement.

    Logique :
    - upvotes / max(comments, 1) > 50 ET upvotes >= 100 → suspect
    - Pattern : post viral légitime OU campagne organisée
    - Limitation : sans account age (API publique), impossibilité de confirmation

    Limitation documentée pour Notion :
    "Le community_signal_score ne détecte pas l'astroturfing organisé.
     Les anomalies de ratio upvotes/comments sont signalées en warning
     mais non filtrées. À pondérer manuellement si concurrent connu
     pour campagnes Reddit (ex: grandes marques SaaS B2B)."
    """
    warnings = []
    suspicious_ids = set()

    for p in posts:
        upvotes = p.get("score", 0)
        comments = p.get("num_comments", 0)

        if upvotes >= ASTROTURFING_MIN_UPVOTES:
            ratio = upvotes / max(comments, 1)
            if ratio > ASTROTURFING_UPVOTE_RATIO_THRESHOLD:
                suspicious_ids.add(p.get("id", ""))
                warnings.append({
                    "post_id": p.get("id", ""),
                    "title": p.get("title", "")[:80],
                    "upvotes": upvotes,
                    "comments": comments,
                    "ratio": round(ratio, 1),
                    "flag": "RATIO_SUSPECT",
                    "note": (
                        f"Ratio {round(ratio, 1)}x upvotes/comments. "
                        "Peut indiquer astroturfing ou post viral sans débat. "
                        "Vérifier manuellement."
                    ),
                })

    return warnings, suspicious_ids


# ============================================================
# Reddit Public API (sans auth)
# ============================================================

def reddit_search_public(keywords, subreddits=None, timeframe="year", limit=100):
    """
    Recherche Reddit via l'API publique JSON (pas d'auth requise).

    Returns list of post dicts: {title, body, url, score, num_comments,
                                  created_utc, subreddit, found_in}
    """
    posts = []
    query = " OR ".join(f'"{kw}"' if " " in kw else kw for kw in keywords)
    seen_ids = set()

    targets = subreddits or SUBREDDITS_FR

    for sub in targets:
        url = f"{REDDIT_BASE}/r/{sub}/search.json"
        params = {
            "q": query,
            "sort": "new",
            "t": timeframe,
            "limit": min(limit, 100),
            "restrict_sr": "true",
        }

        try:
            resp = requests.get(url, headers=REDDIT_HEADERS, params=params, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                for child in data.get("data", {}).get("children", []):
                    p = child["data"]
                    pid = p.get("id", "")
                    if pid not in seen_ids:
                        seen_ids.add(pid)
                        posts.append({
                            "id": pid,
                            "title": p.get("title", ""),
                            "body": p.get("selftext", ""),
                            "url": f"{REDDIT_BASE}{p.get('permalink', '')}",
                            "score": p.get("score", 0),
                            "num_comments": p.get("num_comments", 0),
                            "created_utc": p.get("created_utc", 0),
                            "subreddit": p.get("subreddit", sub),
                            "found_in": "reddit",
                        })
            elif resp.status_code == 429:
                print(f"    [rate limit] r/{sub} — pause 3s")
                time.sleep(3)
            time.sleep(REDDIT_REQUEST_DELAY)
        except requests.RequestException as e:
            print(f"    [erreur] r/{sub}: {str(e)[:50]}")

    # Also search globally (all of Reddit, not sub-restricted)
    global_url = f"{REDDIT_BASE}/search.json"
    global_params = {
        "q": f'({query}) site:reddit.com',
        "sort": "new",
        "t": timeframe,
        "limit": min(limit, 50),
        "restrict_sr": "false",
    }
    try:
        resp = requests.get(global_url, headers=REDDIT_HEADERS,
                            params={"q": query, "sort": "relevance",
                                    "t": timeframe, "limit": 50},
                            timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            for child in data.get("data", {}).get("children", []):
                p = child["data"]
                pid = p.get("id", "")
                # Only add non-duplicate posts from FR-relevant subs or if title is FR
                sub_name = p.get("subreddit", "").lower()
                is_fr_sub = any(s in sub_name for s in ["france", "sante", "travail",
                                                          "medecine", "emploi"])
                if pid not in seen_ids and is_fr_sub:
                    seen_ids.add(pid)
                    posts.append({
                        "id": pid,
                        "title": p.get("title", ""),
                        "body": p.get("selftext", ""),
                        "url": f"{REDDIT_BASE}{p.get('permalink', '')}",
                        "score": p.get("score", 0),
                        "num_comments": p.get("num_comments", 0),
                        "created_utc": p.get("created_utc", 0),
                        "subreddit": p.get("subreddit", ""),
                        "found_in": "reddit_global",
                    })
        time.sleep(REDDIT_REQUEST_DELAY)
    except requests.RequestException:
        pass

    return posts


def reddit_search_praw(keywords, subreddits=None, limit=100):
    """
    Recherche Reddit via PRAW (nécessite client_id + client_secret dans .env).
    Fallback silencieux si non configuré.
    """
    if not HAS_PRAW:
        return []

    client_id = os.environ.get("REDDIT_CLIENT_ID", "")
    client_secret = os.environ.get("REDDIT_CLIENT_SECRET", "")
    if not client_id or not client_secret:
        return []

    try:
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent="MOAT-AppHunter/1.0",
        )

        posts = []
        query = " OR ".join(keywords)
        targets = subreddits or SUBREDDITS_FR

        for sub in targets:
            try:
                subreddit = reddit.subreddit(sub)
                for post in subreddit.search(query, sort="new",
                                              time_filter="year", limit=limit):
                    posts.append({
                        "id": post.id,
                        "title": post.title,
                        "body": post.selftext,
                        "url": f"https://reddit.com{post.permalink}",
                        "score": post.score,
                        "num_comments": post.num_comments,
                        "created_utc": post.created_utc,
                        "subreddit": sub,
                        "found_in": "praw",
                    })
            except Exception:
                pass

        return posts
    except Exception:
        return []


# ============================================================
# Analyse des posts
# ============================================================

def classify_post(post):
    """
    Classifie un post en : 'gap' / 'solution_found' / 'pain' / 'neutral'

    Returns (classification, matched_phrases)
    """
    text = (post.get("title", "") + " " + post.get("body", "")).lower()
    text = re.sub(r'[àâä]', 'a', text)
    text = re.sub(r'[éèêë]', 'e', text)
    text = re.sub(r'[îï]', 'i', text)
    text = re.sub(r'[ôö]', 'o', text)
    text = re.sub(r'[ùûü]', 'u', text)
    text = re.sub(r'[ç]', 'c', text)

    gap_matches = [m for m in GAP_MARKERS_FR if m in text]
    solution_matches = [m for m in SOLUTION_FOUND_MARKERS if m in text]
    pain_matches = [m for m in PAIN_MARKERS_FR if m in text]

    if gap_matches:
        return "gap", gap_matches
    elif solution_matches and not gap_matches:
        return "solution_found", solution_matches
    elif pain_matches:
        return "pain", pain_matches
    else:
        return "neutral", []


def is_recent(created_utc, days=30):
    """Check if post is within last N days."""
    cutoff = datetime.now().timestamp() - (days * 86400)
    return created_utc > cutoff


def extract_gap_phrases(posts, top_n=5):
    """Extract most representative gap-indicating phrases from posts."""
    phrase_counter = Counter()

    for post in posts:
        text = (post.get("title", "") + " " + post.get("body", "")).lower()
        classification, matches = classify_post(post)
        if classification in ("gap", "pain"):
            for m in matches:
                phrase_counter[m] += 1

    return phrase_counter.most_common(top_n)


def compute_community_signal(posts, keywords, active_flags=None):
    """
    Calcule le community_signal_score (0-100).

    Composantes :
      - demand_volume    (0-40) : volume total de posts pertinents
      - solution_gap     (0-35) : proportion posts sans solution satisfaisante
      - recency_boost    (0-15) : posts récents (30j) / total
      - multi_channel    (0-10) : diversité des subreddits sources

    active_flags (list[str], optionnel) : flags V3.1 actifs sur l'idée.
      Si 'market_education' présent → adjustment = 0 (évite double pénalité).
      Le faible signal communautaire est ATTENDU pour les marchés blue ocean.

    Returns dict avec score, composantes, verdict, adjustment, posts analysés,
    anomaly_warnings (Q1), adjustment_override_reason (Q2/Q4).
    """
    active_flags = active_flags or []

    # ── Q4 : Détection verticale privée ──
    private_vertical, private_reason = detect_private_vertical(keywords)

    # ── Q1 : Détection astroturfing (soft) ──
    astro_warnings, suspicious_ids = detect_astroturfing(posts)

    if not posts:
        # Compute override for empty posts case
        _empty_adj = -3
        _empty_override = None
        if private_vertical:
            _empty_adj = 0
            _empty_override = (
                f"Verticale privee '{private_vertical}' — ajustement neutralise a 0. {private_reason}"
            )
        elif "market_education" in active_flags and _empty_adj < 0:
            _empty_adj = 0
            _empty_override = (
                "Flag 'market_education' actif — ajustement negatif neutralise a 0. "
                "Un faible signal Reddit est attendu sur un marche blue ocean."
            )
        return {
            "community_signal_score": 0,
            "verdict": "INEXISTANT",
            "adjustment": _empty_adj,
            "adjustment_override_reason": _empty_override,
            "components": {
                "demand_volume": 0,
                "solution_gap": 0,
                "recency_boost": 0,
                "multi_channel": 0,
            },
            "post_count": 0,
            "gap_count": 0,
            "solution_found_count": 0,
            "pain_count": 0,
            "recent_count": 0,
            "subreddits_hit": [],
            "top_posts": [],
            "top_gap_phrases": [],
            "anomaly_warnings": astro_warnings,
            "private_vertical": private_vertical,
            "analysis_date": datetime.now().isoformat(),
        }

    # Classify all posts
    classified = []
    for p in posts:
        cls, matches = classify_post(p)
        classified.append((p, cls, matches))

    gap_posts = [p for p, cls, _ in classified if cls == "gap"]
    solution_posts = [p for p, cls, _ in classified if cls == "solution_found"]
    pain_posts = [p for p, cls, _ in classified if cls == "pain"]
    recent_posts = [p for p in posts if is_recent(p.get("created_utc", 0), days=30)]
    subreddits_hit = list(set(p.get("subreddit", "") for p in posts))

    total = len(posts)
    meaningful = len(gap_posts) + len(solution_posts) + len(pain_posts)

    # ── Composante 1 : demand_volume (0-40) ──
    # Calibré sur les marchés FR : > 50 posts = marché très actif
    if total >= 50:
        demand_volume = 40
    elif total >= 30:
        demand_volume = 32
    elif total >= 15:
        demand_volume = 24
    elif total >= 8:
        demand_volume = 16
    elif total >= 3:
        demand_volume = 8
    elif total >= 1:
        demand_volume = 4
    else:
        demand_volume = 0

    # ── Composante 2 : solution_gap (0-35) ──
    # Ratio : posts gap / (posts gap + solution_found)
    # Haute proportion de gap = besoin non satisfait = bon signal
    if meaningful > 0:
        gap_ratio = len(gap_posts) / max(len(gap_posts) + len(solution_posts), 1)
        solution_gap = round(gap_ratio * 35)
    else:
        solution_gap = 0

    # Bonus si pain_posts élevé (douleur réelle même sans gap explicite)
    if len(pain_posts) >= 5:
        solution_gap = min(solution_gap + 5, 35)

    # ── Composante 3 : recency_boost (0-15) ──
    # Si beaucoup de posts récents = sujet d'actualité
    if total > 0:
        recency_ratio = len(recent_posts) / total
        if recency_ratio >= 0.5:
            recency_boost = 15
        elif recency_ratio >= 0.3:
            recency_boost = 10
        elif recency_ratio >= 0.1:
            recency_boost = 5
        else:
            recency_boost = 0
    else:
        recency_boost = 0

    # ── Composante 4 : multi_channel (0-10) ──
    # Signal sur plusieurs subreddits = demande transversale
    n_subs = len(subreddits_hit)
    if n_subs >= 4:
        multi_channel = 10
    elif n_subs >= 3:
        multi_channel = 7
    elif n_subs >= 2:
        multi_channel = 4
    elif n_subs >= 1:
        multi_channel = 2
    else:
        multi_channel = 0

    total_score = demand_volume + solution_gap + recency_boost + multi_channel
    total_score = min(max(total_score, 0), 100)

    # ── Verdict ──
    if total_score >= 65:
        verdict = "FORT"
        adjustment = +3
    elif total_score >= 40:
        verdict = "MOYEN"
        adjustment = +1
    elif total_score >= 20:
        verdict = "FAIBLE"
        adjustment = 0
    else:
        verdict = "INEXISTANT"
        adjustment = -3

    # ── Q2 : Override si market_education flag actif ──
    # Le faible signal Reddit est ATTENDU sur les marchés blue ocean.
    # Évite double pénalité : flag market_education (-10) + community signal (-3) = -13 injuste.
    adjustment_override_reason = None
    if "market_education" in active_flags and adjustment < 0:
        adjustment_override_reason = (
            "Flag 'market_education' actif — ajustement négatif neutralisé à 0. "
            "Un faible signal Reddit est attendu sur un marché blue ocean : "
            "l'absence de communauté existante est déjà pénalisée par le flag V3.1 (-10)."
        )
        adjustment = 0

    # ── Q4 : Override si verticale privée détectée ──
    if private_vertical and adjustment != 0:
        adjustment_override_reason = (
            f"Verticale privée '{private_vertical}' détectée — ajustement neutralisé à 0. "
            f"{private_reason}"
        )
        adjustment = 0

    # ── Top posts (triés par engagement) ──
    top_posts = sorted(
        [(p, cls) for p, cls, _ in classified if cls in ("gap", "pain")],
        key=lambda x: x[0].get("num_comments", 0) + x[0].get("score", 0),
        reverse=True
    )[:5]

    top_posts_output = []
    for p, cls in top_posts:
        top_posts_output.append({
            "title": p["title"][:120],
            "subreddit": p.get("subreddit", ""),
            "classification": cls,
            "score": p.get("score", 0),
            "comments": p.get("num_comments", 0),
            "url": p.get("url", ""),
            "recent": is_recent(p.get("created_utc", 0), 30),
        })

    # ── Top gap phrases ──
    top_gap_phrases = extract_gap_phrases(posts)

    return {
        "community_signal_score": total_score,
        "verdict": verdict,
        "adjustment": adjustment,
        "adjustment_override_reason": adjustment_override_reason,
        "components": {
            "demand_volume": demand_volume,
            "solution_gap": solution_gap,
            "recency_boost": recency_boost,
            "multi_channel": multi_channel,
        },
        "post_count": total,
        "gap_count": len(gap_posts),
        "solution_found_count": len(solution_posts),
        "pain_count": len(pain_posts),
        "recent_count": len(recent_posts),
        "subreddits_hit": subreddits_hit,
        "top_posts": top_posts_output,
        "top_gap_phrases": [(phrase, count) for phrase, count in top_gap_phrases],
        "anomaly_warnings": astro_warnings,
        "private_vertical": private_vertical,
        "analysis_date": datetime.now().isoformat(),
    }


# ============================================================
# Validation post-hoc (calibration)
# ============================================================

KNOWN_GROUND_TRUTH = {
    # idea_name -> {expected_verdict, real_mrr_m6, real_downloads_m6}
    # À compléter au fur et à mesure avec les vrais résultats
    "TimeToInvoice": {
        "expected_signal": "FORT",   # Marché B2B, beaucoup de posts facturation obligo
        "note": "Décret 2026 facturation élec obligatoire -> forte demande communautaire",
    },
    "SleepCoach FR": {
        "expected_signal": "MOYEN",  # Insomnie FR : posts existants mais solutions aussi
        "note": "Calm/Headspace omniprésents, mais posts FR sur insomnie sans solution FR",
    },
}


def validate_mode(idea_name, result):
    """Affiche comparaison avec ground truth si disponible."""
    gt = KNOWN_GROUND_TRUTH.get(idea_name)
    if not gt:
        print(f"\n  [VALIDATION] Pas de ground truth pour '{idea_name}'.")
        print(f"  Après le launch, ajouter les données réelles dans KNOWN_GROUND_TRUTH.")
        return

    expected = gt.get("expected_signal", "?")
    actual = result.get("verdict", "?")
    match = "✓ MATCH" if expected == actual else "✗ ECART"

    print(f"\n  {'='*50}")
    print(f"  VALIDATION POST-HOC — {idea_name}")
    print(f"  {'='*50}")
    print(f"  Verdict attendu   : {expected}")
    print(f"  Verdict mesuré    : {actual}")
    print(f"  Résultat          : {match}")
    print(f"  Note calibration  : {gt['note']}")
    if expected != actual:
        print(f"\n  [!] Ecart détecté. Vérifier :")
        print(f"      - Les mots-clés recherchés sont-ils les bons ?")
        print(f"      - Les subreddits couvrent-ils le marché FR ?")
        print(f"      - Les GAP_MARKERS capturent-ils les vrais posts ?")


# ============================================================
# Display + Output
# ============================================================

def display_results(idea_name, keywords, result):
    """Affiche les résultats dans le style MOAT Engine."""

    print(f"\n{'='*60}")
    print(f"  COMMUNITY SIGNAL — {idea_name or ', '.join(keywords)}")
    print(f"  Keywords: {', '.join(keywords)}")
    print(f"{'='*60}")

    c = result["components"]
    total = result["community_signal_score"]

    print(f"\n  {'Composante':25s} {'Score':>6s} {'Max':>5s} {'Barre'}")
    print(f"  {'-'*25} {'-'*6} {'-'*5} {'-'*20}")

    comp_meta = [
        ("Demand Volume",    c["demand_volume"],   40),
        ("Solution Gap",     c["solution_gap"],    35),
        ("Recency Boost",    c["recency_boost"],   15),
        ("Multi Channel",    c["multi_channel"],   10),
    ]
    for label, score, max_val in comp_meta:
        pct = score / max_val if max_val else 0
        bar_len = int(pct * 15)
        bar = '#' * bar_len + '.' * (15 - bar_len)
        print(f"  {label:25s} {score:>5d} /{max_val:<4d} [{bar}]")

    print(f"\n  {'TOTAL':25s} {total:>5d} /100")
    print(f"  {'VERDICT':25s} {result['verdict']}")
    print(f"  {'AJUSTEMENT SCORE V3':25s} {result['adjustment']:+d} pts")

    print(f"\n  POSTS ANALYSÉS:")
    print(f"    Total trouvés      : {result['post_count']}")
    print(f"    GAP (pas de solution) : {result['gap_count']}")
    print(f"    Solution trouvée   : {result['solution_found_count']}")
    print(f"    Douleur/frustration: {result['pain_count']}")
    print(f"    Récents (30j)      : {result['recent_count']}")
    print(f"    Subreddits touchés : {', '.join(result['subreddits_hit']) or '(aucun)'}")

    if result["top_gap_phrases"]:
        print(f"\n  TOP PHRASES GAP :")
        for phrase, count in result["top_gap_phrases"]:
            bar = '#' * min(count, 30)
            print(f"    {phrase:30s} {bar} ({count})")

    if result["top_posts"]:
        print(f"\n  TOP POSTS (engagement) :")
        for p in result["top_posts"]:
            recent_tag = " [RÉCENT]" if p["recent"] else ""
            cls_tag = "GAP" if p["classification"] == "gap" else "DOULEUR"
            print(f"\n    [{cls_tag}]{recent_tag} r/{p['subreddit']}")
            print(f"    \"{p['title']}\"")
            print(f"    {p['score']} upvotes | {p['comments']} commentaires")
            print(f"    {p['url']}")

    # ── Q1 : Afficher anomalies astroturfing ──
    astro = result.get("anomaly_warnings", [])
    if astro:
        print(f"\n  [!] ANOMALIES RATIO UPVOTES/COMMENTS ({len(astro)} post(s)) :")
        for w in astro:
            print(f"    ratio {w['ratio']}x : \"{w['title']}\"")
        print(f"  Limitation : sans account age, astroturfing non confirmable.")
        print(f"  Vérifier manuellement si concurrent connu pour campagnes Reddit.")

    # ── Q2/Q4 : Afficher override reason ──
    override = result.get("adjustment_override_reason")
    if override:
        print(f"\n  [OVERRIDE] Ajustement modifié :")
        print(f"  {override}")

    print(f"\n  {'*'*50}")
    verdict_msgs = {
        "FORT":      "Demande communautaire forte — adoption facilitée. Score +3.",
        "MOYEN":     "Signal présent mais modéré. Score +1.",
        "FAIBLE":    "Peu de signal communautaire. Score neutre (0).",
        "INEXISTANT": "Aucun signal détecté. Marché éducatif ou niche très fermée. Score -3.",
    }
    print(f"  {verdict_msgs.get(result['verdict'], '')}")
    if result["adjustment"] == 0 and override:
        print(f"  Ajustement final : 0 (neutralisé — voir OVERRIDE ci-dessus).")
    print(f"  {'*'*50}")


def save_result(idea_name, keywords, result):
    """Sauvegarde le résultat dans data/research/ (cohérent avec engine_*.json)."""
    output_dir = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "data", "research"
    )
    os.makedirs(output_dir, exist_ok=True)

    slug = re.sub(r"[^\w]", "_", (idea_name or "_".join(keywords)).lower())
    filename = f"community_{slug}_{datetime.now():%Y%m%d_%H%M}.json"
    filepath = os.path.join(output_dir, filename)

    output = {
        "idea": idea_name,
        "keywords": keywords,
        "date": datetime.now().isoformat(),
        "result": result,
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n  Rapport sauvegardé : {filepath}")
    return filepath


# ============================================================
# Main runner
# ============================================================

def run_community_signal(keywords, idea_name=None, subreddits=None,
                         active_flags=None,
                         validate=False, save=True, quiet=False):
    """
    Point d'entrée principal. Utilisable depuis moat_engine.py :

        from community_signal import run_community_signal
        cs = run_community_signal(
            keywords=["burn-out", "stress travail"],
            idea_name="BurnoutDetect",
            active_flags=["rgpd_sante", "partner_medical"],  # flags V3.1 actifs
        )
        adjustment = cs["adjustment"]   # +3 / +1 / 0 / -3

    active_flags : liste des flags V3.1 actifs sur l'idée (ex: ['market_education']).
      - 'market_education' → neutralise les ajustements négatifs (-3 → 0)
      - Verticales privées → neutralise tous les ajustements (≠ 0 → 0)

    Returns le dict result complet.
    """
    if not quiet:
        print(f"\n{'#'*60}")
        print(f"  COMMUNITY SIGNAL DETECTOR")
        print(f"  Idea : {idea_name or 'N/A'}")
        print(f"  Keywords : {', '.join(keywords)}")
        print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print(f"{'#'*60}")
        print(f"\n  [1/3] Recherche Reddit (API publique)...")

    # Try PRAW first (richer data), fallback to public API
    posts = []
    if HAS_PRAW and os.environ.get("REDDIT_CLIENT_ID"):
        if not quiet:
            print(f"       Mode PRAW (credentials détectés)")
        posts = reddit_search_praw(keywords, subreddits=subreddits)

    if not posts:
        if not quiet and HAS_PRAW:
            print(f"       Mode API publique (pas de credentials PRAW)")
        posts = reddit_search_public(keywords, subreddits=subreddits)

    if not quiet:
        print(f"       {len(posts)} posts récupérés")
        print(f"\n  [2/3] Analyse et classification des posts...")

    result = compute_community_signal(posts, keywords, active_flags=active_flags)

    if not quiet:
        print(f"       Score : {result['community_signal_score']}/100 — {result['verdict']}")
        print(f"\n  [3/3] Génération du rapport...")
        display_results(idea_name, keywords, result)

        if validate:
            validate_mode(idea_name, result)

        if save:
            save_result(idea_name, keywords, result)

    return result


# ============================================================
# CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="MOAT Community Signal Detector — mesure la demande organique réelle"
    )
    parser.add_argument(
        "keywords", nargs="+",
        help="Mots-clés à rechercher (ex: 'burn-out' 'stress travail')"
    )
    parser.add_argument(
        "--idea", "-i",
        help="Nom de l'idée (pour le nom du fichier output)"
    )
    parser.add_argument(
        "--subreddits", "-s",
        help="Subreddits custom (virgule, ex: 'france,sante,travail')"
    )
    parser.add_argument(
        "--top", type=int, default=5,
        help="Nombre de top posts à afficher (défaut: 5)"
    )
    parser.add_argument(
        "--validate", action="store_true",
        help="Mode validation post-hoc (compare avec ground truth si disponible)"
    )
    parser.add_argument(
        "--no-save", action="store_true",
        help="Ne pas sauvegarder le rapport JSON"
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Output JSON brut (pour intégration pipeline)"
    )

    args = parser.parse_args()

    subreddits = [s.strip() for s in args.subreddits.split(",")] if args.subreddits else None

    result = run_community_signal(
        keywords=args.keywords,
        idea_name=args.idea,
        subreddits=subreddits,
        validate=args.validate,
        save=not args.no_save,
        quiet=args.json,
    )

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
