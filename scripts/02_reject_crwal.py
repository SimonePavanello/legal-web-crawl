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
OPENWPM_PATH = PROJECT_ROOT / "OpenWPM"

# Aggiunge OpenWPM al percorso di ricerca di Python
if str(OPENWPM_PATH) not in sys.path:
    sys.path.append(str(OPENWPM_PATH))

# Definisce la cartella di output (legal-web-crawl/output/rejected)
DATA_DIR = PROJECT_ROOT / "output" / "rejected"
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
os.environ["FIREFOX_BINARY"] = str(OPENWPM_PATH / "firefox-bin" / "firefox")
EXTENSION_PATH = OPENWPM_PATH / "openwpm.xpi"

def main():
    if DATA_DIR.exists():
        shutil.rmtree(DATA_DIR)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    db_path = DATA_DIR / "rejected.sqlite"
    storage_provider = SQLiteStorageProvider(str(db_path))
    
    manager_params = ManagerParams(num_browsers=1)
    manager_params.data_directory = DATA_DIR
    manager_params.log_path = DATA_DIR / "openwpm.log"
    
    browser_params = [BrowserParams(display_mode="headless")]
    if EXTENSION_PATH.exists():
        browser_params[0].extension_paths = [str(EXTENSION_PATH)]

    browser_params[0].http_instrument = True
    browser_params[0].cookie_instrument = True
    browser_params[0].js_instrument = True
    browser_params[0].navigation_instrument = True

    sites = [
        "https://gtld-servers.net", "https://microsoft.com",
        "https://facebook.com", "https://cloudflare.com",
        "https://googleapis.com", "https://mail.ru",
        "https://youtube.com", "https://apple.com",
        "https://amazonaws.com", "https://instagram.com"
    ]

    print(f"\n{'='*60}")
    print(f"[*] FASE 2: REJECT CRAWL (CONSENSO NEGATO)")
    print(f"[*] Obiettivo: Rilevare violazione V3 (tracciamento post-rifiuto)")
    print(f"{'='*60}\n")

    manager = TaskManager(manager_params, browser_params, storage_provider, None)

    # Keyword ottimizzate per coprire più varianti
    reject_keywords = [
        "Rifiuta", "Reject", "Solo necessari", "Only necessary", 
        "Non accetto", "Decline", "Personalizza", "Manage settings",
        "scelta dei cookie", "Cookie settings"
    ]

    try:
        for i, url in enumerate(sites, 1):
            print(f"[{i}/{len(sites)}] Navigazione + Tentativo Rifiuto: {url}")
            try:
                command_sequence = CommandSequence(url, reset=True)
                command_sequence.get(sleep=10) # Tempo extra per caricamento banner pesanti

                # Loop di interazione: proviamo a cliccare i bottoni trovati
                for kw in reject_keywords:
                    # XPath migliorato: cerca il testo ignorando parzialmente la posizione
                    # e coprendo Button, A, Span e Div (comuni nei banner custom)
                    xpath = (f"//button[contains(text(), '{kw}')] | "
                             f"//a[contains(text(), '{kw}')] | "
                             f"//div[contains(text(), '{kw}') and @role='button']")
                    
                    command_sequence.click_element(xpath)
                
                # Pausa post-click: fondamentale per vedere se partono richieste HTTP 
                # come reazione alla "scelta" dell'utente
                command_sequence.sleep(25)
                
                # Screenshot per verificare se il banner è effettivamente sparito
                site_id = url.split("//")[-1].replace(".", "_").replace("/", "")
                command_sequence.save_screenshot(f"rejected_{site_id}")
                
                manager.execute_command_sequence(command_sequence)
                print(f"         [✓] Interazione completata")
                
            except Exception as e:
                print(f"         [✗] Errore su {url}: {e}")
                
    except KeyboardInterrupt:
        print("\n[!] Interrotto.")
    finally:
        manager.close()
        print(f"\n[*] Reject Crawl terminato. Database: {db_path}")

if __name__ == "__main__":
    main()