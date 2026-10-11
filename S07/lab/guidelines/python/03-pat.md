# Python — 3. Pattern e modularità (`PAT`)

### PY-PAT-01 [CONSIGLIATA] Input espliciti con argparse
- DO: parametri (file, cartelle, soglie, host) come argomenti con `help` e default sensati; `-o/--output-dir` per l'output.
- DO NOT: valori scritti nel corpo del codice; `input()` interattivo (blocca cron e CI).
- Perché: lo stesso script gira su più host e in cron senza modifiche.
- Verifica: `python3 -m <pacchetto> --help` elenca tutti i parametri.
Esempio: `p.add_argument("--soglia", type=int, default=80, help="%% disco oltre cui allarmare")`

### PY-PAT-02 [CONSIGLIATA] Dati su stdout, diagnostica su stderr con `logging`
- DO: risultato su stdout o su file; log con `logging` su stderr; `-v` alza il livello a DEBUG.
- DO NOT: `print()` di debug mescolati ai dati; log su stdout.
- Perché: l'output deve poter finire in una pipe, in un file o in un altro tool.
- Verifica: `python3 -m <pacchetto> ... 2>/dev/null | python3 -m json.tool` (se l'output è JSON).
Esempio: `logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO, format="%(levelname)s %(message)s")`

### PY-PAT-03 [CONSIGLIATA] pathlib, non stringhe di percorso
- DO: `Path(...)`, `path.open(...)`, `read_text()`, `/` per comporre, `path.stem` per il nome senza estensione.
- DO NOT: concatenare percorsi con `+`; `os.path` misto a `Path`; `os.system("cat ...")`.
- Perché: meno errori su separatori e spazi nei nomi.
- Verifica: `ruff check --select PTH`.
Esempio: `out = args.output_dir / f"{log_path.stem}.json"`

### PY-PAT-04 [CONSIGLIATA] Logica separata da I/O
- DO: funzioni pure per parsing e calcolo (ricevono righe/dati, restituiscono dati); lettura file, rete e scrittura solo in `main()` o in funzioni dedicate.
- DO NOT: una funzione che apre il file, analizza, chiama l'endpoint e scrive il risultato.
- Perché: la logica si testa con una lista di stringhe, senza file, rete o processi.
- Verifica: manuale in review (i test di PY-TST-03 non usano `tmp_path` per la logica).
Esempio:
```python
def parse(righe: Iterable[str]) -> list[Evento]: ...
def aggrega(eventi: list[Evento]) -> dict: ...
def main(argv=None) -> int:
    with args.log.open(encoding="utf-8", errors="replace") as f:
        scrivi_json(aggrega(parse(f)), out)
```

### PY-PAT-05 [CONSIGLIATA] Lettura dei log in streaming
- DO: iterare riga per riga (`for n, riga in enumerate(f, start=1)`), conservando il numero di riga; contatori con `collections.Counter`.
- DO NOT: `f.read()` / `readlines()` su log di dimensione ignota.
- Perché: un log di produzione può pesare GB; il numero di riga serve per verificare le citazioni.
- Verifica: `grep -nE "\.read\(\)|readlines\(" *.py` vuoto sui percorsi di lettura log.

### PY-PAT-06 [CONSIGLIATA] Regex compilate, con gruppi nominati e testate
- DO: `re.compile` a livello di modulo, ancorate (`^...`), con gruppi nominati; un test per formato su righe reali (fixture).
- DO NOT: regex "plausibili" mai provate su righe vere; parsing con `split()` e indici posizionali su formati liberi.
- Perché: le regex sono il punto più fragile del parsing di log; una regex sbagliata scarta in silenzio metà delle righe.
- Verifica: `pytest -q` con fixture per ogni formato (PY-TST-03).
Esempio: `SSHD = re.compile(r"^(?P<mese>\w{3})\s+(?P<giorno>\d+) (?P<ora>[\d:]+) (?P<host>\S+) sshd\[(?P<pid>\d+)\]: (?P<msg>.*)$")`

### PY-PAT-07 [CONSIGLIATA] Output JSON con contratto stabile
- DO: schema scritto (docstring o `SPEC.md`); stesse chiavi sempre presenti, `null` se il valore manca; `json.dump(dati, f, ensure_ascii=False, indent=2)`; date ISO 8601 con fuso.
- DO NOT: chiavi che compaiono solo a volte; date naive (`datetime.now()`); cambiare nomi di campo senza aggiornare lo schema.
- Perché: il JSON è l'input dello step successivo (altro script, modello, report): se cambia forma, quello si rompe.
- Verifica: `ruff check --select DTZ` + test che rilegge il JSON e controlla le chiavi (PY-TST-02).
Esempio: `"generato": datetime.now(timezone.utc).isoformat(timespec="seconds")`
