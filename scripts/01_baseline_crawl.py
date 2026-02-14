import shutil
from pathlib import Path

# Importa tutta la configurazione comune
from config import (
    PROJECT_ROOT,
    load_sites_from_file,  
    ManagerParams,
    CommandSequence,
    TaskManager,
    SQLiteStorageProvider,
    get_browser_params
)

DATA_DIR = PROJECT_ROOT / "output" / "baseline"

def main():
    SITES = load_sites_from_file()
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
    
    # 3. Configurazione Browser usando la funzione helper di config.py
    browser_params = get_browser_params(display_mode="headless", use_extension=True)
    
    print(f"\n{'='*60}")
    print(f"[*] PROGETTO: {PROJECT_ROOT.name}")
    print(f"[*] FASE 1: BASELINE (NESSUNA SCELTA)")
    print(f"[*] Destinazione Dati: {DATA_DIR}")
    print(f"[*] Database: {db_path}")
    print(f"{'='*60}\n")

    manager = TaskManager(manager_params, browser_params, storage_provider, None)

    try:
        for i, url in enumerate(SITES, 1):
            print(f"[{i}/{len(SITES)}] Analisi pre-consenso: {url}", flush=True)
            try:
                command_sequence = CommandSequence(url, reset=True)
                
                # Carica pagina e attendi 45 sec per tracciamento silente
                command_sequence.get(sleep=30) 
                
                # Screenshot
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