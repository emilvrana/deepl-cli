#!/usr/bin/env python3
"""DeepL Translation API wrapper.

Usage:
  translate.py <text> --target <lang> [--source <lang>] [--formality <level>]
  translate.py --file <path> --target <lang> [--source <lang>] [--formality <level>]
  translate.py --languages
  translate.py --usage

Environment: DEEPL_API_KEY must be set.
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.parse
import urllib.error

BASE_URL = "https://api.deepl.com/v2"
API_KEY = os.environ.get("DEEPL_API_KEY", "")


def _request(endpoint, params=None, method="POST"):
    url = f"{BASE_URL}/{endpoint}"
    headers = {
        "Authorization": f"DeepL-Auth-Key {API_KEY}",
        "Content-Type": "application/json",
    }
    if params:
        data = json.dumps(params).encode()
    else:
        data = None
        method = "GET"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"Error {e.code}: {body}", file=sys.stderr)
        sys.exit(1)


def translate(text, target, source=None, formality=None):
    params = {"text": [text], "target_lang": target.upper()}
    if source:
        params["source_lang"] = source.upper()
    if formality:
        params["formality"] = formality
    result = _request("translate", params)
    for t in result.get("translations", []):
        detected = t.get("detected_source_language", "?")
        print(f"[{detected} → {target.upper()}]")
        print(t["text"])


def usage():
    # GET request
    headers = {"Authorization": f"DeepL-Auth-Key {API_KEY}"}
    req = urllib.request.Request(f"{BASE_URL}/usage", headers=headers)
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read())
    for p in data.get("products", []):
        ptype = p.get("product_type", "unknown")
        used = p.get("character_count", 0) if ptype == "translate" else p.get("api_key_unit_count", 0)
        print(f"  {ptype}: {used:,} used")
    print(f"  Total characters: {data.get('character_count', 0):,} / {data.get('character_limit', 0):,}")


def languages(lang_type="target"):
    headers = {"Authorization": f"DeepL-Auth-Key {API_KEY}"}
    req = urllib.request.Request(f"{BASE_URL}/languages?type={lang_type}", headers=headers)
    with urllib.request.urlopen(req, timeout=10) as resp:
        langs = json.loads(resp.read())
    for l in langs:
        print(f"  {l['language']:6s} {l['name']}")


def main():
    parser = argparse.ArgumentParser(description="DeepL Translation")
    parser.add_argument("text", nargs="?", help="Text to translate")
    parser.add_argument("-t", "--target", help="Target language code (e.g. EN-US, DE, CS, RU)")
    parser.add_argument("-s", "--source", help="Source language code (auto-detected if omitted)")
    parser.add_argument("-f", "--file", help="Translate text from file")
    parser.add_argument("--formality", choices=["default", "more", "less", "prefer_more", "prefer_less"],
                        help="Formality level")
    parser.add_argument("--languages", action="store_true", help="List supported languages")
    parser.add_argument("--usage", action="store_true", help="Show API usage stats")

    args = parser.parse_args()

    if not API_KEY:
        print("Error: DEEPL_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    if args.usage:
        usage()
        return

    if args.languages:
        languages()
        return

    text = args.text
    if args.file:
        with open(args.file) as f:
            text = f.read()

    if not text:
        parser.print_help()
        sys.exit(1)

    if not args.target:
        print("Error: --target is required for translation", file=sys.stderr)
        sys.exit(1)

    translate(text, args.target, args.source, args.formality)


if __name__ == "__main__":
    main()
