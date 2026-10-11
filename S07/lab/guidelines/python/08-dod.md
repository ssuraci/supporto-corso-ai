# Python — 8. Errori tipici dell'AI e Definition of done

**Errori tipici** (indice):
- librerie inventate o non necessarie (`requests`, `psutil`, `python-dotenv`), versioni non pinnate → PY-VER-01
- codice eseguito all'import, `sys.exit()` sparsi → PY-VER-02, PY-ERR-01
- `open()` senza `encoding`, crash alla prima riga non UTF-8 → PY-VER-05
- URL o IP dell'endpoint scritti nel codice → PY-ENV-01
- funzione unica che legge, analizza, chiama la rete e scrive → PY-PAT-04
- `f.read()` / `readlines()` su un log intero → PY-PAT-05
- regex scritte "a occhio" e mai provate su righe vere → PY-PAT-06
- chiavi JSON presenti solo a volte, date senza fuso → PY-PAT-07
- exit 0 anche a errore → PY-ERR-01
- `except Exception: pass` o `except` allargato per far passare un test → PY-ERR-02
- `subprocess.run` / `urlopen` senza `timeout` → PY-ERR-03
- righe non analizzate scartate senza conteggio → PY-ERR-04
- `0`, `""` o token "stimati" al posto di un errore → PY-ERR-05
- retry infinito o su errori 4xx → PY-ERR-06
- stdout di un comando usato senza controllarne l'esito → PY-ERR-07
- modifica diretta senza anteprima → PY-OPS-01
- script che appende/riavvia a ogni run, o due istanze in cron → PY-OPS-02, PY-OPS-05
- `input()` o valori fissi al posto di argomenti → PY-PAT-01
- JSON scritto direttamente sul file finale, output sopra l'input → PY-OPS-03, PY-OPS-04
- password nel codice o in `--password` → PY-SEC-01
- `subprocess.run(f"... {x}", shell=True)` → PY-SEC-02
- `chmod 777` → PY-SEC-03
- `eval()` sulla risposta del modello, percorsi del modello usati senza controllo → PY-SEC-04
- log grezzi inviati a un endpoint cloud → PY-SEC-05
- `ssl._create_unverified_context()` per aggirare un errore di certificato → PY-SEC-06
- codice generato senza commenti/docstring che spieghino il perché → PY-VER-06
- `# noqa` aggiunto senza motivo → PY-TST-01
- test indebolito, rimosso o che chiama la rete vera → PY-TST-02, PY-TST-04

**Definition of done**:
- [ ] `ruff format --check . && ruff check .` a zero errori (config di PY-TST-01)
- [ ] `pytest -q` passato, offline
- [ ] `python3 -m <pacchetto> --help` elenca tutti i parametri e le variabili d'ambiente
- [ ] exit code 0/1/2 coperti dai test
- [ ] dry-run verificato senza effetti (N/A se sola lettura)
- [ ] seconda run con `--apply` = 0 modifiche (N/A se sola lettura)
- [ ] output JSON rilegge con `json.loads` e rispetta lo schema (N/A se nessun JSON)
- [ ] funzioni con docstring e blocchi non ovvi commentati (PY-VER-06)
- [ ] nessun segreto nel diff né nei file di output
