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
    Logica a tre fasi: Accept Diretto -> Settings -> Accept nel Sottomenu.
    Ottimizzata per evitare click inutili su siti standard e sbloccare banner complessi.
    """
    
    # --- 1. KEYWORDS PER ACCETTAZIONE (IT, EN, RU) ---
    accept_keys = [
        'accetta', 'accept', 'acconsento', 'agree', 'autorizzo', 'ho capito', 'ok',
        'allow all', 'accetta tutto', 'принять', 'согласен', 'разрешить', 'принять все'
    ]
    
    # --- 2. KEYWORDS PER SETTINGS (se l'accetta tutto è nascosto) ---
    settings_keys = [
        'settings', 'personalizza', 'manage', 'opzioni', 'options', 
        'impostazioni', 'настройки', 'показать все', 'параметры', 'подробнее'
    ]

    def find_and_click(keywords):
        """Cerca e clicca basandosi su una lista di parole, includendo span e scroll centrato"""
        # Cerchiamo in button, a, div[role=button] e span
        elements = webdriver.find_elements(By.XPATH, "//button | //a | //div[@role='button'] | //span")
        for el in elements:
            try:
                if el.is_displayed():
                    text = el.text.lower()
                    if any(k in text for k in keywords):
                        # Scroll centrato per assicurarci che l'elemento sia nel viewport
                        webdriver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
                        time.sleep(0.5)
                        try:
                            el.click()
                        except:
                            # Fallback con JavaScript se il click standard è bloccato da overlay
                            webdriver.execute_script("arguments[0].click();", el)
                        return True, text
            except:
                continue
        return False, ""

    try:
        print("         [*] Fase 1: Tentativo di Accept diretto...")
        success, clicked_text = find_and_click(accept_keys)
        
        if success:
            print(f"         [✓] Accept diretto riuscito: '{clicked_text}'")
            return

        print("         [*] Fase 2: Accept diretto non trovato. Cerco Settings/Personalizza...")
        success, clicked_text = find_and_click(settings_keys)
        
        if success:
            print(f"         [+] Entrato in Settings tramite: '{clicked_text}'")
            time.sleep(3) # Attesa per il caricamento del sottomenu
            
            print("         [*] Fase 3: Tentativo di Accept nel sottomenu...")
            success_sub, clicked_text_sub = find_and_click(accept_keys)
            if success_sub:
                print(f"         [✓] Accept sottomenu riuscito: '{clicked_text_sub}'")
                return
            else:
                print("         [!] Settings aperti, ma tasto Accept non trovato all'interno")
        else:
            print("         [!] Nessun tasto Accept o Settings trovato")

    except Exception as e:
        print(f"         [!] Errore durante la procedura di Accept: {e}")


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