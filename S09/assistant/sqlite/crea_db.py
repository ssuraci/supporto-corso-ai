"""Crea sqlite/eventi.db: incident in corso e manutenzioni programmate delle VM.

Uso (dalla radice):  python sqlite/crea_db.py
Serve a sapere se su una VM c'è un incident o una manutenzione: si cerca per ip_vm.
Dati di test inventati (IP del blocco 203.0.113.0/24, riservato alla documentazione).
Ricrea il file da zero a ogni esecuzione.
"""

import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent / "eventi.db"

# Una sola tabella per due tipi di evento: la domanda è sempre la stessa (cosa succede
# su questa VM?). Date in ISO 8601: ordinabili e confrontabili anche come testo.
# CHECK: il database rifiuta valori fuori elenco invece di fidarsi di chi scrive.
SCHEMA = """
CREATE TABLE eventi (
    id          INTEGER PRIMARY KEY,
    tipo        TEXT NOT NULL CHECK (tipo IN ('incident', 'manutenzione')),
    ip_vm       TEXT NOT NULL,
    titolo      TEXT NOT NULL,
    data_inizio TEXT NOT NULL,   -- quando è iniziato / inizierà
    eta         TEXT NOT NULL,   -- fine stimata (ETA)
    CHECK (eta >= data_inizio)
);
CREATE INDEX idx_eventi_ip ON eventi (ip_vm);
"""

# (tipo, ip_vm, titolo, data_inizio, eta)
# Date pensate per il giorno del corso, 13 ottobre 2026 (orario di lezione: 9-18):
# .11 e .25 hanno eventi IN CORSO, .10 ha un incident già concluso (12/10) e una
# manutenzione futura, .30 e .31 hanno solo manutenzioni PROGRAMMATE.
DATI = [
    (
        "incident",
        "203.0.113.10",
        "Disco pieno: la VM non risponde al login SSH",
        "2026-10-12 08:30",
        "2026-10-12 14:00",
    ),
    (
        "incident",
        "203.0.113.11",
        "Rete degradata sul nodo ospitante: pacchetti persi",
        "2026-10-13 06:15",
        "2026-10-13 23:00",
    ),
    (
        "incident",
        "203.0.113.25",
        "Storage lento: latenza elevata sui dischi",
        "2026-10-12 22:40",
        "2026-10-14 06:00",
    ),
    (
        "manutenzione",
        "203.0.113.10",
        "Aggiornamento kernel e riavvio",
        "2026-10-15 02:00",
        "2026-10-15 04:00",
    ),
    (
        "manutenzione",
        "203.0.113.30",
        "Migrazione al nuovo cluster di virtualizzazione",
        "2026-10-14 23:00",
        "2026-10-15 03:00",
    ),
    (
        "manutenzione",
        "203.0.113.31",
        "Estensione del volume di storage",
        "2026-10-20 01:00",
        "2026-10-20 02:30",
    ),
    (
        "manutenzione",
        "203.0.113.11",
        "Sostituzione scheda di rete del nodo",
        "2026-10-13 08:00",
        "2026-10-13 22:00",
    ),
]


def main():
    DB.unlink(missing_ok=True)
    with sqlite3.connect(DB) as con:
        con.executescript(SCHEMA)
        con.executemany(
            "INSERT INTO eventi (tipo, ip_vm, titolo, data_inizio, eta)"
            " VALUES (?, ?, ?, ?, ?)",
            DATI,
        )
    # Controllo: gli eventi di una VM, i più vicini per primi.
    with sqlite3.connect(DB) as con:
        righe = con.execute(
            "SELECT tipo, titolo, data_inizio, eta FROM eventi"
            " WHERE ip_vm = ? ORDER BY data_inizio",
            ("203.0.113.10",),
        ).fetchall()
    print(f"{DB.name}: {len(DATI)} eventi. Esempio 203.0.113.10:")
    for r in righe:
        print("  ", r)


if __name__ == "__main__":
    main()
