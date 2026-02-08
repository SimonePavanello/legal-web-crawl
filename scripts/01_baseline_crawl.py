import sys
import os
import shutil
import sqlite3
from pathlib import Path

# Configurazione Percorsi OpenWPM
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
    # 1. Setup Directory specifica per BASELINE
    data_dir = Path("/home/simone/Workspace/legal-web-crawl/output/baseline").resolve()
    if data_dir.exists():
        shutil.rmtree(data_dir)
    data_dir.mkdir(parents=True, exist_ok=True)
    
    db_path = data_dir / "baseline.sqlite"
    storage_provider = SQLiteStorageProvider(str(db_path))
    
    # 2. Configurazione Manager
    manager_params = ManagerParams(num_browsers=1)
    manager_params.data_directory = data_dir
    manager_params.log_path = data_dir / "openwpm.log"
    
    # 3. Configurazione Browser (Strumentazione Totale)
    browser_params = [BrowserParams(display_mode="headless")]
    
    if os.path.exists(EXTENSION_PATH):
        browser_params[0].extension_paths = [EXTENSION_PATH]
    
    browser_params[0].http_instrument = True
    browser_params[0].cookie_instrument = True
    browser_params[0].js_instrument = True
    browser_params[0].navigation_instrument = True
    browser_params[0].tp_cookies = "always"
    browser_params[0].bot_mitigation = True

       

    sites = [
        "https://gtld-servers.net", "https://microsoft.com",
        "https://facebook.com", "https://cloudflare.com",
        "https://googleapis.com", "https://mail.ru",
        "https://youtube.com", "https://apple.com",
        "https://amazonaws.com", "https://instagram.com"
    ]
    
    print(f"\n{'='*60}")
    print(f"[*] FASE 1: AVVIO BASELINE (NESSUNA SCELTA)")
    print(f"[*] Obiettivo: Rilevare violazioni V1 e V2")
    print(f"[*] Database: {db_path}")
    print(f"{'='*60}\n")

    manager = TaskManager(manager_params, browser_params, storage_provider, None)

    try:
        for i, url in enumerate(sites, 1):
            print(f"[{i}/{len(sites)}] Analisi: {url}", flush=True)
            try:
                command_sequence = CommandSequence(url, reset=True)
                
                # Carica pagina e attendi 30 sec per tracciamento silente
                command_sequence.get(sleep=30) 
                
                # Screenshot (Richiesto dal docente)
                site_id = url.split("//")[-1].replace(".", "_")
                command_sequence.save_screenshot(f"screenshot_{site_id}")
                
                manager.execute_command_sequence(command_sequence)
                print(f"         [✓] Dati e Screenshot salvati", flush=True)
            except Exception as e:
                print(f"         [✗] Errore su {url}: {e}", flush=True)
                
    except KeyboardInterrupt:
        print("\n[!] Interrotto.")
    finally:
        manager.close()
        print("\n[*] Baseline terminata.")

if __name__ == "__main__":
    main()