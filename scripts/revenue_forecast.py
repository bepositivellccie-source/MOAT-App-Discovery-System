#!/usr/bin/env python3
"""
MOAT App Discovery System -- Revenue Forecast

Previsionnel de rentabilite sur 12 mois.
Base sur des benchmarks reels du marche mobile (indie/micro-SaaS).

Usage:
    python revenue_forecast.py --idea "SleepCoach FR" --segment-size 20000000 --price 6.99 --model freemium
    python revenue_forecast.py --idea "DoctAfter" --segment-size 40000000 --price 2.99 --model freemium
    python revenue_forecast.py --idea "CoachCRM" --segment-size 50000 --price 9.99 --model freemium
    python revenue_forecast.py --preset sleepcoach
    python revenue_forecast.py --preset doctafter
"""

import argparse
import json
import os
import sys
from datetime import datetime


# ── Benchmarks industrie reels ──
# Sources: RevenueCat State of Subscription Apps 2025, Sensor Tower, data.ai
BENCHMARKS = {
    'install_to_trial': {
        'low': 0.02,      # 2% des installs essaient le premium
        'medium': 0.05,   # 5%
        'high': 0.10,     # 10% (apps tres ciblees)
    },
    'trial_to_paid': {
        'low': 0.15,      # 15% des trials convertissent
        'medium': 0.30,   # 30% — benchmark RevenueCat 2025
        'high': 0.50,     # 50% (apps a forte valeur percue)
    },
    'monthly_churn': {
        'low': 0.04,      # 4%/mois — excellent (apps therapeutiques)
        'medium': 0.08,   # 8%/mois — standard
        'high': 0.15,     # 15%/mois — mauvais
    },
    'organic_install_growth': {
        'low': 0.05,      # 5%/mois — ASO seul
        'medium': 0.15,   # 15%/mois — ASO + content + referral
        'high': 0.30,     # 30%/mois — viralite + paid
    },
    'arpu_annual_multiplier': {
        # Si prix mensuel, le annual est generalement 60-70% du prix x12
        'monthly_to_annual_ratio': 0.65,
        # % des abonnes qui choisissent annuel
        'annual_adoption': 0.35,
    },
}

# Benchmarks de cout
COSTS = {
    'supabase_free': 0,           # Gratuit <500MB
    'supabase_pro': 25,           # 25$/mois
    'revenuecat': 0,              # Gratuit <2.5K$ MRR
    'revenuecat_pro': 0,          # 1% au dessus (negligeable au debut)
    'sentry': 0,                  # Gratuit
    'domain': 1,                  # ~12 EUR/an = 1/mois
    'hosting': 3,                 # Hostinger
    'google_play': 2,             # 25$ one-time / 12 mois
    'apple_dev': 8.3,             # 99$/an = 8.3/mois
    'content_creation': 0,        # Variable, 0 par defaut
    'total_fixed_low': 6,         # Minimum absolu/mois
    'total_fixed_medium': 40,     # Avec Supabase Pro + Apple
    'total_fixed_high': 100,      # Avec tout + content
}

# Presets
PRESETS = {
    'sleepcoach': {
        'idea': 'SleepCoach FR',
        'segment_size': 20_000_000,
        'reachable_pct': 0.001,    # 0.1% = marketing organique sur 20M
        'price_monthly': 6.99,
        'price_annual': 49.99,
        'install_to_trial': 'high',   # App therapeutique = forte intention
        'trial_to_paid': 'medium',
        'churn': 'low',               # Programme 8 sem = sticky
        'growth': 'medium',
        'costs': 'total_fixed_medium',
        'notes': 'CBT-I therapeutique, programme 8 semaines, zero concurrent FR',
    },
    'doctafter': {
        'idea': 'DoctAfter',
        'segment_size': 40_000_000,
        'reachable_pct': 0.0005,   # 0.05% = trafic organique
        'price_monthly': 2.99,
        'price_annual': 24.99,
        'install_to_trial': 'medium',
        'trial_to_paid': 'medium',
        'churn': 'medium',
        'growth': 'high',             # Viralite medecin-patient
        'costs': 'total_fixed_medium',
        'notes': 'Suivi post-consultation, 40M users Doctolib, gap beeant',
    },
    'coachcrm': {
        'idea': 'CoachCRM',
        'segment_size': 50_000,
        'reachable_pct': 0.02,     # 2% = niche bien ciblee
        'price_monthly': 9.99,
        'price_annual': 79.99,
        'install_to_trial': 'high',
        'trial_to_paid': 'high',      # Outil pro = forte conversion
        'churn': 'low',               # SaaS pro = sticky
        'growth': 'low',              # Niche = croissance lente
        'costs': 'total_fixed_low',
        'notes': 'CRM vertical coach, freemium 5 clients, niche pro',
    },
    'petitsbouts': {
        'idea': 'PetitsBouts',
        'segment_size': 750_000,
        'reachable_pct': 0.005,
        'price_monthly': 3.99,
        'price_annual': 29.99,
        'install_to_trial': 'medium',
        'trial_to_paid': 'low',
        'churn': 'medium',
        'growth': 'medium',
        'costs': 'total_fixed_low',
        'notes': 'App parentalite FR, 750K grossesses/an, zero app adaptee systeme FR',
    },
    'nutrizen': {
        'idea': 'NutriZen',
        'segment_size': 10_000_000,
        'reachable_pct': 0.0005,
        'price_monthly': 4.99,
        'price_annual': 34.99,
        'install_to_trial': 'medium',
        'trial_to_paid': 'low',       # Marche habitue au gratuit
        'churn': 'high',
        'growth': 'medium',
        'costs': 'total_fixed_low',
        'notes': 'Compteur calories sans pub. Yazio 69% neg, MFP 62% neg.',
    },
}


def calculate_blended_arpu(price_monthly, price_annual, annual_adoption=0.35):
    """Calcule l'ARPU mixte (mensuel + annuel)."""
    monthly_payers = 1 - annual_adoption
    annual_monthly_equiv = price_annual / 12
    blended = (monthly_payers * price_monthly) + (annual_adoption * annual_monthly_equiv)
    return round(blended, 2)


def forecast_12_months(
    idea,
    segment_size,
    reachable_pct,
    price_monthly,
    price_annual,
    install_to_trial='medium',
    trial_to_paid='medium',
    churn='medium',
    growth='medium',
    monthly_costs=40,
    notes='',
):
    """Genere un previsionnel mois par mois sur 12 mois."""

    # Resolve benchmark levels
    i2t = BENCHMARKS['install_to_trial'][install_to_trial]
    t2p = BENCHMARKS['trial_to_paid'][trial_to_paid]
    churn_rate = BENCHMARKS['monthly_churn'][churn]
    growth_rate = BENCHMARKS['organic_install_growth'][growth]

    # Initial installs (month 1)
    initial_installs = int(segment_size * reachable_pct)
    blended_arpu = calculate_blended_arpu(price_monthly, price_annual)

    # Conversion funnel
    conversion_rate = i2t * t2p  # install -> paid

    months = []
    cumul_installs = 0
    active_subscribers = 0
    cumul_revenue = 0
    cumul_costs = 0

    for m in range(1, 13):
        # New installs this month (growing)
        new_installs = int(initial_installs * ((1 + growth_rate) ** (m - 1)))
        cumul_installs += new_installs

        # New subscribers from this month's installs
        new_subs = int(new_installs * conversion_rate)

        # Churn from existing
        churned = int(active_subscribers * churn_rate)

        # Active subscribers
        active_subscribers = active_subscribers + new_subs - churned
        active_subscribers = max(active_subscribers, 0)

        # Revenue
        revenue = round(active_subscribers * blended_arpu, 2)
        profit = round(revenue - monthly_costs, 2)
        cumul_revenue += revenue
        cumul_costs += monthly_costs

        months.append({
            'month': m,
            'new_installs': new_installs,
            'cumul_installs': cumul_installs,
            'new_subs': new_subs,
            'churned': churned,
            'active_subs': active_subscribers,
            'mrr': revenue,
            'costs': monthly_costs,
            'profit': profit,
            'cumul_revenue': round(cumul_revenue, 2),
            'cumul_profit': round(cumul_revenue - cumul_costs, 2),
        })

    return {
        'idea': idea,
        'params': {
            'segment_size': segment_size,
            'reachable_pct': reachable_pct,
            'initial_installs_m1': initial_installs,
            'price_monthly': price_monthly,
            'price_annual': price_annual,
            'blended_arpu': blended_arpu,
            'conversion_rate': round(conversion_rate * 100, 2),
            'install_to_trial': f"{i2t*100:.0f}% ({install_to_trial})",
            'trial_to_paid': f"{t2p*100:.0f}% ({trial_to_paid})",
            'monthly_churn': f"{churn_rate*100:.0f}% ({churn})",
            'monthly_growth': f"{growth_rate*100:.0f}% ({growth})",
            'monthly_costs': monthly_costs,
        },
        'months': months,
        'notes': notes,
    }


def display_forecast(forecast):
    """Affiche le previsionnel de facon lisible."""

    p = forecast['params']

    print(f"\n{'#'*70}")
    print(f"  PREVISIONNEL DE RENTABILITE — {forecast['idea']}")
    print(f"  {datetime.now().strftime('%Y-%m-%d')}")
    print(f"{'#'*70}")

    print(f"\n  HYPOTHESES:")
    print(f"    Segment cible          : {p['segment_size']:>12,} personnes")
    print(f"    % atteignable          : {p['reachable_pct']*100:.2f}%")
    print(f"    Installs mois 1        : {p['initial_installs_m1']:>12,}")
    print(f"    Prix mensuel           :       {p['price_monthly']:.2f} EUR")
    print(f"    Prix annuel            :      {p['price_annual']:.2f} EUR")
    print(f"    ARPU mixte/mois        :       {p['blended_arpu']:.2f} EUR")
    print(f"    Install > trial        : {p['install_to_trial']}")
    print(f"    Trial > paid           : {p['trial_to_paid']}")
    print(f"    Conversion totale      : {p['conversion_rate']}%")
    print(f"    Churn mensuel          : {p['monthly_churn']}")
    print(f"    Croissance installs    : {p['monthly_growth']}")
    print(f"    Couts fixes/mois       :      {p['monthly_costs']:.0f} EUR")

    if forecast.get('notes'):
        print(f"\n    Note: {forecast['notes']}")

    # Monthly table
    print(f"\n  {'='*70}")
    print(f"  PREVISIONNEL MOIS PAR MOIS")
    print(f"  {'='*70}")
    print(f"\n  {'Mois':>5s} {'Installs':>10s} {'Nouveaux':>10s} {'Churn':>7s} {'Abonnes':>9s} {'MRR':>10s} {'Couts':>8s} {'Profit':>10s} {'Cumul':>12s}")
    print(f"  {'-'*5} {'-'*10} {'-'*10} {'-'*7} {'-'*9} {'-'*10} {'-'*8} {'-'*10} {'-'*12}")

    breakeven_month = None

    for m in forecast['months']:
        profit_sign = '+' if m['profit'] >= 0 else ''
        cumul_sign = '+' if m['cumul_profit'] >= 0 else ''

        # Highlight breakeven
        marker = ''
        if m['profit'] >= 0 and breakeven_month is None:
            breakeven_month = m['month']
            marker = ' <<< BREAKEVEN'

        print(f"  M{m['month']:>3d} {m['new_installs']:>10,} {m['new_subs']:>10,} {m['churned']:>7,} {m['active_subs']:>9,} {m['mrr']:>9,.0f}E {m['costs']:>7,.0f}E {profit_sign}{m['profit']:>9,.0f}E {cumul_sign}{m['cumul_profit']:>10,.0f}E{marker}")

    # Summary
    last = forecast['months'][-1]
    m6 = forecast['months'][5]

    print(f"\n  {'='*70}")
    print(f"  RESUME")
    print(f"  {'='*70}")

    print(f"\n  A 6 MOIS:")
    print(f"    Abonnes actifs         : {m6['active_subs']:>8,}")
    print(f"    MRR                    : {m6['mrr']:>8,.0f} EUR/mois")
    print(f"    Revenue cumule         : {m6['cumul_revenue']:>8,.0f} EUR")
    print(f"    Profit cumule          : {m6['cumul_profit']:>8,.0f} EUR")

    print(f"\n  A 12 MOIS:")
    print(f"    Installs cumules       : {last['cumul_installs']:>8,}")
    print(f"    Abonnes actifs         : {last['active_subs']:>8,}")
    print(f"    MRR                    : {last['mrr']:>8,.0f} EUR/mois")
    print(f"    ARR (x12)              : {last['mrr']*12:>8,.0f} EUR/an")
    print(f"    Revenue cumule 12 mois : {last['cumul_revenue']:>8,.0f} EUR")
    print(f"    Profit cumule 12 mois  : {last['cumul_profit']:>8,.0f} EUR")

    if breakeven_month:
        print(f"\n    Breakeven atteint      : Mois {breakeven_month}")
    else:
        print(f"\n    Breakeven              : Non atteint en 12 mois")

    # Verdict
    mrr_12 = last['mrr']
    print(f"\n  {'*'*50}")
    if mrr_12 >= 10000:
        print(f"  VERDICT: EXCELLENT — {mrr_12:,.0f} EUR MRR a M12")
        print(f"  Business auto-suffisant, potentiel d'embauche")
    elif mrr_12 >= 5000:
        print(f"  VERDICT: SOLIDE — {mrr_12:,.0f} EUR MRR a M12")
        print(f"  Revenu principal viable pour solo dev")
    elif mrr_12 >= 1000:
        print(f"  VERDICT: VIABLE — {mrr_12:,.0f} EUR MRR a M12")
        print(f"  Micro-SaaS rentable, couvre les couts + revenu complementaire")
    elif mrr_12 >= 100:
        print(f"  VERDICT: EMERGENT — {mrr_12:,.0f} EUR MRR a M12")
        print(f"  Traction naissante, besoin d'accelerer la croissance")
    else:
        print(f"  VERDICT: INSUFFISANT — {mrr_12:,.0f} EUR MRR a M12")
        print(f"  Revoir le modele ou le segment")
    print(f"  {'*'*50}")

    # Scenarios
    print(f"\n  SCENARIOS (MRR a M12):")
    scenarios = [
        ('Pessimiste (x0.5)', 0.5),
        ('Base', 1.0),
        ('Optimiste (x2)', 2.0),
        ('Viral (x5)', 5.0),
    ]
    for label, multiplier in scenarios:
        est_mrr = mrr_12 * multiplier
        print(f"    {label:25s} : {est_mrr:>8,.0f} EUR/mois = {est_mrr*12:>10,.0f} EUR/an")

    print(f"{'#'*70}")

    # Save
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'research')
    os.makedirs(output_dir, exist_ok=True)
    slug = forecast['idea'].lower().replace(' ', '_')[:20]
    filepath = os.path.join(output_dir, f"forecast_{slug}_{datetime.now():%Y%m%d}.json")

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(forecast, f, ensure_ascii=False, indent=2)

    print(f"\n  Rapport: {filepath}")

    return forecast


def main():
    parser = argparse.ArgumentParser(description="MOAT Revenue Forecast")
    parser.add_argument("--idea", help="Nom de l'idee")
    parser.add_argument("--segment-size", type=int, help="Taille du segment")
    parser.add_argument("--reachable-pct", type=float, default=0.001, help="% atteignable (defaut: 0.1%%)")
    parser.add_argument("--price", type=float, help="Prix mensuel EUR")
    parser.add_argument("--price-annual", type=float, help="Prix annuel EUR")
    parser.add_argument("--model", choices=['freemium', 'paid', 'prosumer'], default='freemium')
    parser.add_argument("--growth", choices=['low', 'medium', 'high'], default='medium')
    parser.add_argument("--churn", choices=['low', 'medium', 'high'], default='medium')
    parser.add_argument("--costs", type=float, default=40, help="Couts fixes mensuels EUR")
    parser.add_argument("--preset", help="Utiliser un preset (sleepcoach, doctafter, coachcrm, petitsbouts, nutrizen)")
    parser.add_argument("--list-presets", action="store_true", help="Lister les presets")
    args = parser.parse_args()

    if args.list_presets:
        print(f"\n  Presets disponibles:")
        for name, p in PRESETS.items():
            print(f"    {name:20s} {p['idea']:20s} {p['price_monthly']:.2f}EUR/mois  segment: {p['segment_size']:,}")
        return

    if args.preset:
        if args.preset not in PRESETS:
            print(f"Preset inconnu: {args.preset}. Utilise --list-presets")
            return
        p = PRESETS[args.preset]
        f = forecast_12_months(
            idea=p['idea'],
            segment_size=p['segment_size'],
            reachable_pct=p['reachable_pct'],
            price_monthly=p['price_monthly'],
            price_annual=p['price_annual'],
            install_to_trial=p['install_to_trial'],
            trial_to_paid=p['trial_to_paid'],
            churn=p['churn'],
            growth=p['growth'],
            monthly_costs=COSTS[p['costs']],
            notes=p['notes'],
        )
        display_forecast(f)

    elif args.idea and args.segment_size and args.price:
        price_annual = args.price_annual or round(args.price * 12 * 0.65, 2)
        f = forecast_12_months(
            idea=args.idea,
            segment_size=args.segment_size,
            reachable_pct=args.reachable_pct,
            price_monthly=args.price,
            price_annual=price_annual,
            churn=args.churn,
            growth=args.growth,
            monthly_costs=args.costs,
        )
        display_forecast(f)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
