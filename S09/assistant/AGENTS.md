# CLAUDE.md

## Cos'è

`assistant` è un CLI Python che analizza le richieste di supporto di un data center e risponde
sempre nello stesso formato.

## Comandi

```bash
python -m assistant.main "<richiesta>"          # dalla radice del progetto
python -m assistant.main --json "<richiesta>"   # stampa solo il JSON
pytest                                          # solo logica Python: mai rete, mai modello
pytest -m reale                                 # solo a mano: modelli, Qdrant e database veri (esclusi di default)
pytest -m reale tests/test_cerca_kb_reale.py tests/test_cerca_incident_reale.py   # solo i retriever sul RAG esistente, senza LLM
ruff format --check . && ruff check .           # stile e lint
python qdrant/popola_qdrant.py                  # SOLO docente: ricarica aruba-kb (al corso il RAG esiste già)
python qdrant/popola_past_incidents.py          # SOLO docente: ricarica aruba-past-incidents
python qdrant/smoke_test.py                     # smoke test Qdrant (chiave in sola lettura)
python llm_test/smoke_test.py                   # smoke test accesso ai modelli (base e evoluto)
python sqlite/crea_db.py                        # (una tantum) crea sqlite/eventi.db
python assistant/rag_test/prova_retriever.py "domanda"   # prova a mano dei due retriever
```

Exit code: `0` risposta normale o rifiuto · `1` errore dei modelli · `2` configurazione o uso.

## Configurazione

`.env` in radice (mai nel repository): `OPENAI_BASE_URL`, `OPENAI_API_KEY`,
`LLM_MODEL_BASE`, `LLM_MODEL_ADVANCED`, `QDRANT_ENDPOINT`, `QDRANT_API_KEY_RO` (sola lettura,
usata dai tool: è l'unica chiave Qdrant che serve ai partecipanti) e `QDRANT_API_KEY` (con
scrittura, solo docente, per gli script `qdrant/popola_*.py`). Al corso (13 ottobre 2026) il
RAG Qdrant è già popolato e condiviso: non si ricarica.
Il dettaglio per passo è in [spec/README.md](spec/README.md).

## Workflow (lineare con rami)

- **P0** verifica che i modelli (base e evoluto) rispondano.
- **P1** rifiuta ciò che non è supporto tecnico.
- **P2** classifica tipo, priorità e servizio; il codice sceglie il ramo con `choose_branch`.
  È l'unico passo col modello base (economico): tutti gli altri usano l'evoluto.
- Ramo **informazioni (P3)**: agente col tool `cerca_kb` (retrieve su Qdrant, collection
  `aruba-kb`, soglia di punteggio); fonti = URL dei passaggi trovati.
- Ramo **sicurezza (P4)**: rifiuto fisso ("non posso fornire informazioni"), senza modello né tool.
- Ramo **supporto (P5)**: agente con i tool `stato_vm` (database SQLite: la VM con quell'IP ha
  un incident o una manutenzione?) e, se non c'è un evento pertinente, `cerca_incident`
  (Qdrant, collection `aruba-past-incidents`) per incident simili e soluzione.
- **P6** *(stretch, non fatto)*: sotto-agente con la skill di diagnostica per VM con IP.
- **P7** assembla la risposta di ogni ramo nel formato comune
  `Risposta(tipo, priorita, servizio, ramo, modello, risposta, fonti, diagnostica)`
  (`diagnostica` è sempre vuota finché P6 non esiste). Il rifiuto di P1 resta fuori formato.

## Struttura

- `common/` — unico accesso all'LLM (`get_llm()`), modelli Pydantic e tool riusabili di sola
  lettura (`cerca_kb`, `cerca_incident`, `stato_vm`). Nessun altro modulo istanzia un LLM.
  `strumenti.py` (`leggi_documentazione`) è un tool locale di esempio, fuori dal flusso.
- `assistant/` — un modulo per passo; `main.py` fa solo orchestrazione. `rag_test/` contiene
  le prove a mano dei retriever (non fanno parte dei test).
- `qdrant/` — script che creano e popolano le collection Qdrant (`aruba-kb`,
  `aruba-past-incidents`); `qdrant.txt` e `qdrant-read-only.txt` contengono chiavi: non pubblicarli.
- `sqlite/` — `crea_db.py` e `eventi.db` (incident e manutenzioni per IP di VM).
- `spec/` — la guida del corso, **da seguire nell'ordine di `spec/README.md`**: per passo
  `SPEC.md` e `PIANO.md` (e `BRAINSTORM.md` dove c'è). I passi `dati-*` preparano i dati.
  `spec/PROMPT_DI_PROVA.md` raccoglie i prompt da provare con le risposte reali.
- `tests/` — cartella dedicata ai test, uno per passo (`test_pN.py`), solo offline con
  modello e tool finti; `*_reale.py` sono a mano (`pytest -m reale`).
- `data/` — snapshot Aruba (`data/aruba/<servizio>/documentazione.txt`, sorgente di
  `aruba-kb`) e script `aggiorna_aruba.py`. Incident finti e diagnostica campione: non
  presenti (gli incident stanno in Qdrant, la diagnostica è lo stretch P6).
- `skill/` e `inventory/` — da S04, **non ancora presenti**: servono solo allo stretch P6.
- `guidelines/` — linee guida per strumento (vedi sotto).

## Guidelines

Prima di scrivere o modificare codice leggi le linee guida in [guidelines/](guidelines/):
formato in `guidelines/guidelines-kit-format.md`, regole per strumento in
`guidelines/python.md` e `guidelines/langchain.md` (e `guidelines/python/`).
Le spec nuove partono da `guidelines/spec.template.md`.

## Regola: commenti nel codice

Commenta estensivamente il codice in tutte le sue parti più importanti (prompt, scelta del
ramo, gestione errori ed exit code, accessi al modello): spiega il **perché** delle scelte,
non solo cosa fa la riga. Chi legge è un sistemista, non un programmatore.

## Regola: PROGRESS.md

**Ogni modifica va loggata in `PROGRESS.md`** (data, cosa è cambiato, file toccati), nello
stesso passo in cui la fai.
