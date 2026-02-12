#!/usr/bin/env bash
set -e

echo "Installazione di Firefox Developer Edition per OpenWPM..."

# 1. Pulizia cartelle vecchie
rm -rf firefox-bin firefox target.tar.bz2 2>/dev/null || true

# 2. Download della versione Developer Edition (Linux 64-bit, Italiano)
# Questo link è statico e punta sempre all'ultima versione disponibile
URL="https://download.mozilla.org/?product=firefox-devedition-latest-ssl&os=linux64&lang=it"

echo "Scaricamento da Mozilla..."
if ! wget -O target.tar.bz2 "$URL"; then
    echo "Errore nel download. Controlla la tua connessione."
    exit 1
fi

# 3. Estrazione
echo "Estrazione dei file..."
if ! tar jxf target.tar.bz2; then
    echo "Errore nell'estrazione. Assicurati di avere bzip2 installato (sudo apt install bzip2)."
    exit 1
fi

# 4. Configurazione per OpenWPM
# La cartella estratta si chiama sempre 'firefox'
if [ -d "firefox" ]; then
    mv firefox firefox-bin
    echo "-------------------------------------------------------"
    echo "SUCCESSO: Firefox Developer Edition installato!"
    echo "Percorso: $(pwd)/firefox-bin/firefox"
    echo "-------------------------------------------------------"
else
    echo "Errore: Cartella 'firefox' non trovata dopo l'estrazione."
    exit 1
fi

# Pulizia finale
rm target.tar.bz2