import sys
import os
import shutil
import time
from pathlib import Path

# --- LOGICA DI RILEVAMENTO PERCORSI (PORTABILE) ---
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
OPENWPM_PATH = PROJECT_ROOT / "OpenWPM"

if str(OPENWPM_PATH) not in sys.path:
    sys.path.append(str(OPENWPM_PATH))

DATA_DIR = PROJECT_ROOT / "output" / "rejected"
# --------------------------------------------------

try:
    from openwpm.config import BrowserParams, ManagerParams
    from openwpm.command_sequence import CommandSequence
    from openwpm.task_manager import TaskManager
    from openwpm.storage.sql_provider import SQLiteStorageProvider
    from openwpm.commands.browser_commands import GetCommand
    from openwpm.commands.types import BaseCommand
    from selenium.webdriver.common.by import By
    print(f"[✓] OpenWPM caricato correttamente da {OPENWPM_PATH}")
except ImportError as e:
    print(f"[!] ERRORE: {e}")
    sys.exit(1)

# Configurazione binari
os.environ["FIREFOX_BINARY"] = str(OPENWPM_PATH / "firefox-bin" / "firefox")
EXTENSION_PATH = OPENWPM_PATH / "openwpm.xpi"


def click_reject_button(webdriver):
    """
    Funzione custom da eseguire nel browser per cliccare il pulsante reject.
    """
    try:
        print("         [*] Ricerca pulsante reject...")
        time.sleep(3)  # Aspetta che il banner appaia
        
        # Lista di selettori XPath per trovare pulsanti reject
        selectors = [
            # Testo in italiano/inglese (case-insensitive)
            "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'rifiuta')]",
            "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'reject')]",
            "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'decline')]",
            "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'only necessary')]",
            "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'solo necessari')]",
            "//a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'reject')]",
            "//a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'rifiuta')]",
            "//div[@role='button'][contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'reject')]",
            
            # ID e classi comuni
            "//*[@id='onetrust-reject-all-handler']",
            "//*[contains(@class, 'reject-all')]",
            "//*[contains(@class, 'decline-all')]",
            "//*[@data-action='reject']",
            "//*[@data-testid='reject-button']",
            "//*[contains(@aria-label, 'Reject')]",
            "//*[contains(@aria-label, 'Rifiuta')]",
        ]
        
        for selector in selectors:
            try:
                elements = webdriver.find_elements(By.XPATH, selector)
                
                for element in elements:
                    try:
                        # Verifica se l'elemento è visibile e cliccabile
                        if element.is_displayed() and element.is_enabled():
                            # Scroll verso l'elemento
                            webdriver.execute_script("arguments[0].scrollIntoView(true);", element)
                            time.sleep(0.3)
                            
                            # Prova click normale
                            try:
                                element.click()
                                print(f"         [✓] Pulsante reject cliccato!")
                                time.sleep(2)
                                return
                            except:
                                # Fallback: click con JavaScript
                                webdriver.execute_script("arguments[0].click();", element)
                                print(f"         [✓] Pulsante reject cliccato (JS)!")
                                time.sleep(2)
                                return
                    except:
                        continue
            except:
                continue
        
        print("         [!] Nessun pulsante reject trovato")
        
    except Exception as e:
        print(f"         [!] Errore durante il click: {e}")


def take_screenshot(webdriver, screenshot_path):
    """
    Salva uno screenshot manualmente.
    """
    try:
        webdriver.save_screenshot(screenshot_path)
        print(f"         [✓] Screenshot salvato: {screenshot_path}")
    except Exception as e:
        print(f"         [!] Errore screenshot: {e}")


class CustomFunctionCommand(BaseCommand):
    """
    Comando custom per eseguire una funzione Python nel contesto del browser.
    """
    def __init__(self, function_handle, *args):
        self.function_handle = function_handle
        self.args = args
    
    def __repr__(self):
        return f"CustomFunctionCommand({self.function_handle.__name__})"
    
    def execute(
        self,
        webdriver,
        browser_params,
        manager_params,
        extension_socket,
    ):
        if self.args:
            self.function_handle(webdriver, *self.args)
        else:
            self.function_handle(webdriver)


def main():
    if DATA_DIR.exists():
        shutil.rmtree(DATA_DIR)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    # Crea cartella screenshots
    screenshots_dir = DATA_DIR / "screenshots"
    screenshots_dir.mkdir(exist_ok=True)
    
    db_path = DATA_DIR / "rejected.sqlite"
    storage_provider = SQLiteStorageProvider(str(db_path))
    
    manager_params = ManagerParams(num_browsers=1)
    manager_params.data_directory = DATA_DIR
    manager_params.log_path = DATA_DIR / "openwpm.log"
    
    browser_params = [BrowserParams(display_mode="native")]
    if EXTENSION_PATH.exists():
        browser_params[0].extension_paths = [str(EXTENSION_PATH)]

    # Strumentazione
    browser_params[0].http_instrument = True
    browser_params[0].cookie_instrument = True
    browser_params[0].js_instrument = True
    browser_params[0].navigation_instrument = True

    sites = [
        "https://microsoft.com", 
        "https://facebook.com", 
        "https://cloudflare.com", 
        "https://mail.ru", 
        "https://youtube.com", 
        "https://apple.com", 
        "https://instagram.com"
    ]

    print(f"\n[*] FASE 2: REJECT CRAWL (Interazione Automatica)")
    print(f"[*] Output: {DATA_DIR}")
    print(f"[*] Database: {db_path}\n")
    
    manager = TaskManager(manager_params, browser_params, storage_provider, None)

    try:
        for i, url in enumerate(sites, 1):
            print(f"[{i}/{len(sites)}] Navigazione + Rifiuto: {url}")
            try:
                command_sequence = CommandSequence(url, reset=True)
                
                # 1. Naviga al sito e aspetta che carichi
                command_sequence.append_command(GetCommand(url=url, sleep=5))
                
                # 2. Esegui la funzione custom per cliccare reject
                command_sequence.append_command(CustomFunctionCommand(click_reject_button))
                
                # 3. Aspetta un po' dopo il click per raccogliere traffico
                command_sequence.append_command(GetCommand(url=url, sleep=3))
                
                # 4. Screenshot manuale
                site_id = url.split("//")[-1].replace(".", "_").replace("/", "")
                screenshot_path = screenshots_dir / f"rejected_{site_id}.png"
                command_sequence.append_command(
                    CustomFunctionCommand(take_screenshot, str(screenshot_path))
                )
                
                manager.execute_command_sequence(command_sequence)
                print(f"         [✓] Completato\n")
                
            except Exception as e:
                print(f"         [✗] Errore su {url}: {e}\n")
                import traceback
                traceback.print_exc()
                
    except KeyboardInterrupt:
        print("\n[!] Interrotto dall'utente.")
    finally:
        manager.close()
        print(f"\n[*] Crawl completato. Dati salvati in: {db_path}")


if __name__ == "__main__":
    main()