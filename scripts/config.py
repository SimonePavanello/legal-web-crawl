"""
Configurazione comune per tutti gli script di crawling
"""
import sys
import os
from pathlib import Path

# --- PERCORSI ---
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent

# Leggi OpenWPM da variabile d'ambiente
OPENWPM_PATH_STR = os.getenv('OPENWPM_PATH')
if OPENWPM_PATH_STR:
    OPENWPM_PATH = Path(OPENWPM_PATH_STR)
    print(f"[✓] OpenWPM path da variabile d'ambiente: {OPENWPM_PATH}")
else:
    OPENWPM_PATH = PROJECT_ROOT / "OpenWPM"
    if OPENWPM_PATH.exists():
        print(f"[✓] OpenWPM path locale: {OPENWPM_PATH}")
    else:
        print(f"[!] ERRORE: OpenWPM non trovato!")
        print(f"[?] Imposta: export OPENWPM_PATH='/path/to/OpenWPM'")
        sys.exit(1)

if str(OPENWPM_PATH) not in sys.path:
    sys.path.insert(0, str(OPENWPM_PATH))

os.environ['OBJC_DISABLE_INITIALIZE_FORK_SAFETY'] = 'YES'

# --- IMPORT OPENWPM ---
try:
    from openwpm.config import BrowserParams, ManagerParams
    from openwpm.command_sequence import CommandSequence
    from openwpm.task_manager import TaskManager
    from openwpm.storage.sql_provider import SQLiteStorageProvider
    from openwpm.commands.browser_commands import GetCommand
    from openwpm.commands.types import BaseCommand
    from selenium.webdriver.common.by import By
    print(f"[✓] OpenWPM caricato correttamente")
except ImportError as e:
    print(f"[!] ERRORE import OpenWPM: {e}")
    sys.exit(1)

# --- FIREFOX ---
def find_firefox():
    """Trova Firefox automaticamente"""
    firefox_paths = [
        "/Applications/Firefox Developer Edition.app/Contents/MacOS/firefox",
        "/Applications/Firefox.app/Contents/MacOS/firefox",
        "/Applications/Firefox Nightly.app/Contents/MacOS/firefox",
        OPENWPM_PATH / "firefox-bin" / "firefox",
    ]
    
    firefox_env = os.getenv('FIREFOX_BINARY')
    if firefox_env and os.path.exists(firefox_env):
        return firefox_env
    
    for path in firefox_paths:
        if os.path.exists(str(path)):
            return str(path)
    
    return None

FIREFOX_BINARY = find_firefox()
if FIREFOX_BINARY:
    os.environ["FIREFOX_BINARY"] = FIREFOX_BINARY
    print(f"[✓] Firefox trovato: {FIREFOX_BINARY}")
else:
    print(f"[!] ERRORE: Firefox non trovato")
    sys.exit(1)

# --- ESTENSIONE ---
EXTENSION_PATH = OPENWPM_PATH / "openwpm.xpi"
if not EXTENSION_PATH.exists():
    EXTENSION_PATH = OPENWPM_PATH / "Extension" / "openwpm.xpi"

if EXTENSION_PATH.exists():
    print(f"[✓] Estensione trovata: {EXTENSION_PATH}")
else:
    print(f"[!] ATTENZIONE: Estensione non trovata")
    EXTENSION_PATH = None

# --- LISTA SITI DA FILE ---
def load_sites_from_file(filepath=None):
    """
    Carica la lista di siti da un file di testo.
    
    Args:
        filepath: Path al file (default: PROJECT_ROOT/sites.txt)
    
    Returns:
        Lista di URL
    """
    if filepath is None:
        filepath = PROJECT_ROOT / "sites.txt"
    else:
        filepath = Path(filepath)
    
    if not filepath.exists():
        print(f"[!] ERRORE: File siti non trovato: {filepath}")
        print(f"[?] Crea il file con un URL per riga")
        sys.exit(1)
    
    sites = []
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            # Ignora righe vuote e commenti
            if line and not line.startswith('#'):
                sites.append(line)
    
    print(f"[✓] Caricati {len(sites)} siti da {filepath}")
    return sites

# Carica i siti
SITES = load_sites_from_file()

# --- CONFIGURAZIONE BROWSER BASE ---
def get_browser_params(display_mode="headless", use_extension=True):
    """
    Crea configurazione browser standard
    
    Args:
        display_mode: "headless", "native", o "xvfb"
        use_extension: Se True carica l'estensione OpenWPM
    
    Returns:
        Lista con BrowserParams configurato
    """
    browser_params = [BrowserParams(display_mode=display_mode)]
    
    if use_extension and EXTENSION_PATH:
        browser_params[0].extension_paths = [str(EXTENSION_PATH)]
    
    browser_params[0].http_instrument = True
    browser_params[0].cookie_instrument = True
    browser_params[0].js_instrument = True
    browser_params[0].navigation_instrument = True
    browser_params[0].tp_cookies = "always"
    browser_params[0].bot_mitigation = True
    
    return browser_params