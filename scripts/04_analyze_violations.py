#!/usr/bin/env python3
"""
GDPR Cookie Violation Analyzer
Analizza i database OpenWPM per rilevare violazioni V1, V2, V3.

Uso: python3 scripts/04_analyze_violations.py
Dipendenze: pip install tldextract requests
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path

import requests
import tldextract

# ---------------------------------------------------------------------------
# Percorsi
# ---------------------------------------------------------------------------
SCRIPT_DIR   = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent

DB_BASELINE = PROJECT_ROOT / "output" / "baseline" / "baseline.sqlite"
DB_REJECTED = PROJECT_ROOT / "output" / "rejected" / "rejected.sqlite"

OUTPUT_DIR       = PROJECT_ROOT / "output"
REPORT_PATH      = OUTPUT_DIR / "report.md"
DISCONNECT_CACHE = OUTPUT_DIR / "disconnect_cache.json"
SITES_FILE       = PROJECT_ROOT / "sites.txt"

DISCONNECT_URL = (
    "https://raw.githubusercontent.com/disconnectme/"
    "disconnect-tracking-protection/master/services.json"
)
TRACKER_CATEGORIES = {
    "Advertising", "Analytics", "Social",
    "FingerprintingInvasive", "FingerprintingGeneral",
}


# ---------------------------------------------------------------------------
# Utilità
# ---------------------------------------------------------------------------

def load_sites_from_file() -> list[str]:
    sites = []
    with open(SITES_FILE) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                sites.append(line)
    return sites


def _parse_disconnect(data: dict) -> dict[str, str]:
    """Ritorna {domain: category} per le categorie tracker rilevanti.

    Formato Disconnect.me:
      categories.Advertising = [
        {"CompanyName": {"https://homepage/": ["domain1.com", "domain2.com"]}},
        ...
      ]
    """
    tracker_map: dict[str, str] = {}
    for cat_name, company_list in data.get("categories", {}).items():
        if cat_name not in TRACKER_CATEGORIES:
            continue
        # Normalizza il nome categoria per il report
        display_cat = cat_name.replace("FingerprintingInvasive", "Fingerprinting") \
                              .replace("FingerprintingGeneral", "Fingerprinting")
        for company_entry in company_list:
            # company_entry è un dict con una sola chiave (nome azienda)
            for _company_name, homepage_dict in company_entry.items():
                for _homepage, domain_list in homepage_dict.items():
                    for domain in domain_list:
                        d = domain.lower().strip()
                        if d and d not in tracker_map:
                            tracker_map[d] = display_cat
    return tracker_map


def load_tracker_list() -> dict[str, str]:
    """Scarica e/o legge dalla cache la lista tracker Disconnect.me."""
    # Usa la cache se fresca (< 7 giorni)
    if DISCONNECT_CACHE.exists():
        age = datetime.now().timestamp() - DISCONNECT_CACHE.stat().st_mtime
        if age < 7 * 86400:
            data = json.loads(DISCONNECT_CACHE.read_text())
            result = _parse_disconnect(data)
            print(f"      [cache] {len(result)} domini tracker caricati.")
            return result

    # Scarica
    try:
        resp = requests.get(DISCONNECT_URL, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        DISCONNECT_CACHE.write_text(json.dumps(data, indent=2))
        print(f"      [download] Disconnect.me aggiornata.")
    except Exception as e:
        if DISCONNECT_CACHE.exists():
            print(f"      [!] Download fallito ({e}), uso cache stale.")
            data = json.loads(DISCONNECT_CACHE.read_text())
        else:
            raise RuntimeError(f"Impossibile scaricare la tracker list: {e}")

    result = _parse_disconnect(data)
    print(f"      {len(result)} domini tracker caricati.")
    return result


def get_etld1(url_or_host: str) -> str:
    cleaned = url_or_host.lstrip(".")
    ext = tldextract.extract(cleaned)
    # top_domain_under_public_suffix è il nome aggiornato di registered_domain
    return ext.top_domain_under_public_suffix or ext.registered_domain


def is_third_party(cookie_host: str, site_url: str) -> bool:
    cookie_etld1 = get_etld1(cookie_host)
    site_etld1   = get_etld1(site_url)
    if not cookie_etld1 or not site_etld1:
        return False
    return cookie_etld1 != site_etld1


def format_expiry(expiry, is_session: int) -> str:
    if is_session or (expiry and "9999" in str(expiry)):
        return "session"
    if expiry:
        return str(expiry)[:10]
    return "?"


# ---------------------------------------------------------------------------
# Analisi
# ---------------------------------------------------------------------------

SQL_COOKIES = """
SELECT sv.site_url, jc.host, jc.name, jc.expiry, jc.is_session,
       jc.is_http_only, jc.same_site
FROM site_visits sv
JOIN javascript_cookies jc ON sv.visit_id = jc.visit_id
WHERE jc.record_type = 'added-or-changed'
ORDER BY sv.site_url, jc.host, jc.name
"""

SQL_REQUESTS = """
SELECT sv.site_url, hr.url, hr.resource_type
FROM site_visits sv
JOIN http_requests hr ON sv.visit_id = hr.visit_id
ORDER BY sv.site_url
"""


def analyze_v1_cookies(db_path: Path, sites: list[str]) -> dict[str, list[dict]]:
    """V1: cookie di terze parti nel baseline (prima del consenso)."""
    results: dict[str, list[dict]] = {s: [] for s in sites}
    seen: dict[str, set] = {s: set() for s in sites}

    conn = sqlite3.connect(db_path)
    cur  = conn.cursor()
    cur.execute(SQL_COOKIES)
    for site_url, host, name, expiry, is_session, is_http_only, same_site in cur.fetchall():
        if site_url not in results:
            continue
        if not is_third_party(host, site_url):
            continue
        key = (host.lstrip("."), name)
        if key in seen[site_url]:
            # Aggiorna l'ultimo valore (espiry più recente)
            results[site_url] = [
                c if (c["host"].lstrip("."), c["name"]) != key
                else {"host": host, "name": name,
                      "expiry": format_expiry(expiry, is_session),
                      "is_http_only": bool(is_http_only), "same_site": same_site or "?"}
                for c in results[site_url]
            ]
        else:
            seen[site_url].add(key)
            results[site_url].append({
                "host":        host,
                "name":        name,
                "expiry":      format_expiry(expiry, is_session),
                "is_http_only": bool(is_http_only),
                "same_site":   same_site or "?",
            })
    conn.close()
    return results


def analyze_v2_requests(
    db_path: Path,
    tracker_map: dict[str, str],
    sites: list[str],
) -> dict[str, list[tuple[str, str]]]:
    """V2: richieste HTTP verso tracker nel baseline (prima del consenso)."""
    results: dict[str, list[tuple[str, str]]] = {s: [] for s in sites}
    seen: dict[str, set] = {s: set() for s in sites}

    conn = sqlite3.connect(db_path)
    cur  = conn.cursor()
    cur.execute(SQL_REQUESTS)
    for site_url, req_url, _resource_type in cur.fetchall():
        if site_url not in results:
            continue
        req_etld1 = get_etld1(req_url)
        if req_etld1 and req_etld1 in tracker_map and req_etld1 not in seen[site_url]:
            seen[site_url].add(req_etld1)
            results[site_url].append((req_etld1, tracker_map[req_etld1]))
    conn.close()

    # Ordina per categoria poi dominio
    for site in results:
        results[site].sort(key=lambda x: (x[1], x[0]))
    return results


def analyze_v3(
    db_path: Path,
    tracker_map: dict[str, str],
    sites: list[str],
) -> dict[str, dict]:
    """V3: persistenza dopo il rifiuto (cookie terze parti + tracker)."""
    cookies  = analyze_v1_cookies(db_path, sites)
    trackers = analyze_v2_requests(db_path, tracker_map, sites)
    return {
        site: {
            "cookies":   cookies[site],
            "trackers":  trackers[site],
            "violation": bool(cookies[site] or trackers[site]),
        }
        for site in sites
    }


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

def _site_label(url: str) -> str:
    return url.replace("https://", "").replace("http://", "").rstrip("/")


def _cookies_table(cookie_list: list[dict]) -> str:
    if not cookie_list:
        return "*Nessun cookie di terze parti rilevato.*\n"
    lines = [
        "| Cookie | Host | Scadenza | HttpOnly | SameSite |",
        "|--------|------|----------|----------|----------|",
    ]
    for c in cookie_list:
        lines.append(
            f"| `{c['name']}` | `{c['host']}` | {c['expiry']} "
            f"| {'Sì' if c['is_http_only'] else 'No'} | {c['same_site']} |"
        )
    return "\n".join(lines) + "\n"


def _trackers_list(tracker_list: list[tuple[str, str]]) -> str:
    if not tracker_list:
        return "*Nessun tracker contattato.*\n"
    return "\n".join(f"- `{d}` ({cat})" for d, cat in tracker_list) + "\n"


def generate_report(
    v1: dict[str, list[dict]],
    v2: dict[str, list[tuple]],
    v3: dict[str, dict],
    sites: list[str],
) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines: list[str] = []

    # Intestazione
    lines += [
        "# Report Violazioni GDPR – Cookie Consent Compliance",
        "",
        f"**Data analisi**: {now}  ",
        f"**Siti analizzati**: {len(sites)}  ",
        "**Fonte tracker list**: Disconnect.me (Advertising, Analytics, Social, Fingerprinting)  ",
        "**Definizione cookie non necessari**: cookie il cui eTLD+1 è diverso dal sito visitato",
        "",
        "---",
        "",
    ]

    # Tabella riassuntiva
    lines += [
        "## Tabella Riassuntiva",
        "",
        "| Sito | V1 – Cookie pre-consenso | V2 – Tracker pre-consenso | V3 – Post-rifiuto |",
        "|------|--------------------------|---------------------------|-------------------|",
    ]
    for site in sites:
        v1c = len(v1[site])
        v2c = len(v2[site])
        v3flag = "**SÌ**" if v3[site]["violation"] else "No"
        lines.append(
            f"| {_site_label(site)} "
            f"| {v1c} cookie "
            f"| {v2c} tracker "
            f"| {v3flag} |"
        )
    lines += ["", "---", ""]

    # V1
    lines += [
        "## V1 – Cookie Non Necessari Prima del Consenso",
        "",
        "> Cookie di terze parti rilevati nel crawl **baseline**,",
        "> ossia prima di qualsiasi interazione con il banner di consenso.",
        "",
    ]
    for site in sites:
        lines += [f"### {site}", ""]
        lines.append(_cookies_table(v1[site]))

    lines += ["---", ""]

    # V2
    lines += [
        "## V2 – Contatto con Tracker Prima del Consenso",
        "",
        "> Richieste HTTP verso domini classificati come tracker (Disconnect.me)",
        "> rilevate nel crawl **baseline**, prima di qualsiasi azione di consenso.",
        "",
    ]
    for site in sites:
        lines += [f"### {site}", ""]
        lines.append(_trackers_list(v2[site]))

    lines += ["---", ""]

    # V3
    lines += [
        "## V3 – Persistenza Dopo il Rifiuto del Consenso",
        "",
        "> Attività di tracking rilevata nel crawl **rejected**,",
        "> ovvero dopo che l'utente ha esplicitamente negato il consenso.",
        "",
    ]
    for site in sites:
        v3s = v3[site]
        lines += [f"### {site}", ""]
        if v3s["violation"]:
            lines.append("**Violazione V3 rilevata.**\n")
            lines.append("**Cookie di terze parti impostati dopo il rifiuto:**\n")
            lines.append(_cookies_table(v3s["cookies"]))
            lines.append("**Tracker contattati dopo il rifiuto:**\n")
            lines.append(_trackers_list(v3s["trackers"]))
        else:
            lines.append("*Nessuna violazione V3 rilevata.*\n")

    lines += ["---", ""]

    # Note metodologiche
    lines += [
        "## Note Metodologiche",
        "",
        "- **Cookie non necessari** (V1, V3): cookie il cui eTLD+1 host differisce dall'eTLD+1 "
        "del sito visitato. Identificati con la libreria `tldextract` (Public Suffix List).",
        "- **Domini tracker** (V2, V3): domini presenti nella lista Disconnect.me nelle categorie "
        "Advertising, Analytics, Social, Fingerprinting. Il confronto avviene sul `registered_domain`.",
        "- I cookie sono deduplicati per `(host, nome)` — viene mantenuta l'ultima occorrenza nel log.",
        "- I crawl sono separati (baseline, rejected, accepted): non è disponibile un timestamp "
        "preciso dell'interazione con il banner; i dati di baseline rappresentano lo stato "
        "pre-consenso, quelli di rejected lo stato post-rifiuto.",
        "",
    ]

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def _print_summary(
    v1: dict, v2: dict, v3: dict, sites: list[str]
) -> None:
    print("\n" + "=" * 60)
    print(" SUMMARY VIOLAZIONI GDPR")
    print("=" * 60)
    print(f"{'Sito':<30} {'V1':>4} {'V2':>4} {'V3':>6}")
    print("-" * 60)
    for site in sites:
        label = _site_label(site)[:29]
        v3flag = "SÌ" if v3[site]["violation"] else "No"
        print(f"{label:<30} {len(v1[site]):>4} {len(v2[site]):>4} {v3flag:>6}")
    print("=" * 60)


def main():
    print("[*] GDPR Violation Analyzer – avvio")

    print("[1/5] Caricamento siti...")
    sites = load_sites_from_file()
    print(f"      {len(sites)} siti caricati.")

    print("[2/5] Caricamento lista tracker Disconnect.me...")
    tracker_map = load_tracker_list()

    print("[3/5] Analisi V1 – cookie di terze parti (baseline)...")
    v1 = analyze_v1_cookies(DB_BASELINE, sites)
    total_v1 = sum(len(v) for v in v1.values())
    print(f"      {total_v1} cookie di terze parti trovati.")

    print("[4/5] Analisi V2 – richieste tracker (baseline)...")
    v2 = analyze_v2_requests(DB_BASELINE, tracker_map, sites)
    total_v2 = sum(len(v) for v in v2.values())
    print(f"      {total_v2} contatti con tracker trovati.")

    print("[5/5] Analisi V3 – persistenza dopo rifiuto (rejected)...")
    v3 = analyze_v3(DB_REJECTED, tracker_map, sites)
    total_v3 = sum(1 for v in v3.values() if v["violation"])
    print(f"      {total_v3}/{len(sites)} siti con violazioni V3.")

    print("[*] Generazione report Markdown...")
    report = generate_report(v1, v2, v3, sites)
    REPORT_PATH.write_text(report, encoding="utf-8")
    print(f"[✓] Report salvato in: {REPORT_PATH}")

    _print_summary(v1, v2, v3, sites)


if __name__ == "__main__":
    main()
