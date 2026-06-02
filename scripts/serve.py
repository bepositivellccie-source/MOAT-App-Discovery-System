#!/usr/bin/env python3
"""
MOAT Local Dev Server
=====================

Sert dashboard_live.html en static (comme `python -m http.server`)
ET expose 3 endpoints JSON locaux pour generer les fiches manquantes
depuis le bouton "Construire" du modal Roadmap.

Endpoints :
  POST /api/build_blueprint      body {"idea":"..."}  -> run build_blueprint.py
  POST /api/build_index          body {"idea":"..."}  -> run build_index.py
  POST /api/scaffold_opportunity body {"idea":"..."}  -> ecrit data/opportunities/{date}_{slug}.md

Securite :
  - Bind localhost (127.0.0.1) uniquement, pas expose au LAN
  - Validation stricte du parametre idea (regex + longueur max)
  - subprocess.run sans shell=True (args en liste -> pas d'injection)

Usage :
    python scripts/serve.py            # port 8080 par defaut
    python scripts/serve.py 8432       # port custom
"""

import http.server
import json
import os
import re
import subprocess
import sys
import unicodedata
from datetime import datetime

ROOT_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(ROOT_DIR, 'scripts')
RESEARCH    = os.path.join(ROOT_DIR, 'data', 'research')
OPP_DIR     = os.path.join(ROOT_DIR, 'data', 'opportunities')
TEMPLATES   = os.path.join(ROOT_DIR, 'templates')

IDEA_RE = re.compile(r"^[A-Za-z0-9À-ſ _'-]{1,100}$")


def slugify(text: str) -> str:
    """Port du _slugify Python (build_blueprint.py) - ASCII safe."""
    s = text.lower()
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^\w]', '_', s).strip('_')


def find_latest_engine(slug: str):
    if not os.path.isdir(RESEARCH):
        return None
    prefix = f'engine_{slug}_'
    matches = sorted(f for f in os.listdir(RESEARCH)
                     if f.startswith(prefix) and f.endswith('.json'))
    return os.path.join(RESEARCH, matches[-1]) if matches else None


def run_script(args, timeout=60):
    """Run a script subprocess, return (ok, stdout, stderr, code)."""
    try:
        result = subprocess.run(
            args, cwd=ROOT_DIR, capture_output=True, text=True,
            timeout=timeout, shell=False, encoding='utf-8', errors='replace',
        )
        return (result.returncode == 0, result.stdout, result.stderr, result.returncode)
    except subprocess.TimeoutExpired:
        return (False, '', f'Timeout apres {timeout}s', -1)
    except Exception as e:
        return (False, '', f'{type(e).__name__}: {e}', -1)


def handle_build_blueprint(idea: str) -> dict:
    """Run build_blueprint.py - genere data/blueprints/{slug}/design_prompt.md"""
    ok, out, err, code = run_script(
        [sys.executable, os.path.join(SCRIPTS_DIR, 'build_blueprint.py'), idea],
        timeout=30,
    )
    slug = slugify(idea)
    output_path = f'data/blueprints/{slug}/design_prompt.md'
    exists = os.path.isfile(os.path.join(ROOT_DIR, output_path))
    return {
        'ok': ok and exists,
        'output_path': output_path if exists else None,
        'stdout': out[-2000:] if out else '',
        'stderr': err[-2000:] if err else '',
        'code': code,
    }


def handle_build_index(idea: str) -> dict:
    """Run build_index.py - utilise IDEA_PRESETS si dispo, sinon moat_score depuis engine.json."""
    slug = slugify(idea)
    moat_score = None
    engine_path = find_latest_engine(slug)
    if engine_path:
        try:
            with open(engine_path, 'r', encoding='utf-8') as f:
                eng = json.load(f)
            score = (eng.get('phases', {}).get('scoring', {}).get('total')
                     or eng.get('verdict', {}).get('score'))
            if score:
                moat_score = int(score)
        except Exception:
            pass

    # Etape 1 : tenter avec preset (sans --moat-score) - utilise IDEA_PRESETS si idea connue
    bin_py = sys.executable
    script = os.path.join(SCRIPTS_DIR, 'build_index.py')
    ok, out, err, code = run_script([bin_py, script, '--idea', idea], timeout=15)

    # Si pas de preset trouve, retry avec flags custom
    used_preset = True
    if 'non trouve' in (out or '').lower() or 'utilise --moat-score' in (out or '').lower():
        used_preset = False
        if moat_score is None:
            moat_score = 50  # fallback safe
        ok, out, err, code = run_script([
            bin_py, script, '--idea', idea,
            '--moat-score', str(moat_score),
            '--stack-match', '5',
            '--mvp-weeks', '8',
            '--synergy', '3',
            '--mvp-clarity', '3',
            '--risk', '3',
        ], timeout=15)

    fiche_dir = os.path.join(ROOT_DIR, 'data', 'build_fiches')
    output_path = None
    if os.path.isdir(fiche_dir):
        # build_index.py slugifie naivement (lower + replace space) sans dropper les accents.
        # On cherche d'abord avec ce slug brut, puis on rename en ASCII propre pour le frontend.
        raw_slug  = idea.lower().replace(' ', '_')[:20]
        ascii_slug = slug[:20]
        all_files = sorted(os.listdir(fiche_dir))
        match = None
        for variant in (raw_slug, ascii_slug):
            prefix = f'build_{variant}_'
            cands = [f for f in all_files if f.startswith(prefix) and f.endswith('.md')]
            if cands:
                match = cands[-1]
                break
        if match:
            src = os.path.join(fiche_dir, match)
            ascii_name = f'build_{ascii_slug}_{datetime.now():%Y%m%d}.md'
            dst = os.path.join(fiche_dir, ascii_name)
            if match != ascii_name and not os.path.isfile(dst):
                try:
                    os.rename(src, dst)
                    output_path = f'data/build_fiches/{ascii_name}'
                except OSError:
                    output_path = f'data/build_fiches/{match}'
            else:
                output_path = f'data/build_fiches/{match}'

    # Parse le BRI depuis stdout pour donner un retour utile meme si fiche pas generee
    bri = None
    decision_text = None
    m = re.search(r'TOTAL\s+BRI\s+([\d.]+)\s*/\s*100', out or '')
    if m:
        try:
            bri = float(m.group(1))
        except ValueError:
            pass
    m = re.search(r'DECISION\s*:\s*(.+)', out or '')
    if m:
        decision_text = m.group(1).strip()

    return {
        'ok': ok,                      # le script s'est-il execute correctement ?
        'fiche_generated': output_path is not None,
        'output_path': output_path,
        'bri': bri,
        'decision': decision_text,
        'used_preset': used_preset,
        'moat_score_used': moat_score,
        'stdout': out[-2000:] if out else '',
        'stderr': err[-2000:] if err else '',
        'code': code,
    }


def handle_scaffold_opportunity(idea: str) -> dict:
    """Cree data/opportunities/{date}_{slug}.md avec les champs auto-remplis depuis engine.json."""
    slug = slugify(idea)
    date_str = datetime.now().strftime('%Y-%m-%d')
    output_filename = f'{date_str}_{slug}.md'
    output_full = os.path.join(OPP_DIR, output_filename)
    output_rel = f'data/opportunities/{output_filename}'

    if os.path.isfile(output_full):
        return {'ok': True, 'output_path': output_rel, 'already_existed': True}

    template_path = os.path.join(TEMPLATES, 'opportunity_card.md')
    if not os.path.isfile(template_path):
        return {'ok': False, 'stderr': f'Template introuvable : {template_path}'}

    with open(template_path, 'r', encoding='utf-8') as f:
        tpl = f.read()

    eng = None
    engine_path = find_latest_engine(slug)
    if engine_path:
        try:
            with open(engine_path, 'r', encoding='utf-8') as f:
                eng = json.load(f)
        except Exception:
            pass

    md = tpl.replace('[NOM DE L\'IDEE]', idea).replace('[NOM DE L IDEE]', idea)
    md = md.replace('# [NOM DE L\'IDEE]', f'# {idea}')

    sources_block = '\n## Sources auto\n'
    sources_block += f'- **Date scaffolding** : {date_str}\n'
    if engine_path:
        sources_block += f'- **Engine source** : `{os.path.relpath(engine_path, ROOT_DIR)}`\n'
    if eng:
        scoring = eng.get('phases', {}).get('scoring', {})
        verdict = eng.get('verdict', {})
        market  = eng.get('phases', {}).get('market_sizing', {})
        reviews = eng.get('phases', {}).get('review_analysis', {})
        if scoring.get('total'):
            sources_block += f'- **Score MOAT** : {scoring["total"]}/100 ({scoring.get("decision","")})\n'
        if market.get('segment_size'):
            sources_block += f'- **Segment size** : {market["segment_size"]:,}\n'
        if market.get('som'):
            sources_block += f'- **SOM** : {market["som"]:,.0f} EUR\n'
        if reviews.get('total_reviews_analyzed'):
            sources_block += f'- **Avis analyses** : {reviews["total_reviews_analyzed"]}\n'
            sources_block += f'- **Ratio negatifs** : {reviews.get("avg_negative_ratio",0)}%\n'
        if verdict.get('signals'):
            sources_block += '- **Signals** : ' + ' / '.join(verdict['signals'][:3]) + '\n'
        if verdict.get('risks'):
            sources_block += '- **Risks** : ' + ' / '.join(verdict['risks'][:3]) + '\n'

    md = md.rstrip() + '\n\n' + sources_block + '\n*Scaffold genere par serve.py - a completer manuellement.*\n'

    os.makedirs(OPP_DIR, exist_ok=True)
    with open(output_full, 'w', encoding='utf-8') as f:
        f.write(md)

    return {
        'ok': True,
        'output_path': output_rel,
        'engine_source': os.path.relpath(engine_path, ROOT_DIR) if engine_path else None,
        'already_existed': False,
    }


ACTIONS = {
    'build_blueprint':      handle_build_blueprint,
    'build_index':          handle_build_index,
    'scaffold_opportunity': handle_scaffold_opportunity,
}


class MoatHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT_DIR, **kwargs)

    def _send_json(self, payload, status=200):
        body = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if not self.path.startswith('/api/'):
            self.send_error(404, 'Not Found')
            return
        action = self.path[len('/api/'):].split('?', 1)[0].strip('/')
        if action not in ACTIONS:
            self._send_json({'ok': False, 'error': f'Action inconnue : {action}'}, 404)
            return

        try:
            length = int(self.headers.get('Content-Length', '0'))
            raw = self.rfile.read(length) if length > 0 else b'{}'
            body = json.loads(raw.decode('utf-8'))
        except Exception as e:
            self._send_json({'ok': False, 'error': f'Body JSON invalide : {e}'}, 400)
            return

        idea = (body.get('idea') or '').strip()
        if not idea or not IDEA_RE.match(idea):
            self._send_json({'ok': False, 'error': 'Champ "idea" invalide ou absent (regex strict).'}, 400)
            return

        try:
            result = ACTIONS[action](idea)
            status = 200 if result.get('ok') else 500
            self._send_json(result, status)
        except Exception as e:
            self._send_json({'ok': False, 'error': f'{type(e).__name__}: {e}'}, 500)

    def log_message(self, format, *args):
        sys.stderr.write(f'[{datetime.now():%H:%M:%S}] {self.address_string()} - {format % args}\n')


def main():
    port = 8080
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f'Port invalide : {sys.argv[1]}', file=sys.stderr)
            sys.exit(1)

    server = http.server.ThreadingHTTPServer(('127.0.0.1', port), MoatHandler)
    print(f'MOAT serve.py - http://localhost:{port}/dashboard_live.html')
    print(f'  GET  /...                       -> static files (cwd = {ROOT_DIR})')
    print(f'  POST /api/build_blueprint        -> generate design_prompt.md')
    print(f'  POST /api/build_index            -> generate build fiche')
    print(f'  POST /api/scaffold_opportunity   -> scaffold opportunity card')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nArret du serveur.')
        server.shutdown()


if __name__ == '__main__':
    main()
