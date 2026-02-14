import sys
import os
import shutil
from pathlib import Path

# --- LOGICA DI RILEVAMENTO PERCORSI (PORTABILE) ---
# Identifica la cartella dove si trova questo script (legal-web-crawl/scripts)
SCRIPT_DIR = Path(__file__).resolve().parent

# La radice del progetto è un livello sopra (legal-web-crawl/)
PROJECT_ROOT = SCRIPT_DIR.parent

# OpenWPM ora è DENTRO la tua repo (legal-web-crawl/OpenWPM)
OPENWPM_PATH = "/Users/pava/Documents/Workspace/Repos/OpenWPM"  # Cambia questo percorso se hai spostato la cartella OpenWPM

# Aggiunge OpenWPM al percorso di ricerca di Python
if str(OPENWPM_PATH) not in sys.path:
    sys.path.append(str(OPENWPM_PATH))

# Definisce la cartella di output (legal-web-crawl/output/baseline)
DATA_DIR = PROJECT_ROOT / "output" / "baseline"
# --------------------------------------------------

try:
    from openwpm.config import BrowserParams, ManagerParams
    from openwpm.command_sequence import CommandSequence
    from openwpm.task_manager import TaskManager
    from openwpm.storage.sql_provider import SQLiteStorageProvider
    print(f"[*] OpenWPM caricato correttamente dalla cartella interna!")
except ImportError:
    print(f"[!] ERRORE: Non trovo OpenWPM in {OPENWPM_PATH}")
    print("[?] Hai rimosso la cartella OpenWPM o hai cambiato struttura?")
    sys.exit(1)

# Configurazione binari interni alla repo

FIREFOX_DEV_PATH = "/Applications/Firefox Developer Edition.app/Contents/MacOS/firefox"
if os.path.exists(FIREFOX_DEV_PATH):
    os.environ["FIREFOX_BINARY"] = FIREFOX_DEV_PATH
    print(f"[✓] Firefox Developer Edition trovato")
elif os.path.exists("/Applications/Firefox.app/Contents/MacOS/firefox"):
    os.environ["FIREFOX_BINARY"] = "/Applications/Firefox.app/Contents/MacOS/firefox"
    print(f"[✓] Firefox normale trovato")
elif os.path.exists(OPENWPM_PATH / "firefox-bin" / "firefox"):
    os.environ["FIREFOX_BINARY"] = str(OPENWPM_PATH / "firefox-bin" / "firefox")
    print(f"[✓] Firefox binario interno trovato")
else:
    print(f"[!] ERRORE: Non trovo Firefox in nessuno dei percorsi standard.")
    print("[?] Hai installato Firefox Developer Edition o Firefox normale?")
    print("[?] Hai lasciato il binario di Firefox dentro la cartella OpenWPM?")
    sys.exit(1)


#EXTENSION_PATH = OPENWPM_PATH / "openwpm.xpi"
EXTENSION_PATH = Path("/Users/pava/Documents/Workspace/Repos/OpenWPM/Extension") / "openwpm.xpi"

def main():
    # 1. Setup Directory specifica per BASELINE
    if DATA_DIR.exists():
        shutil.rmtree(DATA_DIR)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    db_path = DATA_DIR / "baseline.sqlite"
    storage_provider = SQLiteStorageProvider(str(db_path))
    
    # 2. Configurazione Manager
    manager_params = ManagerParams(num_browsers=1)
    manager_params.data_directory = DATA_DIR
    manager_params.log_path = DATA_DIR / "openwpm.log"
    
    # 3. Configurazione Browser (Strumentazione Totale)
    browser_params = [BrowserParams(display_mode="headless")]
    
    if EXTENSION_PATH.exists():
        browser_params[0].extension_paths = [str(EXTENSION_PATH)]
        print(f"[*] Estensione trovata e caricata.")
    else:
        print(f"[!] ATTENZIONE: Estensione non trovata in {EXTENSION_PATH}")
    
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
    print(f"[*] PROGETTO: {PROJECT_ROOT.name}")
    print(f"[*] FASE 1: AVVIO BASELINE (NESSUNA SCELTA)")
    print(f"[*] Destinazione Dati: {DATA_DIR}")
    print(f"[*] Database: {db_path}")
    print(f"{'='*60}\n")

    manager = TaskManager(manager_params, browser_params, storage_provider, None)

    try:
        for i, url in enumerate(sites, 1):
            print(f"[{i}/{len(sites)}] Analisi pre-consenso: {url}", flush=True)
            try:
                command_sequence = CommandSequence(url, reset=True)
                
                # Carica pagina e attendi 30 sec per tracciamento silente (V1 e V2)
                command_sequence.get(sleep=30) 
                
                # Screenshot (Richiesto dal docente)
                # Pulisce l'URL per usarlo come nome file
                site_id = url.split("//")[-1].replace(".", "_").replace("/", "")
                command_sequence.save_screenshot(f"screenshot_{site_id}")
                
                manager.execute_command_sequence(command_sequence)
                print(f"         [✓] Successo: Dati e Screenshot salvati", flush=True)
            except Exception as e:
                print(f"         [✗] Errore su {url}: {e}", flush=True)
                
    except KeyboardInterrupt:
        print("\n[!] Interrotto manualmente.")
    finally:
        manager.close()
        print(f"\n[*] Baseline terminata. I dati sono pronti in: {DATA_DIR}")

if __name__ == "__main__":
    main()