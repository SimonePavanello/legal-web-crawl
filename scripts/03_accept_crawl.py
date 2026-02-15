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
    By,
    CustomFunctionCommand,
    heartbeat_wait,
    save_manual_screenshot,
    get_screenshot_path,
)

# Cambiata la directory di output in "accepted"
DATA_DIR = PROJECT_ROOT / "output" / "accepted"

def click_accept_button(webdriver):
    """
    Funzione custom da eseguire nel browser per cliccare il pulsante di consenso (Accept).
    """
    try:
        print("         [*] Ricerca pulsante accetta...")
        time.sleep(3)  # Aspetta che il banner appaia
        
        # Lista di selettori XPath aggiornati per trovare pulsanti di consenso
        selectors = [
            # Testo in italiano/inglese (case-insensitive)
            "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'accetta')]",
            "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'accept')]",
            "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'acconsento')]",
            "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'agree')]",
            "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'ho capito')]",
            "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'autorizzo')]",
            "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'ok')]",
            "//a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'accetta')]",
            "//div[@role='button'][contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'accetta')]",
            
            # ID e classi comuni per l'accettazione (spesso differiscono dal reject)
            "//*[@id='onetrust-accept-btn-handler']",
            "//*[contains(@class, 'accept-all')]",
            "//*[contains(@class, 'consent-all')]",
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
                                print(f"         [✓] Pulsante accetta cliccato!")
                                time.sleep(2)
                                return
                            except:
                                webdriver.execute_script("arguments[0].click();", element)
                                print(f"         [✓] Pulsante accetta cliccato (JS)!")
                                time.sleep(2)
                                return
                    except:
                        continue
            except:
                continue
        
        print("         [!] Nessun pulsante accetta trovato")
        
    except Exception as e:
        print(f"         [!] Errore durante il click: {e}")

def main():
    # 1. Setup Directory specifica per ACCEPTED
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
            print(f"[{i}/{len(SITES)}] Navigazione + Accetto: {url}", flush=True)
            try:
                command_sequence = CommandSequence(url, reset=True, blocking=True)
                
                # 1. Caricamento iniziale
                command_sequence.append_command(GetCommand(url=url, sleep=10), timeout=120)
                
                # 2. Click su Accetta (Logica inversa rispetto al reject)
                command_sequence.append_command(CustomFunctionCommand(click_accept_button), timeout=60)
                
                # 3. Osservazione post-consenso (heartbeat per evitare crash)
                command_sequence.append_command(CustomFunctionCommand(heartbeat_wait, 60), timeout=120)
                
                # 4. Screenshot per verifica visiva
                screenshot_path = get_screenshot_path(url, "accept", screenshots_dir)
                command_sequence.append_command(CustomFunctionCommand(save_manual_screenshot, screenshot_path))
     
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