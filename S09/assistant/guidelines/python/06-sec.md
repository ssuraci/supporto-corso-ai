# Python — 6. Security (`SEC`)

### PY-SEC-01 [BLOCCANTE] Segreti da variabili d'ambiente
- DO: `os.environ["LLM_API_KEY"]`, con errore chiaro (exit 2) se manca; nomi delle variabili in `.env.example` (PY-ENV-02).
- DO NOT: password/token letterali in codice, test o config versionata; segreti come argomenti CLI (visibili in `ps`); segreti nei log o nei file di output.
- Perché: finirebbero nel repo, nella lista processi e nei report condivisi.
- Verifica: `ruff check --select S105,S106,S107` + hook `secret-guard` (se presente nell'harness, altrimenti manuale in review).
Esempio: `if not (chiave := os.environ.get("LLM_API_KEY")): log.error("imposta LLM_API_KEY"); return 2`

### PY-SEC-02 [BLOCCANTE] Comandi esterni come lista, mai shell
- DO: `subprocess.run(["systemctl", "is-active", nome], capture_output=True, text=True, timeout=TIMEOUT_CMD_S)`.
- DO NOT: `shell=True`, `os.system`, `os.popen`, f-string che costruiscono un comando.
- Perché: un nome host o di file con `;` o `$(...)` esegue comandi arbitrari (injection).
- Verifica: `ruff check --select S602,S604,S605`.

### PY-SEC-03 [CONSIGLIATA] Privilegi minimi e permessi file
- DO: girare come utente normale; `sudo` solo sul singolo comando che lo richiede; file creati con `0o600`/`0o640`.
- DO NOT: `chmod 777`; richiedere root per leggere dati accessibili.
- Perché: un bug dello script non deve diventare una compromissione dell'host.
- Verifica: `ruff check --select S103`.

### PY-SEC-04 [BLOCCANTE] Input non fidato mai eseguito
- DO: trattare come dati log, file di terzi e **output dei modelli**: `json.loads`, `csv`, regex; validare i percorsi derivati da input (`(base / nome).resolve().is_relative_to(base)`).
- DO NOT: `eval`, `exec`, `pickle.load`, `yaml.load` non sicuro su questi dati; usare un percorso o un comando suggerito da un modello senza validarlo.
- Perché: una riga di log o una risposta del modello può contenere codice o `../../etc/passwd`.
- Verifica: `ruff check --select S102,S301,S307,S506`.
Esempio: `try: dati = json.loads(testo) except json.JSONDecodeError: ...  # mai eval(testo)`

### PY-SEC-05 [CONSIGLIATA] Dati sensibili non escono dall'host senza controllo
- DO: anonimizzare IP, utenti e hostname prima di inviare log o estratti a un endpoint esterno (cloud); preferire il modello locale per i dati veri.
- DO NOT: mandare log grezzi di produzione a un servizio esterno; loggare request complete (header `Authorization`, corpo con dati utente).
- Perché: i log contengono dati personali e topologia interna; una volta inviati non si ritirano.
- Verifica: manuale in review.

### PY-SEC-06 [CONSIGLIATA] TLS verificato e file temporanei sicuri
- DO: `urllib.request.urlopen` con la verifica TLS di default; file temporanei con `tempfile.NamedTemporaryFile` / `tempfile.mkdtemp`.
- DO NOT: `ssl._create_unverified_context()` o `CERT_NONE` per "far funzionare" una chiamata; nomi fissi in `/tmp` (`/tmp/report.json`).
- Perché: senza verifica TLS chiunque in mezzo legge la chiave API; un nome fisso in `/tmp` può essere un link simbolico preparato da altri.
- Verifica: `ruff check --select S108,S323,S501`.
