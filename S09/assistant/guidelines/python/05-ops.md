# Python — 5. Operatività (`OPS`)

Si applica a script che modificano file, servizi o utenti. Script di sola lettura
(controlli, report, parsing): OPS-01/02/05 `N/A — nessuna modifica`; OPS-03/04 valgono
comunque per i file di output.

### PY-OPS-01 [BLOCCANTE] Dry-run di default, azione solo con `--apply`
- DO: senza `--apply` stampare l'elenco dei target e cosa si farebbe, con il conteggio; con `--apply` eseguire.
- DO NOT: scrivere, cancellare o riavviare senza `--apply`; cancellare con glob non mostrati prima.
- Perché: blast radius: l'operatore deve vedere l'anteprima prima di toccare un sistema vivo.
- Verifica: test che esegue `main([...])` senza `--apply` su `tmp_path` e verifica che nulla sia cambiato (PY-TST-02).
Esempio: `if args.apply: path.unlink() else: print(f"[dry-run] rimuoverei {path}")`

### PY-OPS-02 [CONSIGLIATA] Idempotenza e backup
- DO: seconda esecuzione = nessuna modifica; controllare lo stato prima di agire; copia `.bak` prima di sovrascrivere un file di sistema.
- DO NOT: aggiungere righe a un file a ogni run (`open(..., "a")` senza controllo); riavviare un servizio se nulla è cambiato.
- Perché: gli script girano in cron e vengono rilanciati dopo un guasto.
- Verifica: eseguire due volte con `--apply`; la seconda deve riportare "0 modifiche".

### PY-OPS-03 [CONSIGLIATA] Scrittura atomica dei file di output
- DO: scrivere su un file temporaneo nella stessa cartella e poi `Path.replace()` sul nome finale.
- DO NOT: scrivere direttamente sul file finale.
- Perché: se lo script muore a metà, chi legge dopo (altro script, cron, modello) trova un JSON troncato.
- Verifica: manuale in review.
Esempio:
```python
tmp = out.with_suffix(out.suffix + ".tmp")
tmp.write_text(json.dumps(dati, ensure_ascii=False, indent=2), encoding="utf-8")
tmp.replace(out)
```

### PY-OPS-04 [CONSIGLIATA] Input in sola lettura, output in cartella dedicata
- DO: aprire gli input solo in lettura; scrivere nella cartella di `-o` (creata con `mkdir(parents=True, exist_ok=True)`); rifiutare (exit 2) se l'output coinciderebbe con un input.
- DO NOT: modificare o sovrascrivere i file di input; scrivere nella cartella corrente "per comodità".
- Perché: l'input originale è la prova: serve per rifare l'analisi e verificare le citazioni.
- Verifica: test che controlla l'hash del file di input prima e dopo l'esecuzione.

### PY-OPS-05 [CONSIGLIATA] Una sola istanza alla volta in cron
- DO: lock esclusivo non bloccante con `fcntl.flock` su un file in `/run/lock` o nella cartella di output; se è già preso, messaggio ed exit 2.
- DO NOT: lasciare che due run si sovrappongano sugli stessi file.
- Perché: un run lento più il successivo di cron = file scritti due volte o corrotti.
- Verifica: lanciare due istanze in parallelo; la seconda esce con 2.
Esempio: `fcntl.flock(lock_f, fcntl.LOCK_EX | fcntl.LOCK_NB)` (solleva `BlockingIOError` se occupato)
