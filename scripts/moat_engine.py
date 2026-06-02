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

try:
    from community_signal import run_community_signal
    modules['community_signal'] = True
except ImportError:
    modules['community_signal'] = False


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
    'rgpd_sante': -5,           # V3.1: B2C health data (Art.9) - added after SleepCoach audit
    'rgpd_sante_b2b': -10,      # V3.1 Cycle 2: B2B health data (Art.9 + Art.28 + HDS 15-30K/an + DPIA) - PatientFlow audit
}

# ============================================================
# ── V3.1 UPGRADES (2026-04-19 — post-audit ShadowWork + SleepCoach) ──
# ============================================================
# See scripts/MOAT_ENGINE_V3.1_POSTMORTEM.md for rationale
#
# 7 rules enforced:
# A1 — Coherence geographique TAM-Trend-SOM
# A2 — Trend STABLE if target market index avg < 50/100
# A3 — Forecast/SOM Solo ratio (<=3x OK, 3-5x FLAG, >5x KILL)
# A4 — Score delta traceability (BLOCKING on commit)
# B5 — timing_type enum (1=regulatory, 2=chronic, 3=cultural)
# B6.1 — Readiness gating binary (blocker active → force B-Validate)
# B7 — data_freshness_date > 90 days → re-audit required

# A2 — Trend multiplier micro-volume guard
MICRO_VOLUME_THRESHOLD = 50  # Below this index avg (0-100), force STABLE

# A2 raffine (Sonnet cross-review) — Macro-volume stable guard
# If volume is HIGH (>=50) but variation is LOW (<10%), also force STABLE
# (catches pattern like insomnie FR: avg 77/100 but +3.4% = noise, not UP)
MACRO_VOLUME_VARIATION_THRESHOLD = 10  # Variation % abs below this + volume>=50 -> STABLE

# A3 — Forecast coherence thresholds
FORECAST_COHERENCE_FLAG = 3.0  # Ratio forecast/SOM Solo: flag + explanation
FORECAST_COHERENCE_KILL = 5.0  # Ratio forecast/SOM Solo: KILL forecast

# A1 — Geographic target codes (must match TAM geo)
GEOGRAPHIC_TARGETS = ['FR', 'BE', 'CH', 'QC', 'DE', 'IT', 'ES', 'UK', 'US', 'GLOBAL']

# A1 — TAM sanity thresholds by geographic target (in EUR)
# If TAM exceeds these, probably global/multi-country, not national
# Loose heuristic: national_tam_max ≈ population × avg_annual_spend_per_capita
TAM_MAX_NATIONAL = {
    'FR': 100_000_000_000,   # 100B EUR = probably global
    'BE': 20_000_000_000,
    'CH': 30_000_000_000,
    'QC': 20_000_000_000,
    'DE': 150_000_000_000,
    'IT': 100_000_000_000,
    'ES': 80_000_000_000,
    'UK': 150_000_000_000,
    'US': 1_000_000_000_000,
    'GLOBAL': float('inf'),
}

# B5 — Timing type enum
TIMING_TYPES = {
    1: {
        'label': 'Driver reglementaire',
        'window_months': '36-60',
        'priority_rank': 1,
        'examples': 'TimeToInvoice (facturation electronique obligatoire)',
    },
    2: {
        'label': 'Pathologie chronique',
        'window_months': 'Permanent (saturable)',
        'priority_rank': 2,
        'examples': 'SleepCoach FR, SoulageR, ProcheSoin',
    },
    3: {
        'label': 'Trend culturel',
        'window_months': '6-18',
        'priority_rank': 3,
        'examples': 'ShadowWork FR, DecidR, ZenColere',
    },
}

# B6.1 — Flags that block A-Build decision if not resolved
READINESS_BLOCKERS = {
    'partner_medical': 'partner_confirmed',        # Requires signed clinician
    'rgpd_sante': 'dpia_signed',                   # Requires DPIA completed
    'rgpd_sante_b2b': 'hds_certified_and_dpia',    # V3.1 Cycle 2: requires HDS cert + DPIA + Art.28 clauses
    'market_education': 'education_validated',    # Requires landing/LinkedIn test passed
    'regulatory_risk': 'legal_clearance',         # Requires legal review
}

# B7 — Data freshness
DATA_FRESHNESS_DAYS = 90  # After this, force re-audit before A-Build


# ============================================================
# V3.1 — Validation functions (enforce 7 rules)
# ============================================================

class MoatEngineValidationError(Exception):
    """Raised when V3.1 enforcement rules are violated."""
    pass


def validate_trend_geographic(trend_direction, geo_target, trend_index_avg_12m,
                               trend_variation_pct=None):
    """
    A2 enforcement (raffined post Sonnet cross-review):

    Force STABLE x1.00 if ANY of:
    - Micro-volume: index avg 12m on target geo < 50/100 (artefact on low base)
    - Macro-volume stable: variation_pct abs < 10% AND volume >= 50 (noise on high base)

    Returns (final_trend_direction, guard_flag).
    guard_flag: 'MICRO_VOLUME_GUARD', 'MACRO_STABLE_GUARD', or None.
    """
    if not geo_target:
        return trend_direction, None

    # Micro-volume guard (original A2)
    if trend_index_avg_12m is not None and trend_index_avg_12m < MICRO_VOLUME_THRESHOLD:
        return 'STABLE', 'MICRO_VOLUME_GUARD'

    # Macro-volume stable guard (A2 raffine)
    if (trend_index_avg_12m is not None and trend_variation_pct is not None
            and trend_index_avg_12m >= MICRO_VOLUME_THRESHOLD
            and abs(trend_variation_pct) < MACRO_VOLUME_VARIATION_THRESHOLD):
        return 'STABLE', 'MACRO_STABLE_GUARD'

    return trend_direction, None


def validate_geographic_consistency_tam_trend_som(tam, geo_target):
    """
    A1 enforcement: Check TAM vs geographic target.

    If TAM > national max for target country, probably global TAM applied to national target.
    Returns (is_consistent, flag).
    """
    if not geo_target or geo_target == 'GLOBAL':
        return True, None

    tam_max = TAM_MAX_NATIONAL.get(geo_target, float('inf'))
    if tam > tam_max:
        return False, 'TAM_SUSPECT_GLOBAL'
    return True, None


def validate_forecast_coherence(forecast_m12_mrr, som_solo_monthly):
    """
    A3 enforcement: Ratio forecast M12 / SOM Solo Y1 monthly.

    Returns (status, ratio).
    status: 'COHERENT' (<=3x), 'FLAGGED_INCOHERENT' (3-5x), 'KILLED_INCOHERENT' (>5x), 'UNKNOWN'
    """
    if not som_solo_monthly or som_solo_monthly == 0:
        return 'UNKNOWN', 0.0

    ratio = forecast_m12_mrr / som_solo_monthly

    if ratio > FORECAST_COHERENCE_KILL:
        return 'KILLED_INCOHERENT', ratio
    elif ratio > FORECAST_COHERENCE_FLAG:
        return 'FLAGGED_INCOHERENT', ratio
    else:
        return 'COHERENT', ratio


def generate_score_audit_trail(score_base, trend_multiplier, trend_delta,
                                structural_bonus, flags_applied, score_v3):
    """
    A4 helper: Generate enforced format audit trail string.

    flags_applied: list of tuples (flag_name, value) e.g. [('market_education', -10), ('rgpd_sante', -5)]
    """
    flags_str = ', '.join([f"{name}: {value:+d}" for name, value in flags_applied]) if flags_applied else 'aucun'
    return (
        f"base: {score_base}\n"
        f"+ trend_multiplier: x{trend_multiplier:.2f} ({trend_delta:+d} pts)\n"
        f"+ driver_structurel: {structural_bonus:+d}\n"
        f"+ flags: [{flags_str}]\n"
        f"= score_v3: {score_v3}"
    )


def validate_score_justification(justification, score_base, score_v3,
                                  trend_delta, structural_bonus, flags_total):
    """
    A4 enforcement (raffined post Sonnet cross-review):

    BLOCKING on commit. Raises ValidationError if justification missing, format non-conforming,
    or arithmetic mismatch.

    Strict regex enforcement:
    - trend_multiplier must be one of x1.00, x1.08, x1.15, x0.90 (TREND_MULTIPLIERS values)
    - Arithmetic tolerance = 0 (no ±1 leeway, use round() uniformly)

    MUST be called before any Airtable/dashboard write.
    """
    if not justification or not justification.strip():
        raise MoatEngineValidationError(
            "A4 violation: score_justification is mandatory. "
            "Use generate_score_audit_trail() to create one."
        )

    # Check required format markers
    required_markers = ['base:', 'trend_multiplier:', 'driver_structurel:', 'flags:', 'score_v3:']
    missing = [m for m in required_markers if m not in justification]
    if missing:
        raise MoatEngineValidationError(
            f"A4 violation: score_justification missing required markers: {missing}. "
            f"Expected format: 'base: N\\n+ trend_multiplier: x1.00 (+0 pts)\\n"
            f"+ driver_structurel: +0\\n+ flags: [...]\\n= score_v3: N'"
        )

    # A4 raffine: strict regex for trend_multiplier (only 4 allowed values)
    trend_mult_pattern = r'trend_multiplier:\s*x(1\.00|1\.08|1\.15|0\.90)'
    if not re.search(trend_mult_pattern, justification):
        raise MoatEngineValidationError(
            f"A4 violation: trend_multiplier format non-conforming. "
            f"Must match one of: x1.00, x1.08, x1.15, x0.90 (TREND_MULTIPLIERS values only). "
            f"Use generate_score_audit_trail() for correct format."
        )

    # A4 raffine: strict regex for base and score_v3 (integer)
    base_pattern = r'base:\s*(\d+)'
    v3_pattern = r'score_v3:\s*(\d+)'
    if not (re.search(base_pattern, justification) and re.search(v3_pattern, justification)):
        raise MoatEngineValidationError(
            "A4 violation: base or score_v3 format non-conforming. Expected integer values."
        )

    # Verify arithmetic (tolerance 0 strict)
    expected_v3 = score_base + trend_delta + structural_bonus - flags_total
    # Apply MOAT cap [0, 100] (same as data_backed_score)
    expected_v3_capped = min(max(expected_v3, 0), 100)
    if expected_v3_capped != score_v3:
        raise MoatEngineValidationError(
            f"A4 violation: arithmetic mismatch (tolerance 0). "
            f"base {score_base} + trend {trend_delta:+d} + driver {structural_bonus:+d} - flags {flags_total} "
            f"= {expected_v3} (capped: {expected_v3_capped}), "
            f"but score_v3 committed is {score_v3}. "
            f"Difference inexpliquee de {score_v3 - expected_v3_capped:+d} pts."
        )


def validate_timing_type(timing_type):
    """
    B5 enforcement: Must be 1 (regulatory), 2 (chronic), or 3 (cultural).
    """
    if timing_type is None:
        raise MoatEngineValidationError(
            "B5 violation: timing_type is mandatory. "
            "Use 1 (regulatory driver), 2 (chronic pathology), or 3 (cultural trend)."
        )
    if timing_type not in TIMING_TYPES:
        raise MoatEngineValidationError(
            f"B5 violation: timing_type must be 1, 2, or 3. Got: {timing_type}. "
            f"See TIMING_TYPES for definitions."
        )


def check_readiness_gating(score_v3, active_flags, blockers_resolved):
    """
    B6.1 enforcement (raffined post Sonnet cross-review):

    Force B-Validate if any blocker active, even if score >=75.
    Granularity: SINGLE / MULTIPLE / SEVERE based on count of unresolved blockers.

    active_flags: list of flag names currently active (e.g. ['partner_medical', 'rgpd_sante'])
    blockers_resolved: dict {flag_name: bool} e.g. {'partner_medical': False, 'rgpd_sante': True}

    Returns (decision, readiness_status).
    readiness_status granularity (raffined):
    - 'CLEAR' : no blocker active
    - 'BLOCKED_SINGLE: <flag>' : 1 blocker (1 validation, 2-4 weeks)
    - 'BLOCKED_MULTIPLE: <flags>' : 2 blockers (2 validations, 4-8 weeks)
    - 'BLOCKED_SEVERE: <flags>' : 3+ blockers (chained validations, 2-3+ months, reconsider Watchlist)
    """
    # Identify active UNRESOLVED blockers
    active_blockers = [
        f for f in active_flags
        if f in READINESS_BLOCKERS and not blockers_resolved.get(f, False)
    ]

    # Base decision from score
    if score_v3 >= 75:
        base_decision = 'A -- Build now'
    elif score_v3 >= 60:
        base_decision = 'B -- Validate'
    elif score_v3 >= 45:
        base_decision = 'C -- Watchlist'
    else:
        base_decision = 'D -- Kill'

    # Apply B6.1 gating: force B-Validate if A-eligible but has unresolved blockers
    if active_blockers:
        n = len(active_blockers)
        blockers_str = ', '.join(active_blockers)
        if n == 1:
            status = f'BLOCKED_SINGLE: {blockers_str}'
        elif n == 2:
            status = f'BLOCKED_MULTIPLE: {blockers_str}'
        else:  # 3+
            status = f'BLOCKED_SEVERE: {blockers_str} (reconsider Watchlist, 2-3 months chained validations)'

        # Downgrade A-Build to B-Validate. B-Validate/C-Watchlist/D-Kill unaffected by blocker count.
        if base_decision == 'A -- Build now':
            return 'B -- Validate', status
        return base_decision, status

    return base_decision, 'CLEAR'


def check_data_freshness(data_freshness_date_str, decision):
    """
    B7 enforcement: If data_freshness_date > 90 days AND decision is A-Build, require re-audit.

    Returns (is_fresh, status).
    """
    if not data_freshness_date_str:
        return True, 'NO_FRESHNESS_DATE'  # Not enforced if no date (legacy)

    try:
        freshness_date = datetime.fromisoformat(data_freshness_date_str.replace('Z', '+00:00'))
    except (ValueError, TypeError):
        return False, 'INVALID_DATE_FORMAT'

    # Strip timezone if present for naive comparison
    if freshness_date.tzinfo is not None:
        freshness_date = freshness_date.replace(tzinfo=None)

    age_days = (datetime.now() - freshness_date).days

    if decision.startswith('A') and age_days > DATA_FRESHNESS_DAYS:
        return False, f'STALE_DATA_{age_days}d_REAUDIT_REQUIRED'

    return True, f'fresh_{age_days}d'


# ============================================================
# V3 scoring function (kept for backward compat) — V3.1 wraps it
# ============================================================


def data_backed_score(market_data, review_data, tam_data, angle_strength=3,
                      trend_direction='STABLE', structural_driver=False,
                      # ── V3.1 parameters (backward-compatible, all optional) ──
                      geo_target=None,
                      trend_index_avg_12m=None,
                      trend_variation_pct=None,
                      flags=None,
                      blockers_resolved=None,
                      timing_type=None,
                      data_freshness_date=None):
    """
    Generate a MOAT score backed by real data instead of gut feeling.

    V3: trend multiplier + structural driver bonus.
    V3.1 (optional params):
      - geo_target (FR/BE/CH/DE/etc.) — enables A1 TAM consistency + A2 trend guard
      - trend_index_avg_12m (0-100) — A2 forces STABLE if <50
      - flags (list of str) — explicit flags to apply (see CONDITIONAL_PENALTIES)
      - blockers_resolved (dict) — B6.1 which blockers are resolved
      - timing_type (1/2/3) — B5 opportunity window type
      - data_freshness_date (ISO str) — B7 freshness check

    Returns scores 1-5 for each criterion based on data signals.
    V3.1 adds: score_justification (audit trail), readiness_status, forecast_coherence.
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

    score_base = total  # Save base for audit trail
    v31_flags = []  # Track warnings/overrides for this scoring
    applied_flags = []  # List of (flag_name, value) for audit trail

    # ── V3.1 / A2 (raffined): Trend geographic guard (micro-volume OR macro-stable)
    original_trend = trend_direction
    trend_direction, trend_guard = validate_trend_geographic(
        trend_direction, geo_target, trend_index_avg_12m, trend_variation_pct
    )
    if trend_guard:
        if trend_guard == 'MICRO_VOLUME_GUARD':
            detail = f'Trend forced STABLE: index_avg_12m={trend_index_avg_12m} < {MICRO_VOLUME_THRESHOLD} on geo={geo_target}. Original trend "{original_trend}" overridden.'
        else:  # MACRO_STABLE_GUARD
            detail = f'Trend forced STABLE: volume={trend_index_avg_12m} high but variation={trend_variation_pct:+.1f}% < {MACRO_VOLUME_VARIATION_THRESHOLD}% (noise, not real UP). Original trend "{original_trend}" overridden.'
        v31_flags.append({
            'rule': 'A2',
            'flag': trend_guard,
            'detail': detail,
        })

    # ── V3.1 / A1: TAM-Trend-SOM geographic consistency
    tam_value = tam_data.get('tam', 0)
    tam_ok, tam_flag = validate_geographic_consistency_tam_trend_som(tam_value, geo_target)
    if not tam_ok:
        v31_flags.append({
            'rule': 'A1',
            'flag': tam_flag,
            'detail': f'TAM {tam_value:,.0f} EUR suspect for geo_target={geo_target} (max expected: {TAM_MAX_NATIONAL.get(geo_target, "N/A"):,}). Probably global TAM applied to national target.',
        })

    # V3: Apply trend multiplier (post-A2 override)
    trend_mult = TREND_MULTIPLIERS.get(trend_direction, 1.0)
    total_after_trend = round(total * trend_mult)
    trend_delta = total_after_trend - score_base

    # V3: Apply structural driver bonus
    structural_bonus = 0
    if structural_driver:
        structural_bonus = STRUCTURAL_DRIVER_BONUS

    # ── V3.1: Apply explicit flags (partner_medical, rgpd_sante, etc.)
    flags_total_penalty = 0
    flags_list = flags if flags else []
    for flag_name in flags_list:
        if flag_name in CONDITIONAL_PENALTIES:
            penalty = CONDITIONAL_PENALTIES[flag_name]  # Already negative
            flags_total_penalty += abs(penalty)  # Track absolute for accounting
            applied_flags.append((flag_name, penalty))

    # Compute final score: base * trend + structural - flags (all caps at 100)
    total = total_after_trend + structural_bonus - flags_total_penalty
    total = min(max(total, 0), 100)

    # V3: Calculate Solo Dev SOM
    som_theoretical = tam_data.get('som', 0)
    som_solo_dev = round(som_theoretical * SOLO_DEV_SOM_FACTOR)
    som_solo_monthly = som_solo_dev / 12 if som_solo_dev else 0

    # ── V3.1 / A3: Forecast coherence check (if forecast_m12 provided in tam_data)
    forecast_m12 = tam_data.get('forecast_m12_mrr', None)
    if forecast_m12 is not None and som_solo_monthly:
        coherence_status, coherence_ratio = validate_forecast_coherence(forecast_m12, som_solo_monthly)
        if coherence_status in ('FLAGGED_INCOHERENT', 'KILLED_INCOHERENT'):
            v31_flags.append({
                'rule': 'A3',
                'flag': coherence_status,
                'detail': f'Forecast M12 {forecast_m12:,.0f} vs SOM Solo mensuel {som_solo_monthly:,.0f} = ratio {coherence_ratio:.1f}x.',
                'ratio': round(coherence_ratio, 2),
            })
    else:
        coherence_status = 'UNKNOWN'
        coherence_ratio = 0.0

    # ── V3.1 / A4: Generate audit trail (BLOCKING on commit)
    score_justification = generate_score_audit_trail(
        score_base=score_base,
        trend_multiplier=trend_mult,
        trend_delta=trend_delta,
        structural_bonus=structural_bonus,
        flags_applied=applied_flags,
        score_v3=total,
    )

    # Validate justification against arithmetic (raise if mismatch)
    validate_score_justification(
        justification=score_justification,
        score_base=score_base,
        score_v3=total,
        trend_delta=trend_delta,
        structural_bonus=structural_bonus,
        flags_total=flags_total_penalty,
    )

    # ── V3.1 / B5: Validate timing_type if provided
    if timing_type is not None:
        validate_timing_type(timing_type)

    # ── V3.1 / B6.1: Readiness gating (binary)
    blockers_resolved = blockers_resolved or {}
    decision, readiness_status = check_readiness_gating(
        score_v3=total,
        active_flags=flags_list,
        blockers_resolved=blockers_resolved,
    )

    # ── V3.1 / B7: Data freshness check
    is_fresh, freshness_status = check_data_freshness(data_freshness_date, decision)
    if not is_fresh:
        v31_flags.append({
            'rule': 'B7',
            'flag': freshness_status,
            'detail': f'data_freshness_date: {data_freshness_date}. Re-audit required before A-Build commit.',
        })
        # Downgrade decision to B-Validate if stale
        if decision.startswith('A'):
            decision = 'B -- Validate'
            readiness_status = f'STALE_DATA_FORCED_B_VALIDATE'

    # Store V3 + V3.1 data
    scores['_v3'] = {
        'trend_direction': trend_direction,
        'trend_direction_original': original_trend,
        'trend_multiplier': trend_mult,
        'trend_delta': trend_delta,
        'structural_driver': structural_driver,
        'structural_bonus': structural_bonus,
        'total_before_adjustments': score_base,
        'som_theoretical': som_theoretical,
        'som_solo_dev_y1': som_solo_dev,
    }
    scores['_v31'] = {
        'geo_target': geo_target,
        'trend_index_avg_12m': trend_index_avg_12m,
        'flags_applied': applied_flags,
        'flags_total_penalty': flags_total_penalty,
        'timing_type': timing_type,
        'timing_type_label': TIMING_TYPES.get(timing_type, {}).get('label') if timing_type else None,
        'readiness_status': readiness_status,
        'forecast_coherence_status': coherence_status,
        'forecast_coherence_ratio': round(coherence_ratio, 2) if coherence_ratio else None,
        'data_freshness_date': data_freshness_date,
        'data_freshness_status': freshness_status,
        'v31_flags': v31_flags,
        'score_justification': score_justification,
    }

    return {
        'total': total,
        'max': 100,
        'decision': decision,
        'details': details,
        'raw_scores': scores,
        'score_justification': score_justification,
        'v31_flags': v31_flags,
    }


def run_engine(idea_name, query=None, competitors=None, segment_size=None,
               arpu=None, angle=None, angle_strength=3,
               trend_direction='STABLE', structural_driver=False,
               condition=None, condition_met=False,
               lang='fr', country='fr',
               # ── V3.1 parameters ──
               geo_target=None,
               trend_index_avg_12m=None,
               trend_variation_pct=None,
               flags=None,
               blockers_resolved=None,
               timing_type=None,
               data_freshness_date=None,
               forecast_m12_mrr=None,
               # ── V4 community signal ──
               community_keywords=None,
               community_subreddits=None):
    """
    Run the full MOAT engine pipeline.

    V3.1 (optional, recommended for all new scorings):
      geo_target: 'FR' | 'BE' | 'CH' | 'QC' | 'DE' | 'IT' | 'ES' | 'UK' | 'US' | 'GLOBAL'
      trend_index_avg_12m: 0-100 (Google Trends average for target geo)
      flags: list of CONDITIONAL_PENALTIES keys ['partner_medical', 'rgpd_sante', ...]
      blockers_resolved: dict {'partner_medical': True/False, ...}
      timing_type: 1 (regulatory), 2 (chronic), 3 (cultural)
      data_freshness_date: ISO date string (auto-set to today if None)
      forecast_m12_mrr: projected MRR at month 12 (for A3 coherence check)
    """

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

    # TODO BUG [2026-04-25] : query fallback = idea_name (ex: "BurnoutDetect") → 0 résultat Play Store.
    # Le scraper doit chercher sur l'INTENTION utilisateur, pas le nom de l'app.
    # Fix : passer --query "burnout stress test" / "migraine journal tracker" lors du run.
    # Correction auto à implémenter post-ChronoFacture : normaliser idea_name en mots-clés
    # (split camelCase, retirer suffixes FR/Pro/App, traduire si nécessaire).
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

    # V3.1: auto-set data_freshness_date to today if not provided
    if data_freshness_date is None:
        data_freshness_date = datetime.now().date().isoformat()

    # V3.1: merge forecast_m12_mrr into tam_data for A3 coherence check
    if forecast_m12_mrr is not None:
        tam_data = dict(tam_data)  # copy to avoid mutation
        tam_data['forecast_m12_mrr'] = forecast_m12_mrr

    try:
        scoring = data_backed_score(
            market_data, review_data, tam_data, angle_strength,
            trend_direction=trend_direction,
            structural_driver=structural_driver,
            geo_target=geo_target,
            trend_index_avg_12m=trend_index_avg_12m,
            trend_variation_pct=trend_variation_pct,
            flags=flags,
            blockers_resolved=blockers_resolved,
            timing_type=timing_type,
            data_freshness_date=data_freshness_date,
        )
    except MoatEngineValidationError as e:
        print(f"\n  !! V3.1 VALIDATION ERROR !! ")
        print(f"  {e}")
        report['v31_validation_error'] = str(e)
        return report

    # V3.1: Display V3.1 flags if any
    v31_flags = scoring.get('v31_flags', [])
    if v31_flags:
        print(f"\n  -- V3.1 FLAGS DECTECTED --")
        for flag in v31_flags:
            print(f"  [{flag['rule']}] {flag['flag']}: {flag['detail']}")

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

    # ── PHASE 4c: Community Signal (V4 — optionnel, --community-signal) ──
    community_data = None
    if community_keywords and modules.get('community_signal'):
        print(f"\n{'='*60}")
        print(f"  PHASE 4c: Community Signal (données réelles Reddit FR)")
        print(f"{'='*60}")
        try:
            community_data = run_community_signal(
                keywords=community_keywords,
                idea_name=idea_name,
                subreddits=community_subreddits,
                active_flags=flags or [],  # Q2 : passe les flags V3.1 actifs
                save=False,   # On sauvegarde dans le rapport engine global
                quiet=False,
            )
            report['phases']['community_signal'] = community_data

            # Appliquer l'ajustement au score V3 (+3/+1/0/-3)
            adj = community_data.get('adjustment', 0)
            if adj != 0:
                old_score = scoring['total']
                scoring['total'] = min(max(scoring['total'] + adj, 0), 100)
                report['phases']['scoring']['total'] = scoring['total']

                # Q3 : Détection score saturé (pas de changement réel malgré ajustement)
                if old_score == scoring['total']:
                    print(f"\n  [V4] Community Signal ajustement : {adj:+d} pts")
                    print(f"       Score V3 : {old_score} → {scoring['total']}")
                    print(f"       [NOTE] Score saturé — ajustement sans impact réel.")
                    print(f"       (Score était déjà à {old_score}/100, cappé à 100)")
                    print(f"       Le Community Signal confirme la demande mais ne change pas le rang.")
                    community_data['score_saturation_note'] = (
                        f"Ajustement {adj:+d} sans impact : score déjà à {old_score}/100 "
                        f"(cap 100). Community Signal confirmatoire uniquement."
                    )
                else:
                    print(f"\n  [V4] Community Signal ajustement : {adj:+d} pts")
                    print(f"       Score V3 : {old_score} → {scoring['total']}")
            else:
                if adj == 0 and community_data.get('adjustment_override_reason'):
                    print(f"\n  [V4] Community Signal ajustement : 0 (neutralisé)")
                    print(f"       Score V3 inchangé : {scoring['total']}")

        except Exception as e:
            print(f"\n  [community_signal] Erreur : {str(e)[:80]}")
            print(f"  Scoring V3 non modifié.")
    elif community_keywords and not modules.get('community_signal'):
        print(f"\n  [!] --community-signal demandé mais module non disponible.")
        print(f"      Vérifier : pip install praw requests beautifulsoup4")

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
    # V4 community signal
    if community_data:
        cs_score = community_data.get('community_signal_score', 0)
        cs_verdict = community_data.get('verdict', '')
        cs_adj = community_data.get('adjustment', 0)
        if cs_verdict == 'FORT':
            signals.append(f"[+] Community Signal FORT ({cs_score}/100) — demande organique confirmée Reddit FR")
        elif cs_verdict == 'MOYEN':
            signals.append(f"[~] Community Signal MOYEN ({cs_score}/100) — signal présent mais modéré")

    risks = []
    if market_data.get('total_installs', 0) < 100_000:
        risks.append("[-] Marche petit ou naissant (peu d'installs)")
    if review_data.get('avg_negative_ratio', 0) < 20:
        risks.append("[-] Faible frustration = concurrence de qualite")
    if tam_data.get('som', 0) / 12 < 1000:
        risks.append("[-] Revenue potentiel faible")
    # V4 community signal risk
    if community_data and community_data.get('verdict') == 'INEXISTANT':
        risks.append("[-] Community Signal INEXISTANT — marché éducatif ou niche très fermée")

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

    # ── V3.1 display ──
    v31 = scoring.get('raw_scores', {}).get('_v31', {})
    if v31:
        print(f"\n  -- V3.1 --")
        if v31.get('geo_target'):
            print(f"  GEO TARGET     : {v31['geo_target']}")
        if v31.get('trend_index_avg_12m') is not None:
            print(f"  TREND INDEX    : {v31['trend_index_avg_12m']}/100 (moyenne 12m cible)")
        if v31.get('flags_applied'):
            flags_str = ', '.join([f"{n}({v:+d})" for n, v in v31['flags_applied']])
            print(f"  FLAGS          : {flags_str}")
        if v31.get('timing_type'):
            print(f"  TIMING TYPE    : {v31['timing_type']} -- {v31['timing_type_label']}")
        if v31.get('readiness_status') and v31['readiness_status'] != 'CLEAR':
            print(f"  READINESS      : {v31['readiness_status']}")
        if v31.get('forecast_coherence_status') and v31['forecast_coherence_status'] != 'UNKNOWN':
            ratio = v31.get('forecast_coherence_ratio', 0)
            print(f"  FORECAST COHER : {v31['forecast_coherence_status']} (ratio {ratio}x)")
        if v31.get('data_freshness_status'):
            print(f"  DATA FRESHNESS : {v31['data_freshness_status']}")

        # Audit trail (A4)
        if v31.get('score_justification'):
            print(f"\n  -- SCORE AUDIT TRAIL (A4) --")
            for line in v31['score_justification'].split('\n'):
                print(f"    {line}")

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
    parser = argparse.ArgumentParser(description="MOAT Engine V3.1 -- Full Pipeline Analysis")
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

    # ── V3.1 parameters ──
    parser.add_argument("--geo-target", choices=GEOGRAPHIC_TARGETS,
                       help="V3.1 A1/A2: marche cible geographique (FR/BE/CH/QC/DE/IT/ES/UK/US/GLOBAL)")
    parser.add_argument("--trend-index-avg", type=float, metavar='0-100',
                       help="V3.1 A2: moyenne 12m de l'index Google Trends sur marche cible. Si <50 -> STABLE force")
    parser.add_argument("--trend-variation-pct", type=float, metavar='%',
                       help="V3.1 A2 raffine: variation %% du trend sur 12m. Si abs <10%% ET volume>=50 -> STABLE force (macro-stable guard)")
    parser.add_argument("--flags", help="V3.1: flags explicites (virgule) ex: 'partner_medical,rgpd_sante'")
    parser.add_argument("--blockers-resolved", help="V3.1 B6.1: blockers resolus (virgule) ex: 'partner_medical'")
    parser.add_argument("--timing-type", type=int, choices=[1, 2, 3],
                       help="V3.1 B5: 1=reglementaire, 2=pathologie chronique, 3=trend culturel")
    parser.add_argument("--forecast-m12-mrr", type=float,
                       help="V3.1 A3: MRR projete M12 (pour coherence check vs SOM Solo)")
    parser.add_argument("--data-freshness-date", default=None,
                       help="V3.1 B7: date ISO YYYY-MM-DD (defaut: aujourd'hui). Si >90j et A-Build -> re-audit force")

    # ── V4 community signal ──
    parser.add_argument("--community-signal", metavar='KEYWORDS',
                       help="V4: mots-clés community signal Reddit FR (virgule). "
                            "Ex: 'burn-out,stress travail,epuisement professionnel'. "
                            "Ajoute +-3 pts au score selon la demande organique détectée.")
    parser.add_argument("--community-subreddits", metavar='SUBS',
                       help="V4: subreddits custom (virgule). Défaut: france,sante,travail,medecine,emploi")

    # ── V5 build blueprint ──
    parser.add_argument("--design-prompt", action="store_true",
                       help="V5: génère data/blueprints/{slug}/design_prompt.md après le run. "
                            "Lit le rapport engine produit et applique FRUSTRATION_TO_GUARDRAIL.")
    parser.add_argument("--style-note", metavar='NOTE',
                       help="V5: note de direction visuelle pour le prompt Claude Design. "
                            "Ex: 'Dark mode premium souhaité'. Combiné avec --design-prompt.")

    args = parser.parse_args()

    # Parse flags list
    flags_list = [f.strip() for f in args.flags.split(',')] if args.flags else None

    # Parse blockers_resolved
    blockers_resolved = None
    if args.blockers_resolved:
        blockers_resolved = {f.strip(): True for f in args.blockers_resolved.split(',')}

    # Parse community signal keywords
    community_keywords = None
    if args.community_signal:
        community_keywords = [kw.strip() for kw in args.community_signal.split(',')]

    # Parse community subreddits
    community_subreddits = None
    if args.community_subreddits:
        community_subreddits = [s.strip() for s in args.community_subreddits.split(',')]

    report = run_engine(
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
        # V3.1
        geo_target=args.geo_target,
        trend_index_avg_12m=args.trend_index_avg,
        trend_variation_pct=args.trend_variation_pct,
        flags=flags_list,
        blockers_resolved=blockers_resolved,
        timing_type=args.timing_type,
        data_freshness_date=args.data_freshness_date,
        forecast_m12_mrr=args.forecast_m12_mrr,
        # V4
        community_keywords=community_keywords,
        community_subreddits=community_subreddits,
    )

    # ── V5: Build Blueprint (--design-prompt) ──────────────────────────────────
    if args.design_prompt and report:
        verdict = report.get('verdict', {})
        if verdict.get('bodyguard_killed'):
            print("\n  [design-prompt] Skipped — idée éliminée par le bodyguard.")
        else:
            try:
                from build_blueprint import run_build_blueprint
                # Le rapport engine vient d'être sauvegardé — find_latest_json le trouvera
                print("\n" + "="*60)
                print("  V5: Build Blueprint -- Génération du prompt Claude Design")
                print("="*60)
                bp = run_build_blueprint(
                    idea_name=args.idea,
                    style_note=args.style_note,
                    quiet=False,
                )
                print(f"  Prompt prêt : {bp['output_path']}")
            except ImportError:
                print("\n  [design-prompt] Module build_blueprint.py non trouvé dans scripts/")
            except Exception as e:
                print(f"\n  [design-prompt] Erreur : {str(e)[:80]}")


if __name__ == "__main__":
    main()
