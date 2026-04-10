#!/usr/bin/env python3
"""
MOAT App Discovery System -- TAM/SAM/SOM Market Sizer

Calculates Total Addressable Market, Serviceable Addressable Market,
and Serviceable Obtainable Market for mobile app opportunities.

Combines bottom-up and top-down approaches with pre-built French market
data for common niches.

Usage:
    python market_sizer.py --segment "insomniacs FR" --users 20000000 --arpu 60 --capture 0.02
    python market_sizer.py --segment "coaches sportifs" --users 50000 --arpu 120 --capture 0.05
    python market_sizer.py --preset insomnia_fr
    python market_sizer.py --preset freelance_fr

Interactive mode if no args provided.
"""

import argparse
import math
import sys


# ---------------------------------------------------------------------------
# Pre-built market presets (France-focused)
# ---------------------------------------------------------------------------

PRESETS = {
    "insomnia_fr": {
        "segment": "Insomniacs France",
        "total_users": 20_000_000,        # ~1/3 of population
        "arpu": 60,                        # EUR/year
        "top_down_market": 2_500_000_000,  # EUR global sleep-aid market
        "top_down_pct": 0.03,              # 3% France mobile niche
        "geo_filter": 0.85,               # % in metro areas with smartphone
        "lang_filter": 1.0,               # French speakers
        "platform_filter": 0.55,          # Android France ~55%
        "pricing_filter": 0.10,           # Willing to pay for sleep app
        "competition": "high",
        "differentiation": "medium",
        "distribution": "medium",
    },
    "freelance_fr": {
        "segment": "Freelances France",
        "total_users": 4_000_000,
        "arpu": 120,
        "top_down_market": 800_000_000,
        "top_down_pct": 0.05,
        "geo_filter": 0.90,
        "lang_filter": 1.0,
        "platform_filter": 0.55,
        "pricing_filter": 0.25,
        "competition": "high",
        "differentiation": "medium",
        "distribution": "medium",
    },
    "artisans_fr": {
        "segment": "Artisans France",
        "total_users": 1_300_000,
        "arpu": 150,
        "top_down_market": 300_000_000,
        "top_down_pct": 0.08,
        "geo_filter": 0.90,
        "lang_filter": 1.0,
        "platform_filter": 0.55,
        "pricing_filter": 0.20,
        "competition": "medium",
        "differentiation": "medium",
        "distribution": "medium",
    },
    "coaches_sportifs_fr": {
        "segment": "Coaches Sportifs France",
        "total_users": 50_000,
        "arpu": 120,
        "top_down_market": 50_000_000,
        "top_down_pct": 0.10,
        "geo_filter": 0.95,
        "lang_filter": 1.0,
        "platform_filter": 0.55,
        "pricing_filter": 0.30,
        "competition": "low",
        "differentiation": "high",
        "distribution": "medium",
    },
    "health_wellness_fr": {
        "segment": "Health/Wellness France",
        "total_users": 15_000_000,
        "arpu": 72,
        "top_down_market": 5_000_000_000,
        "top_down_pct": 0.02,
        "geo_filter": 0.85,
        "lang_filter": 1.0,
        "platform_filter": 0.55,
        "pricing_filter": 0.12,
        "competition": "high",
        "differentiation": "low",
        "distribution": "medium",
    },
    "pet_owners_fr": {
        "segment": "Pet Owners France",
        "total_users": 30_000_000,
        "arpu": 48,
        "top_down_market": 1_500_000_000,
        "top_down_pct": 0.02,
        "geo_filter": 0.85,
        "lang_filter": 1.0,
        "platform_filter": 0.55,
        "pricing_filter": 0.08,
        "competition": "medium",
        "differentiation": "medium",
        "distribution": "medium",
    },
    "coproprietaires_fr": {
        "segment": "Coproprietaires France",
        "total_users": 10_000_000,
        "arpu": 96,
        "top_down_market": 600_000_000,
        "top_down_pct": 0.04,
        "geo_filter": 0.90,
        "lang_filter": 1.0,
        "platform_filter": 0.55,
        "pricing_filter": 0.15,
        "competition": "low",
        "differentiation": "high",
        "distribution": "low",
    },
}


# ---------------------------------------------------------------------------
# Competition / differentiation / distribution scoring
# ---------------------------------------------------------------------------

COMPETITION_FACTOR = {"low": 0.05, "medium": 0.03, "high": 0.015}
DIFFERENTIATION_FACTOR = {"low": 0.8, "medium": 1.0, "high": 1.3}
DISTRIBUTION_FACTOR = {"low": 0.7, "medium": 1.0, "high": 1.4}


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------

def fmt_eur(value):
    """Format a number as EUR with thousands separator (ASCII-safe)."""
    if value >= 1_000_000:
        return "{:,.0f} EUR ({:.1f}M EUR)".format(value, value / 1_000_000)
    elif value >= 1_000:
        return "{:,.0f} EUR ({:.0f}K EUR)".format(value, value / 1_000)
    else:
        return "{:,.0f} EUR".format(value)


def fmt_pct(value):
    """Format a float as a percentage string."""
    return "{:.2f}%".format(value * 100)


def separator(char="-", width=70):
    """Return a horizontal separator line."""
    return char * width


# ---------------------------------------------------------------------------
# Core calculations
# ---------------------------------------------------------------------------

def calc_tam_bottom_up(users, arpu):
    """TAM bottom-up: total potential users * ARPU."""
    return users * arpu


def calc_tam_top_down(market_revenue, niche_pct):
    """TAM top-down: total market revenue * niche percentage."""
    return market_revenue * niche_pct


def calc_sam(tam, geo, lang, platform, pricing):
    """SAM: TAM filtered by geography, language, platform, pricing."""
    return tam * geo * lang * platform * pricing


def calc_som(sam, capture_rate):
    """SOM: SAM * realistic capture rate."""
    return sam * capture_rate


def calc_adjusted_capture(base_capture, competition, differentiation, distribution):
    """Adjust capture rate based on qualitative factors."""
    comp = COMPETITION_FACTOR.get(competition, 0.03)
    diff = DIFFERENTIATION_FACTOR.get(differentiation, 1.0)
    dist = DISTRIBUTION_FACTOR.get(distribution, 1.0)
    # Base capture capped between comp floor and 10%
    adjusted = base_capture * diff * dist
    adjusted = max(comp, min(adjusted, 0.10))
    return adjusted


def months_to_mrr(target_mrr, som_monthly, growth_rate=0.10):
    """
    Estimate months to reach a target MRR.

    Assumes starting at som_monthly * 0.1 (10% of theoretical SOM/12)
    and growing at growth_rate per month.

    Returns number of months, or None if unreachable within 60 months.
    """
    if som_monthly <= 0:
        return None

    current = som_monthly * 0.10  # start at 10% of monthly SOM
    if current <= 0:
        return None
    if current >= target_mrr:
        return 1

    for month in range(1, 61):
        current *= (1 + growth_rate)
        if current >= target_mrr:
            return month

    return None  # unreachable within 5 years


def viability_verdict(som_yearly):
    """Return a verdict based on SOM yearly revenue."""
    if som_yearly >= 120_000:
        return "Viable micro-SaaS  --  Strong potential for solo/indie dev"
    elif som_yearly >= 60_000:
        return "Viable micro-SaaS  --  Sustainable with lean operations"
    elif som_yearly >= 20_000:
        return "Needs scale  --  Side project viable, needs growth to sustain"
    else:
        return "Too small  --  Niche too narrow or ARPU too low at this capture"


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def generate_report(params):
    """Generate the full TAM/SAM/SOM report and return it as a string."""
    segment = params["segment"]
    users = params["total_users"]
    arpu = params["arpu"]
    capture = params.get("capture_rate", 0.02)

    # Top-down values (optional)
    td_market = params.get("top_down_market", 0)
    td_pct = params.get("top_down_pct", 0)

    # SAM filters
    geo = params.get("geo_filter", 0.85)
    lang = params.get("lang_filter", 1.0)
    platform = params.get("platform_filter", 0.55)
    pricing = params.get("pricing_filter", 0.15)

    # Qualitative factors
    competition = params.get("competition", "medium")
    differentiation = params.get("differentiation", "medium")
    distribution = params.get("distribution", "medium")

    # --- TAM ---
    tam_bu = calc_tam_bottom_up(users, arpu)
    tam_td = calc_tam_top_down(td_market, td_pct) if td_market > 0 else None

    # --- SAM (using bottom-up TAM) ---
    sam = calc_sam(tam_bu, geo, lang, platform, pricing)

    # --- SOM ---
    adjusted_capture = calc_adjusted_capture(capture, competition,
                                             differentiation, distribution)
    som = calc_som(sam, adjusted_capture)
    som_monthly = som / 12.0

    # Revenue projections at different capture rates
    captures = [0.01, 0.02, 0.05]
    projections = []
    for c in captures:
        adj = calc_adjusted_capture(c, competition, differentiation,
                                    distribution)
        rev_year = sam * adj
        rev_month = rev_year / 12.0
        projections.append((c, adj, rev_year, rev_month))

    # Time to MRR milestones
    milestones = [1_000, 5_000, 10_000]
    milestone_months = []
    for target in milestones:
        m = months_to_mrr(target, som_monthly)
        milestone_months.append((target, m))

    # Break-even analysis (assume typical indie costs)
    monthly_costs = [500, 1_000, 2_000]

    # --- Build report ---
    lines = []
    lines.append("")
    lines.append(separator("=", 70))
    lines.append("  TAM / SAM / SOM  --  Market Sizing Report")
    lines.append(separator("=", 70))
    lines.append("")
    lines.append("  Segment:  {}".format(segment))
    lines.append("")

    # TAM section
    lines.append(separator("-", 70))
    lines.append("  1. TAM  --  Total Addressable Market")
    lines.append(separator("-", 70))
    lines.append("")
    lines.append("  Bottom-up method:")
    lines.append("    Potential users:     {:>15,}".format(users))
    lines.append("    ARPU (EUR/year):     {:>15,}".format(arpu))
    lines.append("    TAM (bottom-up):     {:>15}".format(fmt_eur(tam_bu)))
    lines.append("")
    if tam_td is not None:
        lines.append("  Top-down method:")
        lines.append("    Global market:       {:>15}".format(
            fmt_eur(td_market)))
        lines.append("    Niche share:         {:>15}".format(
            fmt_pct(td_pct)))
        lines.append("    TAM (top-down):      {:>15}".format(
            fmt_eur(tam_td)))
        lines.append("")
        ratio = tam_td / tam_bu if tam_bu > 0 else 0
        if 0.5 <= ratio <= 2.0:
            lines.append("    -> Methods converge (ratio {:.2f}x)"
                         " -- Good confidence".format(ratio))
        else:
            lines.append("    -> Methods diverge (ratio {:.2f}x)"
                         " -- Investigate assumptions".format(ratio))
        lines.append("")

    # SAM section
    lines.append(separator("-", 70))
    lines.append("  2. SAM  --  Serviceable Addressable Market")
    lines.append(separator("-", 70))
    lines.append("")
    lines.append("  Filters applied to bottom-up TAM:")
    lines.append("    Geography:           {:>15}".format(fmt_pct(geo)))
    lines.append("    Language:            {:>15}".format(fmt_pct(lang)))
    lines.append("    Platform (mobile):   {:>15}".format(fmt_pct(platform)))
    lines.append("    Pricing willingness: {:>15}".format(fmt_pct(pricing)))
    lines.append("    Combined filter:     {:>15}".format(
        fmt_pct(geo * lang * platform * pricing)))
    lines.append("")
    lines.append("    SAM:                 {:>15}".format(fmt_eur(sam)))
    lines.append("")

    # SOM section
    lines.append(separator("-", 70))
    lines.append("  3. SOM  --  Serviceable Obtainable Market (Year 1)")
    lines.append(separator("-", 70))
    lines.append("")
    lines.append("  Qualitative adjustments:")
    lines.append("    Competition:         {:>15}".format(competition))
    lines.append("    Differentiation:     {:>15}".format(differentiation))
    lines.append("    Distribution:        {:>15}".format(distribution))
    lines.append("")
    lines.append("    Input capture rate:  {:>15}".format(fmt_pct(capture)))
    lines.append("    Adjusted capture:    {:>15}".format(
        fmt_pct(adjusted_capture)))
    lines.append("")
    lines.append("    SOM (yearly):        {:>15}".format(fmt_eur(som)))
    lines.append("    SOM (monthly):       {:>15}".format(
        fmt_eur(som_monthly)))
    lines.append("")

    # Revenue projections
    lines.append(separator("-", 70))
    lines.append("  4. Revenue Projections at Different Capture Rates")
    lines.append(separator("-", 70))
    lines.append("")
    lines.append("  {:>8}  {:>10}  {:>16}  {:>14}".format(
        "Input %", "Adjusted", "Yearly EUR", "Monthly EUR"))
    lines.append("  {:>8}  {:>10}  {:>16}  {:>14}".format(
        "--------", "----------", "----------------", "--------------"))
    for (c, adj, rev_y, rev_m) in projections:
        lines.append("  {:>8}  {:>10}  {:>16}  {:>14}".format(
            fmt_pct(c), fmt_pct(adj),
            "{:,.0f}".format(rev_y), "{:,.0f}".format(rev_m)))
    lines.append("")

    # Indie benchmarks
    lines.append("  Indie app benchmarks:")
    lines.append("    Micro-SaaS sweet spot:  5,000 - 50,000 EUR MRR")
    lines.append("    Ramen profitable:       ~3,000 EUR MRR")
    lines.append("    Sustainable solo dev:    ~5,000 EUR MRR")
    lines.append("")

    # Break-even
    lines.append(separator("-", 70))
    lines.append("  5. Break-Even Analysis")
    lines.append(separator("-", 70))
    lines.append("")
    lines.append("  {:>18}  {:>14}  {:>12}".format(
        "Monthly costs", "Capture needed", "Feasible?"))
    lines.append("  {:>18}  {:>14}  {:>12}".format(
        "------------------", "--------------", "------------"))
    for cost in monthly_costs:
        yearly_cost = cost * 12
        needed_capture = yearly_cost / sam if sam > 0 else float("inf")
        feasible = "YES" if needed_capture <= 0.05 else (
            "STRETCH" if needed_capture <= 0.10 else "NO")
        lines.append("  {:>15,} EUR  {:>14}  {:>12}".format(
            cost, fmt_pct(needed_capture), feasible))
    lines.append("")

    # Time to MRR milestones
    lines.append(separator("-", 70))
    lines.append("  6. Time to MRR Milestones (10% MoM growth assumption)")
    lines.append(separator("-", 70))
    lines.append("")
    for (target, m) in milestone_months:
        if m is not None:
            lines.append("    {:>6,} EUR MRR:  ~{} months".format(target, m))
        else:
            lines.append("    {:>6,} EUR MRR:  >60 months (unlikely)".format(
                target))
    lines.append("")

    # Verdict
    verdict = viability_verdict(som)
    lines.append(separator("=", 70))
    lines.append("  VERDICT:  {}".format(verdict))
    lines.append(separator("=", 70))
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Interactive mode
# ---------------------------------------------------------------------------

def ask_float(prompt, default=None):
    """Prompt user for a float value with optional default."""
    suffix = " [{}]: ".format(default) if default is not None else ": "
    while True:
        raw = input(prompt + suffix).strip()
        if not raw and default is not None:
            return float(default)
        try:
            return float(raw)
        except ValueError:
            print("  -> Please enter a valid number.")


def ask_int(prompt, default=None):
    """Prompt user for an integer value with optional default."""
    suffix = " [{}]: ".format(default) if default is not None else ": "
    while True:
        raw = input(prompt + suffix).strip()
        if not raw and default is not None:
            return int(default)
        try:
            return int(raw)
        except ValueError:
            print("  -> Please enter a valid integer.")


def ask_choice(prompt, choices, default=None):
    """Prompt user to pick from a list of choices."""
    choices_str = "/".join(choices)
    suffix = " ({}) [{}]: ".format(choices_str, default) if default else \
             " ({}): ".format(choices_str)
    while True:
        raw = input(prompt + suffix).strip().lower()
        if not raw and default:
            return default
        if raw in choices:
            return raw
        print("  -> Choose one of: {}".format(choices_str))


def interactive_mode():
    """Run the calculator interactively, step by step."""
    print("")
    print(separator("=", 70))
    print("  TAM/SAM/SOM Market Sizer  --  Interactive Mode")
    print(separator("=", 70))
    print("")

    # Check if user wants a preset
    print("  Available presets:")
    for key, val in PRESETS.items():
        print("    {:<25} ({:>12,} users, {:>3} EUR ARPU)".format(
            key, val["total_users"], val["arpu"]))
    print("")

    use_preset = input("  Use a preset? (enter name or press Enter to skip): "
                       ).strip().lower()

    if use_preset and use_preset in PRESETS:
        params = dict(PRESETS[use_preset])
        # Allow override of capture rate
        capture = ask_float("  Capture rate (e.g. 0.02 for 2%)", 0.02)
        params["capture_rate"] = capture
        return params

    # Manual entry
    print("")
    print("  -- Step 1: Define your segment --")
    segment = input("  Segment name: ").strip() or "Custom segment"

    print("")
    print("  -- Step 2: TAM inputs --")
    users = ask_int("  Number of potential users", 1_000_000)
    arpu = ask_float("  Average revenue per user per year (EUR)", 60)

    print("")
    print("  -- Step 2b: Top-down comparison (optional) --")
    td_market = ask_float("  Total global market revenue (EUR, 0 to skip)", 0)
    td_pct = 0
    if td_market > 0:
        td_pct = ask_float("  Your niche share of that market (e.g. 0.03)", 0.03)

    print("")
    print("  -- Step 3: SAM filters --")
    geo = ask_float("  Geography filter (0-1)", 0.85)
    lang = ask_float("  Language filter (0-1)", 1.0)
    platform = ask_float("  Platform filter (Android/iOS share, 0-1)", 0.55)
    pricing = ask_float("  Pricing willingness filter (0-1)", 0.15)

    print("")
    print("  -- Step 4: SOM factors --")
    capture = ask_float("  Base capture rate (e.g. 0.02 for 2%)", 0.02)
    competition = ask_choice("  Competition level", ["low", "medium", "high"],
                             "medium")
    differentiation = ask_choice("  Differentiation",
                                 ["low", "medium", "high"], "medium")
    distribution = ask_choice("  Distribution capability",
                              ["low", "medium", "high"], "medium")

    return {
        "segment": segment,
        "total_users": users,
        "arpu": arpu,
        "top_down_market": td_market,
        "top_down_pct": td_pct,
        "geo_filter": geo,
        "lang_filter": lang,
        "platform_filter": platform,
        "pricing_filter": pricing,
        "capture_rate": capture,
        "competition": competition,
        "differentiation": differentiation,
        "distribution": distribution,
    }


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def build_parser():
    """Build the argparse parser."""
    parser = argparse.ArgumentParser(
        description="TAM/SAM/SOM Market Sizer for mobile app opportunities.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python market_sizer.py --preset insomnia_fr\n"
            "  python market_sizer.py --segment \"insomniacs FR\""
            " --users 20000000 --arpu 60 --capture 0.02\n"
            "  python market_sizer.py  (interactive mode)\n"
            "\nAvailable presets: " + ", ".join(sorted(PRESETS.keys()))
        )
    )

    parser.add_argument("--preset", type=str, default=None,
                        help="Use a pre-built market preset"
                             " (e.g. insomnia_fr, freelance_fr)")
    parser.add_argument("--segment", type=str, default=None,
                        help="Segment name / description")
    parser.add_argument("--users", type=int, default=None,
                        help="Number of potential users")
    parser.add_argument("--arpu", type=float, default=None,
                        help="Average Revenue Per User per year (EUR)")
    parser.add_argument("--capture", type=float, default=0.02,
                        help="Base capture rate (default: 0.02 = 2%%)")

    # SAM filters
    parser.add_argument("--geo", type=float, default=0.85,
                        help="Geography filter 0-1 (default: 0.85)")
    parser.add_argument("--lang", type=float, default=1.0,
                        help="Language filter 0-1 (default: 1.0)")
    parser.add_argument("--platform", type=float, default=0.55,
                        help="Platform filter 0-1 (default: 0.55)")
    parser.add_argument("--pricing", type=float, default=0.15,
                        help="Pricing willingness filter 0-1 (default: 0.15)")

    # Qualitative factors
    parser.add_argument("--competition", type=str, default="medium",
                        choices=["low", "medium", "high"],
                        help="Competition level (default: medium)")
    parser.add_argument("--differentiation", type=str, default="medium",
                        choices=["low", "medium", "high"],
                        help="Differentiation level (default: medium)")
    parser.add_argument("--distribution", type=str, default="medium",
                        choices=["low", "medium", "high"],
                        help="Distribution capability (default: medium)")

    # Top-down
    parser.add_argument("--td-market", type=float, default=0,
                        help="Total global market revenue for top-down"
                             " (EUR, default: 0 = skip)")
    parser.add_argument("--td-pct", type=float, default=0.03,
                        help="Niche percentage of global market"
                             " (default: 0.03)")

    # Output
    parser.add_argument("--list-presets", action="store_true",
                        help="List all available presets and exit")

    return parser


def main():
    """Main entry point."""
    parser = build_parser()
    args = parser.parse_args()

    # List presets
    if args.list_presets:
        print("")
        print("Available presets:")
        print(separator("-", 60))
        for key, val in sorted(PRESETS.items()):
            print("  {:<25} {:>12,} users  {:>4} EUR ARPU".format(
                key, val["total_users"], val["arpu"]))
        print("")
        sys.exit(0)

    # Preset mode
    if args.preset:
        preset_key = args.preset.lower().replace("-", "_").replace(" ", "_")
        if preset_key not in PRESETS:
            print("Error: Unknown preset '{}'. Use --list-presets to see"
                  " available options.".format(args.preset))
            sys.exit(1)
        params = dict(PRESETS[preset_key])
        params["capture_rate"] = args.capture
        # Allow CLI overrides even with preset
        if args.users is not None:
            params["total_users"] = args.users
        if args.arpu is not None:
            params["arpu"] = args.arpu
        if args.segment is not None:
            params["segment"] = args.segment

    # Custom segment mode
    elif args.segment and args.users is not None and args.arpu is not None:
        params = {
            "segment": args.segment,
            "total_users": args.users,
            "arpu": args.arpu,
            "top_down_market": args.td_market,
            "top_down_pct": args.td_pct,
            "geo_filter": args.geo,
            "lang_filter": args.lang,
            "platform_filter": args.platform,
            "pricing_filter": args.pricing,
            "capture_rate": args.capture,
            "competition": args.competition,
            "differentiation": args.differentiation,
            "distribution": args.distribution,
        }

    # Interactive mode (no args or incomplete args)
    else:
        # Check if any args were partially provided
        has_partial = (args.segment is not None or args.users is not None
                       or args.arpu is not None)
        if has_partial:
            print("Error: For custom segments, all of --segment, --users,"
                  " and --arpu are required.")
            print("       Or use --preset for pre-built data.")
            sys.exit(1)

        try:
            params = interactive_mode()
        except (KeyboardInterrupt, EOFError):
            print("\n\nAborted.")
            sys.exit(0)

    # Generate and print report
    report = generate_report(params)
    print(report)


if __name__ == "__main__":
    main()
