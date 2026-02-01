import sys
import os
import asyncio
import time
from pathlib import Path

# 1. SETUP PATH
OPENWPM_PATH = "/Users/pava/Documents/Workspace/Repos/OpenWPM/"
sys.path.append(OPENWPM_PATH)

from openwpm.config import BrowserParams, ManagerParams
from openwpm.task_manager import TaskManager
from openwpm.storage.sql_provider import SQLiteStorageProvider
from openwpm.storage.local_storage import LocalArrowProvider

# Impostazioni Ambiente
os.environ["FIREFOX_BINARY"] = "/Applications/Firefox Developer Edition.app/Contents/MacOS/firefox"
os.environ["OPENWPM_ROOT_DIRECTORY"] = "/Users/pava/Documents/Workspace/Repos/OpenWPM"

async def main():
    # CANCELLIAMO IL VECCHIO DB PER EVITARE CONFLITTI
    db_path = Path("analisi_baseline.sqlite").resolve()
    if db_path.exists():
        db_path.unlink()
    
    unstructured_dir = Path("crawl_data").resolve()
    unstructured_dir.mkdir(exist_ok=True)
    
    structured_provider = SQLiteStorageProvider(str(db_path))
    unstructured_provider = LocalArrowProvider(str(unstructured_dir))

    manager_params = ManagerParams(num_browsers=1)
    browser_params_template = BrowserParams()
    browser_params_template.preferences = {
        "xpinstall.signatures.required": False,
        "extensions.checkCompatibility.nightly": False,
    }

    sites = [
        "gtld-servers.net",
        "microsoft.com",
        "facebook.com",
        "cloudflare.com"
        "googleapis.com"
        "mail.ru",
        "youtube.com",
        "apple.com",
        "amazonaws.com",
        "instagram.com"
    ]





    manager = TaskManager(
        manager_params,
        structured_storage_provider=structured_provider,
        unstructured_storage_provider=unstructured_provider,
        browser_params_temp=[browser_params_template] 
    )

    try:
        for url in sites:
            print(f"[*] Navigazione su: {url}")
            manager.browse(url)
            # Attendiamo 40 secondi per ogni sito
            await asyncio.sleep(40) 

    except Exception as e:
        print(f"\n[!] Errore durante il crawl: {e}")
    finally:
        print("[*] Chiusura in corso... Attendere 10 secondi per il salvataggio...")
        # Chiudiamo in modo sicuro senza await se non necessario
        try:
            res = manager.close()
            if asyncio.iscoroutine(res):
                await res
        except Exception as close_error:
            print(f"[*] Nota: Chiusura manuale eseguita ({close_error})")
        
        # Lasciamo il tempo al sistema di scrivere l'indice del database
        time.sleep(10)

    print(f"\n[!] Crawl terminato con successo. Database: {db_path}")

if __name__ == "__main__":
    asyncio.run(main())