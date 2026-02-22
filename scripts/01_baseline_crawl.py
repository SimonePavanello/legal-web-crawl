import shutil
from pathlib import Path

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
    CustomFunctionCommand,
    heartbeat_wait,
    save_manual_screenshot,
    get_screenshot_path,
)

DATA_DIR = PROJECT_ROOT / "output" / "baseline"

def main():
    if DATA_DIR.exists():
        shutil.rmtree(DATA_DIR)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    screenshots_dir = DATA_DIR / "screenshots"
    screenshots_dir.mkdir(exist_ok=True)
    
    db_path = DATA_DIR / "baseline.sqlite"
    storage_provider = SQLiteStorageProvider(str(db_path))
    
    manager_params = ManagerParams(num_browsers=1)
    manager_params.data_directory = DATA_DIR
    manager_params.log_path = DATA_DIR / "openwpm.log"
    
    browser_params = get_browser_params(display_mode="headless", use_extension=True)
    
    SITES = load_sites_from_file()

    print(f"\n{'='*60}")
    print(f"[*] PROGETTO: {PROJECT_ROOT.name}")
    print(f"[*] FASE 1: BASELINE (NESSUNA SCELTA)")
    print(f"[*] Obiettivo: Rilevare violazioni V1 e V2")
    print(f"[*] Database: {db_path}")
    print(f"{'='*60}\n")

    manager = TaskManager(manager_params, browser_params, storage_provider, None)

    try:
        for i, url in enumerate(SITES, 1):
            print(f"[{i}/{len(SITES)}] Analisi pre-consenso: {url}", flush=True)
            try:
                command_sequence = CommandSequence(url, reset=True, blocking=True)
                
                command_sequence.append_command(GetCommand(url=url, sleep=10), timeout=120)
                
                command_sequence.append_command(CustomFunctionCommand(heartbeat_wait), timeout=120)
                
                screenshot_path = get_screenshot_path(url, "baseline", screenshots_dir)
                command_sequence.append_command(CustomFunctionCommand(save_manual_screenshot, screenshot_path))
                
                manager.execute_command_sequence(command_sequence)
                print(f"         [✓] Successo: Dati pre-consenso raccolti", flush=True)
                
            except Exception as e:
                print(f"         [✗] Errore su {url}: {e}", flush=True)
                
    except KeyboardInterrupt:
        print("\n[!] Interrotto manualmente.")
    finally:
        manager.close()
        print(f"\n[*] Baseline terminata. I dati sono pronti in: {DATA_DIR}")

if __name__ == "__main__":
    main()