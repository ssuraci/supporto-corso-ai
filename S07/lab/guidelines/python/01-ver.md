# Python — 1. Versioni, stile e struttura (`VER`)

### PY-VER-01 [BLOCCANTE] Solo libreria standard, versione dichiarata
- DO: usare `argparse`, `pathlib`, `subprocess`, `json`, `logging`, `re`, `csv`, `urllib.request`, `datetime`, `tempfile`, `shutil`, `socket`.
- DO: dichiarare `requires-python = ">=3.10"` in `pyproject.toml`; strumenti di sviluppo (pytest, ruff) pinnati in `requirements-dev.txt` (`pytest==8.3.3`, `ruff==0.6.9`).
- DO NOT: aggiungere dipendenze pip per ciò che la stdlib già fa (`requests`, `psutil`, `click`, `python-dotenv`); mai versioni non pinnate o `latest`.
- Perché: sul server target spesso non c'è pip né rete; ogni dipendenza è da installare, aggiornare e verificare.
- Verifica: `python3 -m <pacchetto> --help` in un venv con il solo `requirements-dev.txt` funziona; `grep -vE '^\s*(#|$)|==' requirements-dev.txt` non stampa nulla.

### PY-VER-02 [CONSIGLIATA] Struttura standard dello script
- DO: shebang `#!/usr/bin/env python3`, docstring di 1-3 righe (cosa fa, input, exit code), funzioni piccole, `main(argv)` che restituisce l'exit code.
- DO NOT: codice eseguito all'import; variabili globali modificate a runtime.
- Perché: lo script si legge dall'alto in basso e i test chiamano `main([...])` senza lanciare processi.
- Verifica: `python3 -c "import <modulo>"` non produce output né effetti.
Esempio:
```python
#!/usr/bin/env python3
"""Controlla lo spazio disco. Exit: 0 ok, 1 soglia superata, 2 errore."""


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    ...


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        raise SystemExit(130)
```

### PY-VER-03 [CONSIGLIATA] Sorgenti in `src/`, test in `tests/`
- DO: codice sempre in `src/`, test sempre in `tests/` (con `fixtures/`), alla radice del progetto. Script semplice: `src/<nome>.py`. Oltre ~300 righe: pacchetto `src/<pacchetto>/` con `__init__.py`, `__main__.py` (solo `main()`) e un modulo per responsabilità (lettura, parsing, aggregazione, output). Nomi importabili in `snake_case`, senza trattini.
- DO: avvio con `PYTHONPATH=src python3 -m <pacchetto>` (i comandi `python3 -m <pacchetto>` di queste linee guida vanno intesi così); `pythonpath = ["src"]` in pytest (PY-TST-01).
- DO NOT: sorgenti e test mescolati nella radice; un file unico di 800 righe; moduli `utils.py` / `helpers.py` generici.
- Perché: separazione netta tra ciò che si esegue e ciò che lo verifica; chi rivede trova subito dove sta il parser di un formato; i test importano il codice come farebbe un utente.
- Verifica: `ls` della radice mostra `src/` e `tests/`; `pytest -q` importa il codice senza hack su `sys.path`.
Esempio:
```
src/logscan/  __init__.py  __main__.py  parsers.py  aggregate.py  output.py
tests/        fixtures/  test_parsers.py  test_cli.py
pyproject.toml  requirements-dev.txt  .gitignore
```

### PY-VER-04 [CONSIGLIATA] Nomi, type hint e costanti
- DO: `snake_case`, nomi parlanti (`soglia_percento`, `righe_scartate`); type hint sulle firme; costanti di configurazione (soglie, pesi, timeout) in MAIUSCOLO in testa al modulo.
- DO NOT: nomi di una lettera (tranne indici brevi); numeri "magici" sparsi nel codice.
- Perché: chi rivede non è un programmatore; nome e costante devono spiegare lo scopo.
- Verifica: `ruff check --select N` + manuale in review per le costanti.
Esempio: `TIMEOUT_HARNESS_S = 300` · `PESI = {"correttezza": 0.4, "fedelta": 0.25}`

### PY-VER-05 [CONSIGLIATA] Encoding esplicito
- DO: `encoding="utf-8"` su ogni apertura di file; per log di terzi anche `errors="replace"`.
- DO NOT: affidarsi all'encoding di default del sistema.
- Perché: lo stesso script su un host con locale diverso legge male o va in `UnicodeDecodeError` alla prima riga sporca.
- Verifica: `ruff check --select PLW1514 --preview` non segnala nulla.
Esempio: `with path.open(encoding="utf-8", errors="replace") as f:`

### PY-VER-06 [CONSIGLIATA] Commenti esplicativi sul codice generato
- DO: commentare in italiano il *perché* dei blocchi non ovvi (regex, soglie, `subprocess`, gestione errori, scelte di sicurezza); una riga per ogni funzione che spieghi cosa fa e cosa restituisce (docstring); spiegare ogni costante di configurazione (unità e origine del valore).
- DO NOT: commentare l'ovvio (`i += 1  # incrementa`); lasciare commenti non aggiornati al codice; usare i commenti per disattivare codice.
- Perché: chi rivede e mantiene lo script è un sistemista, non un programmatore: deve capire cosa fa e perché senza rileggere tutto il codice.
- Verifica: manuale in review; `ruff check --select D1` segnala le docstring mancanti.
Esempio:
```python
SOGLIA_DISCO_PERCENTO = 85  # oltre questa % l'alert scatta (valore concordato col team Run)

def parse_riga(riga: str) -> dict | None:
    """Estrae timestamp e livello da una riga di log; None se il formato non è riconosciuto."""
    # il livello è sempre tra parentesi quadre: [ERROR] ...
    m = RE_LIVELLO.match(riga)
```
