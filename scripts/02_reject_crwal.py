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
    Logica a tre fasi: Reject Diretto -> Settings -> Reject nel Sottomenu.
    Ripristina il funzionamento di YouTube/Microsoft e sblocca mail.ru.
    """
    
    # --- 1. KEYWORDS POTENZIATE ---
    reject_keys = [
        'rifiuta', 'reject', 'declino', 'decline', 'solo necessari', 'only necessary',
        'отклонить', 'только обязательные', 'non accetto', 'continua senza accettare',
        'decline optional cookies', 'rifiuta cookie facoltativi'
    ]
    
    settings_keys = [
        'settings', 'personalizza', 'manage', 'opzioni', 'options', 
        'impostazioni', 'настройки', 'показать все', 'параметры', 'подробнее'
    ]

    def find_and_click(keywords):
        """Sotto-funzione per cercare e cliccare basandosi su una lista di parole"""
        # Cerchiamo in button, a, div[role=button] e anche span (spesso il testo è lì)
        elements = webdriver.find_elements(By.XPATH, "//button | //a | //div[@role='button'] | //span")
        for el in elements:
            try:
                if el.is_displayed():
                    text = el.text.lower()
                    if any(k in text for k in keywords):
                        webdriver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
                        time.sleep(0.5)
                        try:
                            el.click()
                        except:
                            webdriver.execute_script("arguments[0].click();", el)
                        return True, text
            except:
                continue
        return False, ""

    try:
        print("         [*] Fase 1: Tentativo di Reject diretto...")
        success, clicked_text = find_and_click(reject_keys)
        
        if success:
            print(f"         [✓] Reject diretto riuscito: '{clicked_text}'")
            return

        print("         [*] Fase 2: Reject diretto fallito. Cerco Settings/Personalizza...")
        success, clicked_text = find_and_click(settings_keys)
        
        if success:
            print(f"         [+] Entrato in Settings tramite: '{clicked_text}'")
            time.sleep(3) # Tempo extra per mail.ru e menu lenti
            
            print("         [*] Fase 3: Tentativo di Reject nel sottomenu...")
            success_sub, clicked_text_sub = find_and_click(reject_keys)
            if success_sub:
                print(f"         [✓] Reject sottomenu riuscito: '{clicked_text_sub}'")
                return
            else:
                print("         [!] Settings aperti, ma tasto Reject non trovato nel menu")
        else:
            print("         [!] Nessun tasto Reject o Settings trovato")

    except Exception as e:
        print(f"         [!] Errore durante la procedura: {e}")



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