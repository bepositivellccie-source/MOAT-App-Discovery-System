#!/usr/bin/env python3
"""
Cleanup Airtable duplicates — helper script.

Le MCP Airtable n'a pas de tool de suppression. Ce script utilise l'API directe.

Usage:
    export AIRTABLE_TOKEN="pat_xxxxxxxxxx"
    python scripts/cleanup_airtable_duplicates.py

Ou en ligne de commande:
    python scripts/cleanup_airtable_duplicates.py --token pat_xxxxxxxxxx

Le token est le Personal Access Token Airtable avec scope data.records:write sur la base MOAT.
Pour le creer: https://airtable.com/create/tokens
"""

import argparse
import os
import sys
import urllib.request
import urllib.error
import json


BASE_ID = "appupXnLCe8ZIpKdV"
TABLE_ID = "tblKhcP3GsGMmhzb1"

DUPLICATES_TO_DELETE = [
    ("recEWmjGS7vf49ZZ2", "DOUBLON SUPPRIMER — BurnoutDetect"),
    ("recicbXCcykZkLfYL", "DOUBLON SUPPRIMER — ProcheSoin"),
]


def delete_record(token: str, record_id: str, label: str) -> bool:
    """Delete a single record via Airtable API."""
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_ID}/{record_id}"
    req = urllib.request.Request(url, method="DELETE")
    req.add_header("Authorization", f"Bearer {token}")

    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read())
            if data.get("deleted"):
                print(f"  OK    {record_id}  {label}")
                return True
            else:
                print(f"  FAIL  {record_id}  unexpected response: {data}")
                return False
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"  FAIL  {record_id}  HTTP {e.code}: {body}")
        return False
    except Exception as e:
        print(f"  FAIL  {record_id}  {type(e).__name__}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Delete Airtable duplicate records.")
    parser.add_argument("--token", help="Airtable PAT (Personal Access Token)")
    parser.add_argument("--dry-run", action="store_true", help="List records without deleting")
    args = parser.parse_args()

    token = args.token or os.environ.get("AIRTABLE_TOKEN")
    if not token and not args.dry_run:
        print("ERROR: AIRTABLE_TOKEN non fourni.")
        print("Usage: python cleanup_airtable_duplicates.py --token pat_xxxxx")
        print("   ou: export AIRTABLE_TOKEN=pat_xxxxx && python cleanup_airtable_duplicates.py")
        sys.exit(1)

    print(f"Base    : {BASE_ID}")
    print(f"Table   : {TABLE_ID}")
    print(f"Records a supprimer : {len(DUPLICATES_TO_DELETE)}")
    print()

    if args.dry_run:
        print("DRY RUN (aucune suppression):")
        for rid, label in DUPLICATES_TO_DELETE:
            print(f"  - {rid}  {label}")
        return

    print("Suppression en cours...")
    success = 0
    for rid, label in DUPLICATES_TO_DELETE:
        if delete_record(token, rid, label):
            success += 1

    print()
    print(f"Resultat: {success}/{len(DUPLICATES_TO_DELETE)} supprimes")


if __name__ == "__main__":
    main()
