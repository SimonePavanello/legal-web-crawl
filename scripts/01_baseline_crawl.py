import sys
import os
import shutil
import sqlite3
import asyncio
from pathlib import Path

# Configurazione Percorsi
OPENWPM_ROOT = "/home/simone/Workspace/OpenWPM"
if OPENWPM_ROOT not in sys.path:
    sys.path.append(OPENWPM_ROOT)

try:
    from openwpm.config import BrowserParams, ManagerParams
    from openwpm.command_sequence import CommandSequence
    from openwpm.task_manager import TaskManager
    from openwpm.storage.sql_provider import SQLiteStorageProvider
except ImportError as e:
    print(f"[!] Errore import: {e}. Controlla PYTHONPATH.")
    sys.exit(1)

# Impostazione binario Firefox e estensione
os.environ["FIREFOX_BINARY"] = os.path.join(OPENWPM_ROOT, "firefox-bin/firefox")
EXTENSION_PATH = os.path.join(OPENWPM_ROOT, "openwpm.xpi")

def main():
    # 1. Setup Directory Dati (Evitiamo il cestino!)
    data_dir = Path("/home/simone/Workspace/legal-web-crawl/output_data").resolve()
    if data_dir.exists():
        shutil.rmtree(data_dir)
    data_dir.mkdir(parents=True, exist_ok=True)
    
    db_path = data_dir / "crawl-data.sqlite"
    storage_provider = SQLiteStorageProvider(str(db_path))
    
    # 2. Configurazione Manager
    manager_params = ManagerParams(num_browsers=1)
    manager_params.data_directory = data_dir
    manager_params.log_path = data_dir / "openwpm.log"
    
    # 3. Configurazione Browser con Strumentazione TOTALE
    browser_params = [BrowserParams(display_mode="headless")]
    
    # Attiviamo l'estensione buildata
    if os.path.exists(EXTENSION_PATH):
        print(f"[*] Caricamento estensione da: {EXTENSION_PATH}")
        browser_params[0].extension_paths = [EXTENSION_PATH]
    else:
        print("[!] ATTENZIONE: openwpm.xpi non trovato. Procedo senza estensione.")

    # Strumentazione per analisi legale (GDPR/ePrivacy)
    browser_params[0].http_instrument = True       # Richieste di rete (Tracker)
    browser_params[0].cookie_instrument = True     # Cookie (via Estensione/Headers)
    browser_params[0].js_instrument = True         # Script JS (Fingerprinting)
    browser_params[0].navigation_instrument = True # Flusso di navigazione
    
    # Impostazioni Privacy per "vedere" tutto il tracciamento
    browser_params[0].tp_cookies = "always"        # Accetta cookie di terze parti per loggarli
    browser_params[0].bot_mitigation = True
    
    sites = [
        "https://gtld-servers.net", "https://microsoft.com",
        "https://facebook.com", "https://cloudflare.com",
        "https://googleapis.com", "https://mail.ru",
        "https://youtube.com", "https://apple.com",
        "https://amazonaws.com", "https://instagram.com"
    ]
    
    print(f"\n{'='*60}")
    print(f"[*] AVVIO CRAWL LEGALE - OpenWPM 0.31.0")
    print(f"[*] Database: {db_path}")
    print(f"[*] Modalità: Full Instrumentation (Network + JS + Cookies)")
    print(f"{'='*60}\n")

    manager = TaskManager(manager_params, browser_params, storage_provider, None)

    try:
        for i, url in enumerate(sites, 1):
            print(f"[{i}/{len(sites)}] Navigazione su: {url}", flush=True)
            try:
                # Reset=True pulisce il profilo tra un sito e l'altro per isolare i cookie
                command_sequence = CommandSequence(url, reset=True)
                command_sequence.get(sleep=30) # 30 secondi per permettere ai banner di caricare i tracker
                manager.execute_command_sequence(command_sequence)
                print(f"         [✓] Successo", flush=True)
            except Exception as e:
                print(f"         [✗] Errore: {e}", flush=True)
                
    except KeyboardInterrupt:
        print("\n[!] Interruzione manuale...")
    finally:
        print("\n[*] Chiusura in corso...", flush=True)
        manager.close()
        
    # 4. ANALISI POST-CRAWL (Query Utili per la Tesi)
    if db_path.exists():
        conn = sqlite3.connect(db_path)
        try:
            print(f"\n{'='*60}")
            print(f"📊 REPORT DATI RACCOLTI (SINTESI LEGALE)")
            print(f"{'='*60}")
            
            # Conta richieste a domini terzi (potenziali violazioni)
            n_requests = conn.execute("SELECT COUNT(*) FROM http_requests").fetchone()[0]
            n_cookies = conn.execute("SELECT COUNT(*) FROM javascript_cookies").fetchone()[0]
            
            # Query per individuare i domini di terze parti più frequenti
            print(f"Richieste HTTP totali: {n_requests}")
            print(f"Cookie JS registrati:  {n_cookies}")
            
            print("\nTop 5 domini contattati (potenziali tracker):")
            query = """
                SELECT SUBSTR(url, 1, 30), COUNT(*) as c 
                FROM http_requests 
                GROUP BY 1 ORDER BY c DESC LIMIT 5
            """
            for row in conn.execute(query):
                print(f" - {row[0]}... ({row[1]} richieste)")
                
            print(f"{'='*60}\n")
            
        except Exception as e:
            print(f"[!] Errore durante l'analisi rapida: {e}")
        finally:
            conn.close()

if __name__ == "__main__":
    main()