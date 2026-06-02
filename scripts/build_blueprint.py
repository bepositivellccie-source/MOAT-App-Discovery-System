#!/usr/bin/env python3
"""
Build Blueprint V2 — Générateur de Prompt Claude Design
=========================================================

Lit les données MOAT (engine_*.json + community_signal_*.json) et génère
un prompt Claude Design en 6 sections entièrement auto-remplies.

Valeur ajoutée : section 4 "Garde-fous Design" dérivés des données marché objectives
→ Claude Design pose des questions hyper-contextualisées plutôt que génériques.

Livrable : data/blueprints/{slug}/design_prompt.md (~150 lignes, 0 slot [À COMPLÉTER])

Usage :
    python scripts/build_blueprint.py "DiabeteCoach FR"
    python scripts/build_blueprint.py "ChronoFacture" --style-note "Dark mode premium souhaité"
    python scripts/build_blueprint.py "SleepCoach FR" --print
    python scripts/build_blueprint.py "BurnoutDetect" --no-save
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from typing import Optional

# ── Chemins ──────────────────────────────────────────────────────────────────
SCRIPT_DIR     = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR       = os.path.dirname(SCRIPT_DIR)
RESEARCH_DIR   = os.path.join(ROOT_DIR, 'data', 'research')
BLUEPRINTS_DIR = os.path.join(ROOT_DIR, 'data', 'blueprints')
TEMPLATES_DIR  = os.path.join(ROOT_DIR, 'templates')
DESIGN_PROMPT_TEMPLATE = os.path.join(TEMPLATES_DIR, 'claude_design_prompt.md')


# ── FRUSTRATION → GUARDRAIL ───────────────────────────────────────────────────
# Cœur du module. Chaque frustration compétiteur → 1 garde-fou design précis.
# Ces garde-fous alimentent les questions de Claude Design (Section 4 du prompt).
# Source de validation : test live DiabèteCoach FR (2026-04-24).

FRUSTRATION_TO_GUARDRAIL = {
    # Pricing → paywall UX
    "gratuit":        "Freemium lisible : les features gratuites clairement identifiées, pas de bait-and-switch sur les limites",
    "payant":         "Paywall différé (J+14 minimum) sans saisie de CB — l'utilisateur expérimente la valeur AVANT de payer",
    "abonnement":     "Tarif annuel + économie visible AVANT le paywall — ex. 39.99€/an vs 59.88€ en mensuel",
    "premium":        "Comparatif Free/Pro visible dès l'onboarding — bénéfice perçu avant demande de paiement",
    "payante":        "L'app reste utilisable sans paiement — le free tier est réel, pas un teaser frustrant",
    "cher":           "La valeur justifie le prix — afficher l'économie AVANT le chiffre de l'abonnement",
    "prix":           "Transparence tarifaire complète — aucun frais caché, aucun dark pattern de conversion",
    "vénal":          "Le prix apparaît en dernier et discrètement — JAMAIS en proéminence visuelle",
    # UX / performance
    "bug":            "Stabilité visible — états error/empty/loading jamais silencieux, récupération toujours explicite",
    "lent":           "Performance perçue prioritaire — transitions < 200ms, aucun spinner > 1s sans feedback textuel",
    "crash":          "Crash-free > 99.5% avant launch — aucune perte de données silencieuse, Sentry intégré S1",
    "ne fonctionne":  "Robustesse visible — chaque action a un état succès ET un état erreur avec instruction de récupération",
    "fonctionne pas": "Robustesse visible — chaque action a un état succès ET un état erreur avec instruction de récupération",
    # Complexité / friction
    "difficile":      "Action principale en 3 taps maximum — onboarding 3 étapes avec skip accessible à tout moment",
    "compliqué":      "Onboarding progressif — montrer 1 feature à la fois, dashboard jamais vide au premier lancement",
    "impossible":     "UX testée par 3 non-techniciens cible avant release — aucune action bloquante sans issue visible",
    "oblige":         "Tout opt-in (RGPD Art.7) — aucune action irréversible sans confirmation explicite, pas de cage dorée",
    # Ton / émotion
    "pub":            "ZÉRO publicité dans le tier payant — mentionné explicitement dans le paywall comme avantage clé",
    "nul":            "Qualité premium perçue dès le premier écran — polish visible avant même l'inscription",
    "froid":          "Ton chaleureux et humain — JAMAIS de jargon clinique froid ou de vocabulaire technique abstrait",
    "anxiogène":      "Visuel rassurant — pas de rouge alarmiste, pas de DANGER, les alertes utilisent ambre/ocre/bleu",
    "infantilisant":  "Ton adulte expert — pas de confettis, pas d'emoji célébratoire forcé, respect de l'autonomie",
    # Données
    "perdu":          "Données jamais perdues — confirmation visuelle après chaque sauvegarde importante",
    "sync":           "Sync background silencieux — fonctionne offline, synchro au retour réseau sans friction visible",
    # Localisation / scope
    "anglais":        "Interface 100% en français — vocabulaire local, unités métriques, formats de date DD/MM/YYYY",
    "généraliste":    "App spécialisée sur la verticale — pas de tracking universel, profondeur > largeur",
}


# ── PERSONA → GUARDRAIL ───────────────────────────────────────────────────────
# Garde-fous dérivés du profil utilisateur détecté (âge, contexte, usage)

PERSONA_TO_GUARDRAIL = {
    "age_50_plus":     "Accessibilité prioritaire — typo min 17px, contrastes WCAG AAA, zones tactiles 48px+, aucun geste obscur (pas de swipe caché, pas de hold)",
    "non_tech":        "Onboarding ultra-progressif — tutoriel skippable mais toujours ré-accessible, aucune hypothèse sur les compétences numériques",
    "medical_chronic": "Légitimité médicale visible dès l'onboarding — mentions RGPD Art.9, encadrement médical, données chiffrées de sécurité",
    "b2b_pro":         "Sobriété professionnelle absolue — un seul CTA principal par écran, hiérarchie visuelle tranchée, chiffres en police tabulaire",
    "stress_anxiety":  "Environnement visuel calme — espaces blancs généreux, aucune urgence visuelle artificielle, couleurs apaisantes sans être fades",
    "sensitive_data":  "Confidentialité visible — icône cadenas aux endroits stratégiques, formulation RGPD rassurante, aucun partage implicite",
}


# ── SCREEN TEMPLATES ──────────────────────────────────────────────────────────
# Suggestions d'écrans par verticale (priorité : premier tag persona matché)

SCREEN_TEMPLATES = {
    "medical_chronic": [
        "Écran 1 — Dashboard accueil (mesures du jour + état global + alerte si hors seuil)",
        "Écran 2 — Saisie rapide (action principale en < 3 taps, confirmation immédiate)",
        "Écran 3 — Journal des 7 derniers jours (liste + mini-graph inline)",
        "Écran 4 — Courbe Tendances 30j (évolution + marqueurs contextuels repas/médicaments)",
        "Écran 5 — Paywall (essai 14j sans CB, tarif annuel mis en avant vs mensuel)",
        "Écran 6 — Profil médical (seuils personnalisés, médecin référent, export PDF)",
    ],
    "b2b_pro": [
        "Écran 1 — Dashboard (KPIs trésorerie + actions en attente + alerte impayés)",
        "Écran 2 — Liste principale (filtre par statut : brouillon / envoyée / payée / impayée)",
        "Écran 3 — Création (formulaire principal + calcul automatique TVA)",
        "Écran 4 — Détail (aperçu document + actions : envoyer / relancer / encaisser)",
        "Écran 5 — Fiche client (coordonnées + historique + solde total)",
        "Écran 6 — Paramètres (profil entreprise, modèles, conditions de paiement)",
    ],
    "stress_anxiety": [
        "Écran 1 — Onboarding étape finale (personnalisation de l'objectif principal)",
        "Écran 2 — Dashboard Aujourd'hui (état émotionnel + action rapide + streak)",
        "Écran 3 — Séance guidée en cours (exercice principal, progression visible)",
        "Écran 4 — Journal de progression (graphe humeur + insights hebdo)",
        "Écran 5 — Paywall (argument valeur, pas d'urgence artificielle)",
        "Écran 6 — Bibliothèque de contenu (séances guidées disponibles, filtrables)",
    ],
    "default": [
        "Écran 1 — Onboarding (setup profil + valeur démontrée en < 60s)",
        "Écran 2 — Accueil (dashboard principal + action principale du jour)",
        "Écran 3 — Feature principale (cœur du produit, flow complet)",
        "Écran 4 — Progression (historique + tendances + insights)",
        "Écran 5 — Paywall (essai sans CB, valeur avant prix)",
        "Écran 6 — Profil / Paramètres (compte + préférences + abonnement)",
    ],
}


# ── UTILS ─────────────────────────────────────────────────────────────────────

def _slugify(text: str) -> str:
    """Slug ASCII safe pour noms de fichiers."""
    text = text.lower()
    for old, new in [('é','e'),('è','e'),('ê','e'),('à','a'),('â','a'),('ù','u'),
                     ('û','u'),('î','i'),('ô','o'),('ç','c'),('ë','e'),('ï','i'),
                     ('ü','u'),('ý','y'),('ñ','n')]:
        text = text.replace(old, new)
    return re.sub(r'[^\w]', '_', text).strip('_')


def _normalize(text: str) -> str:
    """Normalise accents et casse pour la comparaison de chaînes."""
    text = text.lower()
    for old, new in [('é','e'),('è','e'),('ê','e'),('à','a'),('â','a'),('ù','u'),
                     ('û','u'),('î','i'),('ô','o'),('ç','c'),('ë','e'),('ï','i')]:
        text = text.replace(old, new)
    return text


def find_latest_json(prefix: str, idea_name: str, directory: str) -> Optional[str]:
    """Trouve le fichier JSON le plus récent pour une idée donnée."""
    if not os.path.isdir(directory):
        return None
    slug = _slugify(idea_name)
    # Correspondance exacte d'abord
    pattern = re.compile(rf'^{re.escape(prefix)}_{re.escape(slug)}_\d{{8}}_\d{{4}}\.json$')
    matches = [os.path.join(directory, f) for f in os.listdir(directory) if pattern.match(f)]
    if not matches:
        # Correspondance partielle (slug tronqué à 12 chars)
        short = slug[:12]
        pattern2 = re.compile(rf'^{re.escape(prefix)}_{re.escape(short)}.*\.json$')
        matches = [os.path.join(directory, f) for f in os.listdir(directory) if pattern2.match(f)]
    return sorted(matches)[-1] if matches else None


# ── EXTRACTION ────────────────────────────────────────────────────────────────

def extract_data(engine_path: str, community_path: Optional[str] = None) -> dict:
    """Extrait les champs utiles depuis les JSONs MOAT."""
    with open(engine_path, 'r', encoding='utf-8') as f:
        eng = json.load(f)

    phases   = eng.get('phases', {})
    scoring  = phases.get('scoring', {})
    raw      = scoring.get('raw_scores', {})
    v31      = raw.get('_v31', {})
    v3       = raw.get('_v3', {})
    market   = phases.get('market_sizing', {})
    reviews  = phases.get('review_analysis', {})

    # Flags actifs
    flags_raw    = v31.get('flags_applied', [])
    active_flags = [f[0] if isinstance(f, (list, tuple)) else str(f) for f in flags_raw]

    # Timing type → texte
    timing_type  = v31.get('timing_type') or v3.get('timing_type')
    timing_label = v31.get('timing_type_label', '')
    if not timing_label:
        timing_label = {
            1: 'Driver réglementaire (loi/obligation)',
            2: 'Pathologie chronique (besoin permanent)',
            3: 'Trend culturel (comportement émergent)',
        }.get(timing_type, '')
    if not timing_label and v3.get('structural_driver'):
        timing_label = 'Driver structurel (loi ou pathologie — préciser)'

    # Community signal (optionnel)
    community = {}
    if community_path and os.path.isfile(community_path):
        with open(community_path, 'r', encoding='utf-8') as f:
            community = json.load(f)

    return {
        'idea':              eng.get('idea', ''),
        'date':              eng.get('date', '')[:10],
        'score':             scoring.get('total', 0),
        'decision':          scoring.get('decision', ''),
        'engine_file':       os.path.basename(engine_path),
        'flags':             active_flags,
        'top_frustrations':  reviews.get('top_frustrations', []),
        'review_count':      reviews.get('total_reviews_analyzed', 0),
        'neg_ratio':         reviews.get('avg_negative_ratio', 0),
        'pricing_ratio':     reviews.get('pricing_complaint_ratio', 0),
        'segment_size':      market.get('segment_size', 0),
        'som_solo_y1':       v3.get('som_solo_dev_y1', 0),
        'timing_type':       timing_type,
        'timing_label':      timing_label,
        'community':         community,
    }


# ── PERSONA DETECTION ─────────────────────────────────────────────────────────

def detect_persona_tags(data: dict, idea_name: str) -> list:
    """
    Détecte les tags persona depuis les données MOAT.
    Retourne une liste ordonnée (premier tag = priorité écrans).
    """
    tags    = []
    text    = _normalize(idea_name)
    flags   = data.get('flags', [])
    timing  = data.get('timing_type')

    # Pathologie chronique → médical, âge 45+
    CHRONIC_KEYWORDS = ['diabete', 'glucose', 'glycemie', 'tension', 'alzheimer',
                        'endometriose', 'migraine', 'parkinson', 'cancer', 'epilepsie',
                        'asthme', 'arthrite', 'fibromyalgie', 'prochesoin']
    if timing == 2 or any(k in text for k in CHRONIC_KEYWORDS):
        tags.append('medical_chronic')
        tags.append('age_50_plus')

    # RGPD santé → données sensibles + légitimité médicale
    if any(f in flags for f in ('rgpd_sante', 'rgpd_sante_b2b', 'partner_medical')):
        if 'medical_chronic' not in tags:
            tags.append('medical_chronic')
        if 'sensitive_data' not in tags:
            tags.append('sensitive_data')

    # B2B professionnel
    B2B_KEYWORDS = ['facture', 'invoice', 'crm', 'kine', 'kiné', 'comptable',
                    'comptabilite', 'b2b', 'agenda', 'rdv', 'devis', 'tva', 'docpilot',
                    'procompta', 'chronofacture', 'timetoinvoice']
    if any(k in text for k in B2B_KEYWORDS) or timing == 1:
        tags.append('b2b_pro')

    # Stress / anxiété / bien-être
    WELLNESS_KEYWORDS = ['stress', 'anxiete', 'burnout', 'burn-out', 'sommeil', 'sleep',
                         'meditation', 'mindfulness', 'colere', 'toc', 'sensitivapp',
                         'apaise', 'zencolere', 'calmreal', 'rituelzen', 'soulager']
    if any(k in text for k in WELLNESS_KEYWORDS):
        tags.append('stress_anxiety')

    # Non-tech par proxy : pathologie chronique + public grand âge
    SENIOR_KEYWORDS = ['senior', 'retraite', 'alzheimer', 'parent', 'alz', 'companion']
    if 'age_50_plus' in tags or any(k in text for k in SENIOR_KEYWORDS):
        if 'non_tech' not in tags:
            tags.append('non_tech')

    # Données sensibles génériques (hors santé)
    if 'finance' in text or 'banque' in text or 'patrimoine' in text:
        if 'sensitive_data' not in tags:
            tags.append('sensitive_data')

    # Déduplication + conservation de l'ordre
    seen = set()
    result = []
    for t in tags:
        if t not in seen:
            seen.add(t)
            result.append(t)
    return result


# ── GUARDRAILS ────────────────────────────────────────────────────────────────

def build_guardrails(data: dict, persona_tags: list, style_note: Optional[str] = None) -> list:
    """
    Construit la liste complète des garde-fous pour la Section 4.
    Sources : frustrations compétiteurs + persona tags + style note optionnelle.
    """
    guardrails = []
    seen = set()

    # 1. Garde-fous depuis les frustrations compétiteurs (source principale)
    for word, _count in data.get('top_frustrations', []):
        if word in FRUSTRATION_TO_GUARDRAIL:
            gr = FRUSTRATION_TO_GUARDRAIL[word]
            if gr not in seen:
                seen.add(gr)
                guardrails.append(gr)

    # 2. Garde-fous depuis les personas détectés
    for tag in persona_tags:
        if tag in PERSONA_TO_GUARDRAIL:
            gr = PERSONA_TO_GUARDRAIL[tag]
            if gr not in seen:
                seen.add(gr)
                guardrails.append(gr)

    # 3. Garde-fou style note optionnel (--style-note CLI)
    if style_note:
        gr = f"Direction visuelle souhaitée par le PO : {style_note}"
        if gr not in seen:
            guardrails.append(gr)

    # 4. Garde-fou de sécurité : si aucune frustration → message explicite
    if not guardrails:
        guardrails.append("[Pas de données reviews disponibles — relancer avec --competitors pour obtenir des garde-fous précis]")

    return guardrails


# ── RENDERING ─────────────────────────────────────────────────────────────────

def _render_guardrails_section(guardrails: list) -> str:
    return '\n'.join(f"- {g}" for g in guardrails)


def _render_pain_points(top_frustrations: list, review_count: int) -> str:
    if not top_frustrations:
        return "- [Aucune donnée disponible — relancer avec --competitors pour l'analyse reviews]"
    lines = []
    for word, count in top_frustrations[:6]:
        pct = round(count / max(review_count, 1) * 100) if review_count else '?'
        lines.append(f"- **{word}** ({count} mentions, ~{pct}% des avis négatifs)")
    return '\n'.join(lines)


def _render_screens(persona_tags: list) -> list:
    """Retourne la liste des écrans suggérés depuis les personas."""
    for tag in persona_tags:
        if tag in SCREEN_TEMPLATES:
            return SCREEN_TEMPLATES[tag]
    return SCREEN_TEMPLATES['default']


def _render_target(data: dict) -> str:
    seg = data.get('segment_size', 0)
    som = data.get('som_solo_y1', 0)
    if seg > 0:
        target = f"~{seg:,} personnes".replace(',', ' ')
        if som > 0:
            monthly = round(som / 12)
            target += f" | SOM Solo Dev Y1 : ~{monthly:,} EUR/mois".replace(',', ' ')
        return target
    return "À préciser depuis les données marché"


def _render_vertical(data: dict, idea_name: str) -> str:
    """Retourne la verticale marché (domaine), pas le driver business."""
    text    = _normalize(idea_name)
    timing  = data.get('timing_type')

    # Détecter par timing_type ou keywords
    HEALTH_KW   = ['diabete', 'glucose', 'glycemie', 'tension', 'sante', 'medical',
                   'migraine', 'alzheimer', 'endometriose', 'parkinson', 'cancer',
                   'douleur', 'chronique', 'prochesoin']
    B2B_KW      = ['facture', 'invoice', 'crm', 'comptable', 'kine', 'devis',
                   'tva', 'b2b', 'docpilot', 'timetoinvoice', 'chronofacture']
    WELLNESS_KW = ['sleep', 'sommeil', 'stress', 'anxiete', 'meditation',
                   'mindfulness', 'burnout', 'colere', 'toc', 'zencolere', 'apaise']
    FINANCE_KW  = ['epargne', 'budget', 'investissement', 'patrimoine', 'banque']

    if timing == 2 or any(k in text for k in HEALTH_KW):
        return "Sante numerique — pathologie chronique"
    if any(k in text for k in FINANCE_KW):
        return "Finance personnelle — gestion patrimoniale"
    if timing == 1 or any(k in text for k in B2B_KW):
        return "B2B — outil professionnel / gestion"
    if any(k in text for k in WELLNESS_KW):
        return "Bien-etre — sante mentale / physique"
    return "Consumer — app grand public"


def _render_pain_summary(data: dict) -> str:
    neg     = data.get('neg_ratio', 0)
    pricing = data.get('pricing_ratio', 0)
    count   = data.get('review_count', 0)
    parts   = []
    if neg > 40:
        parts.append(f"{neg}% d'avis négatifs sur les apps existantes")
    if pricing > 30:
        parts.append(f"{pricing}% de plaintes sur le pricing (signal de paiement fort)")
    if count >= 50:
        parts.append(f"validé sur {count} avis réels")
    return ' · '.join(parts) if parts else "Données de reviews insuffisantes — relancer avec --competitors"


def render_design_prompt(
    data:         dict,
    persona_tags: list,
    guardrails:   list,
    screens:      list,
    template_path: str = DESIGN_PROMPT_TEMPLATE,
) -> str:
    """Charge le template et substitue toutes les {{VARIABLES}}."""

    variables = {
        'APP_NAME':        data['idea'],
        'DATE':            datetime.now().strftime('%Y-%m-%d'),
        'SCORE':           str(data['score']),
        'DECISION':        data['decision'],
        'ENGINE_FILE':     data['engine_file'],
        'TARGET':          _render_target(data),
        'PAIN_SUMMARY':    _render_pain_summary(data),
        'VERTICAL':        _render_vertical(data, data['idea']),
        'DRIVER':          data['timing_label'] or 'À préciser',
        'REVIEW_COUNT':    str(data['review_count']),
        'PAIN_POINTS_LIST': _render_pain_points(data['top_frustrations'], data['review_count']),
        'GUARDRAILS_LIST': _render_guardrails_section(guardrails),
        'SCREENS_COUNT':   str(len(screens)),
        'SCREENS_LIST':    '\n'.join(screens),
    }

    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Substitution (clés longues en premier pour éviter les sous-substitutions)
    for key in sorted(variables.keys(), key=len, reverse=True):
        content = content.replace('{{' + key + '}}', variables[key])

    return content


# ── ORCHESTRATEUR ─────────────────────────────────────────────────────────────

def run_build_blueprint(
    idea_name:     str,
    engine_path:   Optional[str] = None,
    community_path: Optional[str] = None,
    style_note:    Optional[str] = None,
    save:          bool = True,
    quiet:         bool = False,
) -> dict:
    """Orchestrateur principal."""

    def log(msg):
        if not quiet:
            print(msg)

    log(f"\n{'='*60}")
    log(f"  BUILD BLUEPRINT V2 -- {idea_name}")
    log(f"{'='*60}")

    # 1. Trouver les fichiers sources
    if not engine_path or not os.path.isfile(engine_path):
        engine_path = find_latest_json('engine', idea_name, RESEARCH_DIR)
        if not engine_path:
            print(f"[ERREUR] Aucun engine_*.json trouvé pour '{idea_name}'")
            print(f"         Répertoire : {RESEARCH_DIR}")
            sys.exit(1)

    log(f"  Source engine    : {os.path.basename(engine_path)}")

    if not community_path or not os.path.isfile(community_path):
        community_path = find_latest_json('community_signal', idea_name, RESEARCH_DIR)

    if community_path:
        log(f"  Source community : {os.path.basename(community_path)}")
    else:
        log(f"  Community signal : non disponible (optionnel)")

    # 2. Extraire les données
    data = extract_data(engine_path, community_path)
    log(f"  Score MOAT V3.1  : {data['score']}/100 -- {data['decision']}")
    log(f"  Reviews analysées: {data['review_count']}")
    log(f"  Frustrations     : {len(data['top_frustrations'])} identifiées")

    # 3. Détecter les personas
    persona_tags = detect_persona_tags(data, idea_name)
    log(f"  Personas détectés: {', '.join(persona_tags) if persona_tags else 'default'}")

    # 4. Construire les garde-fous
    guardrails = build_guardrails(data, persona_tags, style_note)
    from_frustrations = sum(1 for w, _ in data.get('top_frustrations', [])
                            if w in FRUSTRATION_TO_GUARDRAIL)
    from_persona = len(persona_tags)
    log(f"  Garde-fous       : {len(guardrails)} total "
        f"({from_frustrations} frustrations + {from_persona} persona"
        f"{' + 1 style note' if style_note else ''})")

    # 5. Sélectionner les écrans
    screens = _render_screens(persona_tags)
    log(f"  Écrans suggérés  : {len(screens)}")

    # 6. Générer le prompt
    design_prompt = render_design_prompt(data, persona_tags, guardrails, screens)

    # 7. Sauvegarder
    output_path = None
    if save:
        slug    = _slugify(idea_name)
        out_dir = os.path.join(BLUEPRINTS_DIR, slug)
        os.makedirs(out_dir, exist_ok=True)
        output_path = os.path.join(out_dir, 'design_prompt.md')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(design_prompt)
        log(f"\n  Prompt sauvegarde: {output_path}")

    log(f"  Pret a coller dans Claude Design (0 slot a completer)")
    log(f"{'='*60}\n")

    return {
        'idea':          idea_name,
        'persona_tags':  persona_tags,
        'score':         data['score'],
        'guardrails_count': len(guardrails),
        'screens_count': len(screens),
        'design_prompt': design_prompt,
        'output_path':   output_path,
    }


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Build Blueprint V2 — Génère le prompt Claude Design depuis les données MOAT"
    )
    parser.add_argument('idea', help="Nom de l'idée (ex: 'DiabeteCoach FR')")
    parser.add_argument('--engine',    help="Chemin explicite vers engine_*.json")
    parser.add_argument('--community', help="Chemin explicite vers community_signal_*.json")
    parser.add_argument('--style-note', metavar='NOTE',
                        help="Note de direction visuelle. Ex: 'Dark mode premium souhaité'. "
                             "Ajoute un garde-fou en Section 4.")
    parser.add_argument('--no-save',  action='store_true',
                        help="Ne pas écrire le fichier — afficher seulement dans le terminal")
    parser.add_argument('--print',    action='store_true',
                        help="Afficher le prompt dans le terminal après génération")
    parser.add_argument('--quiet', '-q', action='store_true',
                        help="Mode silencieux (logs réduits)")

    args = parser.parse_args()

    result = run_build_blueprint(
        idea_name=args.idea,
        engine_path=args.engine,
        community_path=args.community,
        style_note=args.style_note,
        save=not args.no_save,
        quiet=args.quiet,
    )

    if args.print or args.no_save:
        # Encode-safe pour console Windows cp1252
        safe = result['design_prompt'].encode('cp1252', errors='replace').decode('cp1252')
        print('\n' + '-'*60)
        print(safe)
        print('-'*60)


if __name__ == '__main__':
    main()
