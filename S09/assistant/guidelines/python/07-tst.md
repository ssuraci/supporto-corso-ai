# Python — 7. Testing e qualità (`TST`)

### PY-TST-01 [BLOCCANTE] Format, lint e test a zero errori
- DO: configurazione in `pyproject.toml` (sotto) e i comandi `ruff format --check . && ruff check . && pytest -q`.
- DO NOT: `# noqa` o `ignore` nuovi senza motivo scritto accanto (per le CONSIGLIATE: `# deroga: <ID> — motivo`); disattivare regole per far passare il lint.
- Perché: intercetta gli errori tipici prima dell'esecuzione, con le stesse regole per tutti.
- Verifica: i tre comandi sopra, exit 0.
Esempio:
```toml
[project]
requires-python = ">=3.10"
[tool.ruff]
target-version = "py310"
[tool.ruff.lint]
select = ["E", "F", "B", "S", "N", "PTH", "BLE", "DTZ"]
# S603/S607: subprocess a lista con comandi di sistema è il pattern voluto (PY-SEC-02)
# S310: urlopen verso l'endpoint configurato (PY-ENV-01); lo schema http(s) lo valida argparse
ignore = ["S603", "S607", "S310"]
[tool.ruff.lint.per-file-ignores]
"tests/*" = ["S101"]  # assert è il modo di scrivere i test pytest
[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]  # i test importano da src/ (PY-VER-03)
```

### PY-TST-02 [CONSIGLIATA] Test dei contratti della CLI
- DO: in `tests/test_cli.py`, chiamando `main([...])`: caso ok (exit 0), caso problema (exit 1), input errato o file mancante (exit 2); dry-run senza effetti; JSON prodotto valido e con tutte le chiavi dello schema; seconda run identica alla prima.
- DO NOT: modificare o indebolire un test per farlo passare; toccare `/etc`, servizi o file reali (usare `tmp_path`).
- Perché: prova che i contratti su cui si appoggiano cron e step successivi reggono.
- Verifica: `pytest -q`.
Esempio:
```python
def test_scrive_json(tmp_path):
    assert main([str(FIXTURE / "sshd_10.log"), "-o", str(tmp_path)]) == 0
    dati = json.loads((tmp_path / "sshd_10.json").read_text(encoding="utf-8"))
    assert {"log", "righe_totali", "righe_scartate", "anomalie"} <= dati.keys()
```

### PY-TST-03 [CONSIGLIATA] Fixture piccole, reali e con i casi sporchi
- DO: in `tests/fixtures/` 10-50 righe vere per formato, più i casi limite: file vuoto, riga troncata, riga non UTF-8, riga di formato diverso.
- DO NOT: inventare righe "pulite" che il parser passa per costruzione; usare log di produzione non anonimizzati.
- Perché: i bug del parsing stanno nelle righe sporche, non in quelle di esempio.
- Verifica: manuale in review (esiste almeno una fixture con riga malformata per formato).

### PY-TST-04 [CONSIGLIATA] Dipendenze esterne finte, mai rete nei test
- DO: sostituire harness, modelli ed endpoint con un finto: uno script in `tests/` lanciato con `sys.executable`, oppure `monkeypatch` sulla funzione che chiama la rete; coprire successo, errore, timeout e risposta non valida.
- DO NOT: chiamare l'endpoint vero, internet o un modello nei test; `time.sleep` reali (patchare o usare timeout di pochi decimi).
- Perché: i test devono passare offline, in pochi secondi e sempre allo stesso modo.
- Verifica: `pytest -q` con la rete disattivata (es. `unshare -rn pytest -q`).
Esempio: `monkeypatch.setattr(judge, "chiama_modello", lambda *a, **k: '{"score": 0.8, "reason": "ok"}')`
