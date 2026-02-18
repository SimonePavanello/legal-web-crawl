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

DATA_DIR = PROJECT_ROOT / "output" / "rejected"

def click_reject_button(webdriver):
    """
    Funzione custom da eseguire nel browser per cliccare il pulsante reject.
    """
    try:
        print("         [*] Ricerca pulsante reject...")
        time.sleep(3)  # Aspetta che il banner appaia
        
        # Lista di selettori XPath per trovare pulsanti reject
        selectors = [

                    # --- NOVITÀ: Ricerca testuale universale (molto più forte) ---
            "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'declino')]",
            "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'decline optional cookies')]",
            "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'rifiuta cookie facoltativi')]",
            
            # --- SPECIFICO PER FACEBOOK ---
            # Facebook usa spesso l'attributo aria-label per i bottoni dei cookie
            "//div[@role='button'][@aria-label='Decline optional cookies']",
            "//div[@role='button'][@aria-label='Rifiuta cookie facoltativi']",
            "//button[@data-cookiebanner='accept_only_essential_button']", # ID interno di Meta
            
            # --- SPECIFICO PER AWS ---
            # Il bottone di AWS spesso ha ID dinamici, ma possiamo puntare al testo nel link
            "//a[contains(., 'Declino')]",
            "//button[contains(., 'Declino')]",
            # Testo in italiano/inglese (case-insensitive)
            "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'rifiuta')]",
            "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'reject')]",
            "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'declino')]",
            "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'decline')]",
            "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'only necessary')]",
            "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'solo necessari')]",
            "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'Rifiuta cookies facoltativi')]",
            "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'Decline optional cookies')]",
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
            "//*[contains(@aria-label, 'Continua senza accettare')]",
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




def main():
    # 1. Setup Directory specifica per REJECT
    if DATA_DIR.exists():
        shutil.rmtree(DATA_DIR)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    # Crea cartella screenshots
    screenshots_dir = DATA_DIR / "screenshots"
    screenshots_dir.mkdir(exist_ok=True)
    
    db_path = DATA_DIR / "rejected.sqlite"
    storage_provider = SQLiteStorageProvider(str(db_path))
    
    # 2. Configurazione Manager
    manager_params = ManagerParams(num_browsers=1)
    manager_params.data_directory = DATA_DIR
    manager_params.log_path = DATA_DIR / "openwpm.log"
    
    # 3. Configurazione Browser usando la funzione helper di config.py
    browser_params = get_browser_params(display_mode="headless", use_extension=True)
    
    # Carica siti da file
    SITES = load_sites_from_file()

    print(f"\n{'='*60}")
    print(f"[*] PROGETTO: {PROJECT_ROOT.name}")
    print(f"[*] FASE 2: REJECT CRAWL (Click su Rifiuta)")
    print(f"[*] Destinazione Dati: {DATA_DIR}")
    print(f"[*] Database: {db_path}")
    print(f"{'='*60}\n")
    
    manager = TaskManager(manager_params, browser_params, storage_provider, None)

    try:
        for i, url in enumerate(SITES, 1):
            print(f"[{i}/{len(SITES)}] Navigazione + Rifiuto: {url}", flush=True)
            try:
                command_sequence = CommandSequence(url, reset=True, blocking=True)
                
                # 1. Naviga al sito e aspetta che carichi
                command_sequence.append_command(GetCommand(url=url, sleep=10), timeout=120)
                
                # 2. Esegui la funzione custom per cliccare reject
                command_sequence.append_command(CustomFunctionCommand(click_reject_button), timeout=60)
                
                # 3. Aspetta un po' dopo il click per raccogliere traffico
                command_sequence.append_command(CustomFunctionCommand(heartbeat_wait),timeout=120)
                
                # 4. Screenshot manuale
                screenshot_path = get_screenshot_path(url, "reject", screenshots_dir)
                command_sequence.append_command(CustomFunctionCommand(save_manual_screenshot, screenshot_path))
     
                manager.execute_command_sequence(command_sequence)
                print(f"         [✓] Successo: Dati e Screenshot salvati", flush=True)
                
            except Exception as e:
                print(f"         [✗] Errore su {url}: {e}", flush=True)
                
    except KeyboardInterrupt:
        print("\n[!] Interrotto manualmente.")
    finally:
        manager.close()
        print(f"\n[*] Reject crawl terminata. I dati sono pronti in: {DATA_DIR}")


if __name__ == "__main__":
    main()