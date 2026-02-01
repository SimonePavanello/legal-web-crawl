import sys
sys.path.append("/Users/pava/Documents/Workspace/Repos/OpenWPM")

import openwpm
from openwpm import config

print("--- Ispezione Modulo openwpm ---")
print([item for item in dir(openwpm) if "Config" in item or "Params" in item])

print("\n--- Ispezione Modulo openwpm.config ---")
print([item for item in dir(config) if "Config" in item or "Params" in item])