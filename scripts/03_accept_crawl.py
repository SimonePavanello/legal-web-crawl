import shutil
import time
from pathlib import Path

# Importa dalla configurazione comune
from config import (
    PROJECT_ROOT,
    load_sites_from_file,
    ManagerParams,
    CommandSequence,
    TaskManager,
    SQLiteStorageProvider,
    GetCommand,
    BaseCommand,
    get_browser_params,
    By
)

DATA_DIR = PROJECT_ROOT / "output" / "accepted"

def click_accept_button(webdriver):
    """
    Funzione custom da eseguire nel browser per cliccare il pulsante accept.
    """
    try:
        print("         [*] Ricerca pulsante accept...")
        time.sleep(3)
        
        # Lista di selettori XPath per trovare pulsanti accept
        selectors = [
            # Testo in italiano/inglese (case-insensitive)
            "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'accetta')]",
            "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'accept')]",
            "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'agree')]",
            "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'accept all')]",
            "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'accetta tutti')]",
            "//a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'accept')]",
            "//a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'accetta')]",
            "//div[@role='button'][contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'accept')]",
            
            # ID e classi comuni
            "//*[@id='onetrust-accept-btn-handler']",
            "//*[contains(@class, 'accept-all')]",
            "//*[contains(@class, 'agree-button')]",
            "//*[@data-action='accept']",
            "//*[@data-testid='accept-button']",
            "//*[contains(@aria-label, 'Accept')]",
            "//*[contains(@aria-label, 'Accetta')]",
        ]
        
        for selector in selectors:
            try:
                elements = webdriver.find_elements(By.XPATH, selector)
                
                for element in elements:
                    try:
                        if element.is_displayed() and element.is_enabled():
                            webdriver.execute_script("arguments[0].scrollIntoView(true);", element)
                            time.sleep(0.3)
                            
                            try:
                                element.click()
                                print(f"         [✓] Pulsante accept cliccato!")
                                time.sleep(2)
                                return
                            except:
                                webdriver.execute_script("arguments[0].click();", element)
                                print(f"         [✓] Pulsante accept cliccato (JS)!")
                                time.sleep(2)
                                return
                    except:
                        continue
            except:
                continue
        
        print("         [!] Nessun pulsante accept trovato")
        
    except Exception as e:
        print(f"         [!] Errore durante il click: {e}")


def take_screenshot(webdriver, screenshot_path):
    """Salva uno screenshot manualmente."""
    try:
        webdriver.save_screenshot(screenshot_path)
        print(f"         [✓] Screenshot salvato: {screenshot_path}")
    except Exception as e:
        print(f"         [!] Errore screenshot: {e}")


class CustomFunctionCommand(BaseCommand):
    """Comando custom per eseguire una funzione Python nel contesto del browser."""
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


def main():
    # 1. Setup Directory specifica per ACCEPT
    if DATA_DIR.exists():
        shutil.rmtree(DATA_DIR)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    screenshots_dir = DATA_DIR / "screenshots"
    screenshots_dir.mkdir(exist_ok=True)
    
    db_path = DATA_DIR / "accepted.sqlite"
    storage_provider = SQLiteStorageProvider(str(db_path))
    
    # 2. Configurazione Manager
    manager_params = ManagerParams(num_browsers=1)
    manager_params.data_directory = DATA_DIR
    manager_params.log_path = DATA_DIR / "openwpm.log"
    
    # 3. Configurazione Browser
    browser_params = get_browser_params(display_mode="headless", use_extension=True)
    
    # Carica siti da file
    SITES = load_sites_from_file()

    print(f"\n{'='*60}")
    print(f"[*] PROGETTO: {PROJECT_ROOT.name}")
    print(f"[*] FASE 3: ACCEPT CRAWL (Click su Accetta)")
    print(f"[*] Destinazione Dati: {DATA_DIR}")
    print(f"[*] Database: {db_path}")
    print(f"{'='*60}\n")
    
    manager = TaskManager(manager_params, browser_params, storage_provider, None)

    try:
        for i, url in enumerate(SITES, 1):
            print(f"[{i}/{len(SITES)}] Navigazione + Accetta: {url}", flush=True)
            try:
                command_sequence = CommandSequence(url, reset=True)
                
                command_sequence.append_command(GetCommand(url=url, sleep=5))
                command_sequence.append_command(CustomFunctionCommand(click_accept_button))
                command_sequence.append_command(GetCommand(url=url, sleep=3))
                
                site_id = url.split("//")[-1].replace(".", "_").replace("/", "")
                screenshot_path = screenshots_dir / f"accepted_{site_id}.png"
                command_sequence.append_command(
                    CustomFunctionCommand(take_screenshot, str(screenshot_path))
                )
                
                manager.execute_command_sequence(command_sequence)
                print(f"         [✓] Successo: Dati e Screenshot salvati", flush=True)
                
            except Exception as e:
                print(f"         [✗] Errore su {url}: {e}", flush=True)
                
    except KeyboardInterrupt:
        print("\n[!] Interrotto manualmente.")
    finally:
        manager.close()
        print(f"\n[*] Accept crawl terminata. I dati sono pronti in: {DATA_DIR}")


if __name__ == "__main__":
    main()