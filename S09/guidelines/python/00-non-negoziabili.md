# Python — 0. Regole non negoziabili
- PY-VER-01 Solo libreria standard a runtime, Python 3.10+ dichiarato
- PY-ERR-01 Exit code significativi: 0 ok, 1 problema rilevato, 2 errore
- PY-ERR-02 Nessun errore ignorato in silenzio (niente `except: pass`)
- PY-OPS-01 Dry-run di default per ogni script che modifica qualcosa
- PY-SEC-01 Segreti solo da variabili d'ambiente, mai in codice/argomenti/log
- PY-SEC-02 Comandi esterni come lista, mai `shell=True`; input non fidato mai eseguito (PY-SEC-04)
- PY-TST-01 `ruff format --check . && ruff check .` e `pytest -q` a zero errori prima di dichiarare finito
