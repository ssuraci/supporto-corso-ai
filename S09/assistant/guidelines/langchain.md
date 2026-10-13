# Linee guida LangChain (solo funzionalità di base)

Ambito: esempi didattici piccoli, uno per cartella, costruiti con le **sole
funzionalità di base** di LangChain: modello chat, prompt template, catene LCEL
(`|`), output parser, structured output con Pydantic, tool con `bind_tools`,
`create_agent` (solo negli esempi sugli agenti, LC-VER-04).
Si applicano **in aggiunta** a [python.md](python.md): dove c'è conflitto vince
questo file (vedi LC-VER-01).

## 0. Regole non negoziabili
- LC-VER-01 Un solo set di versioni pinnate, comune a tutti gli esempi (deroga a PY-VER-01)
- LC-VER-02 Solo API di base e attuali: niente API legacy
- LC-ENV-01 Modello ed endpoint da variabili d'ambiente, una sola funzione `crea_modello()`
- LC-ERR-01 `timeout` e `max_retries` sempre impostati sul modello
- LC-OPS-01 Tool in sola lettura di default; tool che modificano = dry-run + approvazione umana
- LC-SEC-01 Output del modello = input non fidato; dati utente mai nel system prompt
- LC-TST-01 Test offline con modello finto; DoD di [python/08-dod.md](python/08-dod.md)

## 1. Versioni, stile e struttura (`VER`)

### LC-VER-01 [BLOCCANTE] Un solo set di versioni, alla radice
- DO: `requirements.txt` e `requirements-dev.txt` **alla radice del progetto**, uguali per tutti gli esempi: `langchain==1.4.4`, `langchain-core==1.6.9`, `langchain-openai==1.7.0`, `pydantic==2.14.0`, `python-dotenv==1.2.4`; dev come PY-VER-01.
- DO NOT: `requirements*.txt` dentro le cartelle degli esempi; versioni diverse tra esempi; versioni non pinnate; nuovi pacchetti senza aggiornare il file della radice.
- Perché: è una deroga mirata a PY-VER-01; un solo venv e una sola versione per tutto il corso, nessuna sorpresa tra un esempio e l'altro.
- Verifica: `grep -vE '^\s*(#|$)|==' requirements*.txt` non stampa nulla; `find . -path ./.venv -prune -o -name 'requirements*.txt' -print` trova solo i file della radice.

### LC-VER-02 [BLOCCANTE] Solo API di base, nella forma attuale
- DO: `ChatOpenAI`, `ChatPromptTemplate`, composizione con `|`, `.invoke()` / `.batch()` / `.stream()`, `StrOutputParser`, `with_structured_output()`, `@tool` + `bind_tools()`, `RunnableLambda`, `RunnableParallel`; `create_agent` alle condizioni di LC-VER-04.
- DO NOT: `LLMChain`, `.run()`, `.predict()`, `initialize_agent`, `AgentExecutor`, classi `Memory`.
- Perché: le API legacy sono rimosse o deprecate e l'AI tende a proporle.
- Verifica: `grep -rnE "LLMChain|\.run\(|\.predict\(|initialize_agent|AgentExecutor|Memory" --include=*.py common/ 0*/` non stampa nulla.

### LC-VER-03 [BLOCCANTE] Lab: ogni cartella = un sorgente + un test, nient'altro
- DO: cartella `NN-nome-breve/` con **solo** il sorgente (es. `verifica_avvio.py`) e il suo test (`test_verifica_avvio.py`); stesso schema per `common/` (`modello.py` + `test_modello.py`). Nomi dei file unici in tutto il progetto e **legati al compito** (`classifica_ticket.py`, `verifica_avvio.py`), mai generici (`app.py`, `main.py`, `utils.py`).
- DO: nella docstring del sorgente: obiettivo, **pattern agentico**, **fase del loop** (osserva→pianifica→agisci→verifica), variabili d'ambiente, comando di avvio.
- DO: un solo `pyproject.toml` alla radice (ruff + `pytest` con `pythonpath = ["common", "01-startup", ...]`); dipendenze dalla radice (LC-VER-01); gli import sono `from modello import crea_modello`.
- DO: codice condiviso solo in `common/` (lettura `.env`, `crea_modello()`).
- DO NOT: `README.md`, `src/`, `tests/`, `__init__.py`, `__main__.py`, `pyproject.toml`, fixture o altri file nelle cartelle; import tra esempi diversi; logica di un esempio dentro `common/`.
- Perché: massima semplicità per il lab; deroga a PY-VER-02/03 (struttura `src/`+`tests/`), a PY-TST-01 (config per cartella) e al README di LC-VER-04; vince questo file.
- Verifica: `find . -path ./.venv -prune -o -type f -path './*/*' -print | grep -v -E '/(test_)?[a-z_]+\.py$'` non stampa nulla (a parte `guidelines/` e `spec/`); `pytest -q` dalla radice passa.

### LC-VER-04 [CONSIGLIATA] `create_agent` solo dove l'esempio è l'agente
- DO: `create_agent(model=crea_modello(), tools=[...], system_prompt=...)`; limite di passi con `agente.invoke(..., config={"recursion_limit": MAX_PASSI})`; tool con le stesse regole di LC-OPS-01 e LC-SEC-01.
- DO NOT: `create_agent` dove basta una catena LCEL o un loop `bind_tools`; middleware, checkpointer o store (oltre le basi).
- Perché: l'agente nasconde il loop osserva→agisci; si usa solo quando lo scopo è mostrare la differenza con il loop scritto in chiaro (LC-PAT-04).
- Verifica: manuale in review (la docstring dell'esempio dice perché serve l'agente).

### LC-VER-05 [CONSIGLIATA] Piano breve e rivedibile, prima del codice
- DO: salvare il piano in `spec/NN-nome/plan.md`, derivato dalla spec; massimo ~60 righe, italiano semplice, frasi corte. Sezioni fisse: **Cosa si fa** (2-3 righe), **File** (albero con una riga per file), **Passi** (elenco numerato, un passo = un risultato verificabile), **Test** (elenco di casi, una riga ciascuno), **Da decidere** (solo i dubbi veri, con la scelta proposta).
- DO NOT: codice completo nel piano; ripetere la spec; spiegazioni lunghe, tabelle o gergo; passi vaghi ("sistemare", "gestire").
- Perché: chi rivede (non programmatore) deve leggerlo in due minuti e dire sì o no prima che si scriva codice.
- Verifica: manuale in review (`wc -l spec/NN-nome/plan.md` ≤ 60).

## 2. Ambienti (`ENV`)

### LC-ENV-01 [BLOCCANTE] Endpoint e modello da variabili, in un solo punto
- DO: una funzione `crea_modello()` in `common/` che carica `.env` dalla radice con `python-dotenv` (`load_dotenv()`, l'ambiente già impostato vince) e legge `OPENAI_BASE_URL`, `OPENAI_API_KEY`, `LLM_MODEL` (default `localhost`, PY-ENV-01).
- DO NOT: `ChatOpenAI(...)` sparsi nel codice; URL o nomi di modello cloud come default.
- Perché: si cambia endpoint (mock, LAN, cloud) senza toccare il codice, e i test sostituiscono una sola funzione.
- Verifica: `grep -rn "ChatOpenAI(" --include=*.py common/ 0*/` trova una sola occorrenza.
Esempio:
```python
def crea_modello() -> ChatOpenAI:
    load_dotenv(RADICE / ".env")  # override=False: la shell vince
    return ChatOpenAI(
        base_url=os.environ.get("OPENAI_BASE_URL", "http://localhost:4000"),
        api_key=os.environ.get("OPENAI_API_KEY", "non-impostata"),
        model=os.environ.get("LLM_MODEL", "mock"),
        temperature=0, timeout=TIMEOUT_LLM_S, max_retries=2,
    )
```

## 3. Pattern e modularità (`PAT`)

### LC-PAT-01 [CONSIGLIATA] Catene LCEL piccole e con nome
- DO: `prompt | modello | parser` assegnato a una variabile parlante (`classifica_ticket`); una catena per passo del pattern (chaining, routing, parallelization…).
- DO NOT: catene lunghe una riga sola; logica di business dentro lambda anonime.
- Perché: chi rivede vede i passi del pattern agentico uno per uno.
Esempio: `riassumi = PROMPT_RIASSUNTO | crea_modello() | StrOutputParser()`

### LC-PAT-02 [CONSIGLIATA] Prompt come costanti, variabili esplicite
- DO: `ChatPromptTemplate.from_messages([("system", ...), ("human", "{testo}")])` in MAIUSCOLO in testa al modulo.
- DO NOT: prompt costruiti con f-string o `+`.
- Perché: il prompt si rivede come un file di config; le variabili mancanti fanno errore subito.

### LC-PAT-03 [CONSIGLIATA] Output strutturato con Pydantic quando serve un dato
- DO: `modello.with_structured_output(Classe)` con campi tipizzati e `Literal` per le categorie; testo libero solo se l'output va a una persona.
- DO NOT: parsare a mano il testo del modello con regex o `json.loads` su output libero.
- Perché: un dato fuori schema diventa un errore esplicito, non un valore sbagliato silenzioso.

### LC-PAT-04 [CONSIGLIATA] Loop dei tool scritto in chiaro e limitato
- DO: `bind_tools([...])`, ciclo `for` con `MAX_PASSI`, esecuzione dei soli tool registrati, `ToolMessage` con l'esito.
- DO NOT: `while True`; eseguire un nome di tool restituito dal modello senza cercarlo nella lista.
- Perché: il loop agentico è il contenuto didattico e non deve girare all'infinito.

## 4. Gestione errori (`ERR`)

### LC-ERR-01 [BLOCCANTE] Timeout e retry sul modello
- DO: `timeout` e `max_retries` (≤ 3) su `ChatOpenAI` (vedi LC-ENV-01).
- DO NOT: valori di default impliciti; retry fatti a mano sopra quelli della libreria.
- Perché: un endpoint lento non deve bloccare lo script né moltiplicare le chiamate.
- Verifica: `grep -n "timeout=" common/modello.py` trova la riga di `crea_modello()`.

### LC-ERR-02 [CONSIGLIATA] Errori del modello = exit 2, mai valori inventati
- DO: intercettare `openai.APIError` e `pydantic.ValidationError` in `main()`, log azionabile, exit 2 (PY-ERR-01).
- DO NOT: restituire stringa vuota o una categoria di default quando il modello fallisce (PY-ERR-05).
- Perché: un risultato finto è peggio di un errore visibile.

## 5. Operatività (`OPS`)

### LC-OPS-01 [BLOCCANTE] Tool che modificano: anteprima e conferma umana
- DO: tool in sola lettura di default; un tool che modifica restituisce l'anteprima e agisce solo con `--apply` e conferma esplicita (PY-OPS-01).
- DO NOT: tool che eseguono comandi arbitrari (`run_shell(cmd)`); modifiche decise solo dal modello.
- Perché: il blast radius lo decide una persona, non il modello.
- Verifica: manuale in review (elenco dei tool nella docstring con "lettura"/"modifica").

## 6. Security (`SEC`)

### LC-SEC-01 [BLOCCANTE] Output e argomenti del modello sono input non fidato
- DO: validare gli argomenti dei tool (tipi nella firma, `Literal`, percorsi dentro una cartella ammessa); dati utente/log solo nel messaggio `human`.
- DO NOT: `eval`/`exec`/`shell=True` su testo del modello (PY-SEC-02, PY-SEC-04); log o ticket dentro il system prompt.
- Perché: un log può contenere istruzioni (prompt injection) che il modello esegue.
- Verifica: `ruff check --select S` + manuale in review.

### LC-SEC-02 [CONSIGLIATA] Nessuna telemetria verso servizi esterni
- DO: lasciare spento il tracing (`LANGSMITH_TRACING` non impostata).
- DO NOT: abilitare LangSmith o callback che inviano prompt e dati fuori dal laptop.
- Perché: prompt e log possono contenere dati interni (PY-SEC-05).

## 7. Testing e qualità (`TST`)

### LC-TST-01 [BLOCCANTE] Test offline con modello finto
- DO: `monkeypatch` di `crea_modello()` con `GenericFakeChatModel` (`langchain_core.language_models.fake_chat_models`); i tool si testano da soli con `tool.invoke({...})`.
- DO NOT: chiamare l'endpoint vero nei test (PY-TST-04).
- Perché: i test passano offline, sempre uguali, in pochi secondi.
- Verifica: `unshare -rn pytest -q`.
Esempio:
```python
fake = GenericFakeChatModel(messages=iter([AIMessage("RETE")]))
monkeypatch.setattr(app, "crea_modello", lambda: fake)
assert app.main(["fixtures/ticket.txt"]) == 0
```

## 8. Errori tipici dell'AI e Definition of done
**Errori tipici** (indice):
- `requirements.txt` per esempio, versioni non pinnate o diverse → LC-VER-01
- `LLMChain`, `.run()`, `initialize_agent`, `AgentExecutor` → LC-VER-02
- `create_agent` usato dove bastava una catena, senza `recursion_limit` → LC-VER-04
- `ChatOpenAI(model="gpt-…")` scritto in più punti → LC-ENV-01
- regex o `json.loads` sull'output libero → LC-PAT-03
- `while True` sul tool calling → LC-PAT-04
- nessun `timeout` sul modello → LC-ERR-01
- categoria di default se il modello fallisce → LC-ERR-02
- tool `esegui_comando(cmd)` → LC-OPS-01, LC-SEC-01
- test che chiamano il modello vero → LC-TST-01

**Definition of done**: quella di [python/08-dod.md](python/08-dod.md), più:
- [ ] docstring dell'esempio con pattern agentico, fase del loop, variabili, comando
- [ ] `grep` di LC-VER-02 vuoto
- [ ] esecuzione reale contro l'endpoint del corso provata almeno una volta
