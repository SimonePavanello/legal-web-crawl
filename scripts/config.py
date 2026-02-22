"""
Configurazione comune per tutti gli script di crawling
"""
import sys
import os
from pathlib import Path
import time
import re


def heartbeat_wait(driver, duration_sec=60):
    """Funzione di attesa con heartbeat per evitare crash del driver"""
    print(f"         [*] Osservazione in corso ({duration_sec}s)...")
    steps = int(duration_sec / 5)
    for _ in range(steps):
        try:
            _ = driver.current_url 
            time.sleep(5)
        except Exception:
            break

def save_manual_screenshot(webdriver, path):
    """Gestore universale per gli screenshot"""
    try:
        webdriver.save_screenshot(str(path))
        print(f"         [✓] Screenshot salvato in: {path}")
    except Exception as e:
        print(f"         [!] Errore screenshot: {e}")

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
def get_browser_params(display_mode="headless", use_extension=True, num_browsers=1):
    browser_params = []
    
    for i in range(num_browsers):
        # Crea una nuova istanza per ogni browser
        bp = BrowserParams(display_mode=display_mode)
        
        # Configurazione comune a tutte le istanze
        bp.http_instrument = True
        bp.cookie_instrument = True
        bp.js_instrument = True
        bp.navigation_instrument = True
        bp.tp_cookies = "always"
        bp.bot_mitigation = True
        
        if use_extension and EXTENSION_PATH:
            bp.extension_paths = [str(EXTENSION_PATH)]
            
        # Aggiunge l'istanza alla lista
        browser_params.append(bp)
    
    return browser_params

class CustomFunctionCommand(BaseCommand):
    """Comando universale per eseguire funzioni Python nel browser"""
    def __init__(self, function_handle, *args):
        self.function_handle = function_handle
        self.args = args
    
    def __repr__(self):
        return f"CustomFunctionCommand({self.function_handle.__name__})"
    
    def execute(self, webdriver, browser_params, manager_params, extension_socket):
        if self.args:
            self.function_handle(webdriver, *self.args)
        else:
            self.function_handle(webdriver)

def get_screenshot_path(url, phase_name, directory):
    """
    Compone un path pulito: output/{fase}/screenshots/{fase}_{dominio}.png
    """
    # 1. Estrae il dominio e rimuove caratteri non sicuri
    # Esempio: https://aws.amazon.com/it/ -> aws_amazon_com
    clean_name = re.sub(r'https?://', '', url)
    clean_name = re.sub(r'[^\w\s-]', '_', clean_name).strip('_')
    clean_name = clean_name.split('_it')[0] # Opzionale: accorcia i path localizzati
    
    # 2. Crea il nome file: es. "rejected_aws_amazon_com.png"
    filename = f"{phase_name}_{clean_name}.png"
    
    # 3. Restituisce il path completo
    return Path(directory) / filename