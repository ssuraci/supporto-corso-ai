# Python — 4. Gestione errori (`ERR`)

### PY-ERR-01 [BLOCCANTE] Exit code significativi
- DO: `0` ok, `1` problema rilevato (soglia superata, anomalie trovate), `2` errore d'uso o run che non può proseguire (se solo alcuni elementi falliscono, vedi PY-ERR-05: `1`); `main()` restituisce l'exit code; `130` su Ctrl-C.
- DO NOT: terminare con 0 dopo un errore; stampare "ERRORE" e proseguire; `sys.exit()` sparsi nelle funzioni interne.
- Perché: cron, CI e monitoring leggono solo l'exit code.
- Verifica: test dei tre casi in PY-TST-02 (`assert main([...]) == 1`).
Esempio:
```python
if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        raise SystemExit(130)
```

### PY-ERR-02 [BLOCCANTE] Nessun errore ignorato
- DO: catturare eccezioni specifiche (`FileNotFoundError`, `json.JSONDecodeError`, `subprocess.TimeoutExpired`) con un messaggio azionabile su stderr; un solo `except Exception` ammesso, in `main()`, con `log.exception(...)` e `return 2`.
- DO NOT: `except:` / `except Exception: pass`; rimuovere un controllo o allargare un `except` per far passare un test.
- Perché: un errore silenzioso diventa un falso "tutto ok" in produzione.
- Verifica: `ruff check --select E722,BLE,S110,S112`.
Esempio: `except FileNotFoundError: log.error("manca %s: controlla il percorso o --log", path); return 2`

### PY-ERR-03 [CONSIGLIATA] Timeout su tutto ciò che è esterno
- DO: `timeout=` su `subprocess.run`, `urllib.request.urlopen`, `socket.create_connection`; valore in una costante (PY-VER-04).
- DO NOT: chiamate che possono bloccarsi per sempre.
- Perché: uno script appeso in cron si accumula fino a saturare l'host.
- Verifica: `grep -nE "subprocess\.run|urlopen|create_connection" *.py | grep -v timeout` non stampa nulla.

### PY-ERR-04 [CONSIGLIATA] Righe malformate contate, non nascoste
- DO: una riga che non si analizza viene saltata, contata (`righe_scartate`) e, con `-v`, loggata col numero di riga; il conteggio finisce nell'output.
- DO NOT: fermare tutto per una riga sporca; scartarla senza traccia.
- Perché: i log reali hanno righe troncate e caratteri strani; il conteggio dice se il parser sta perdendo dati.
- Verifica: test con una fixture che contiene una riga rotta (PY-TST-03).

### PY-ERR-05 [CONSIGLIATA] Un errore esterno è un dato, non un valore inventato
- DO: se un comando, un endpoint o un modello fallisce o va in timeout, registrare `null` nel campo e il motivo in `errore`; proseguire con gli altri elementi; exit 1 se qualcosa è fallito.
- DO NOT: sostituire con `0`, `""`, una stima o un valore di default; inventare token, tempi o punteggi.
- Perché: uno zero inventato è indistinguibile da uno zero vero e falsa medie e confronti.
- Verifica: test con dipendenza finta che fallisce e che va in timeout (PY-TST-04).
Esempio: `{"risposta": null, "errore": "timeout dopo 300 s", "tempo_s": 300.0}`

### PY-ERR-06 [CONSIGLIATA] Retry limitati e solo su errori transitori
- DO: al massimo 1-3 tentativi con pausa crescente (`time.sleep(2 ** tentativo)`), solo su timeout, errori di rete, HTTP 429/5xx o risposta non parsabile.
- DO NOT: `while True` di retry; ritentare su 400/401/403/404 (non cambierà nulla).
- Perché: un retry infinito trasforma un endpoint lento in un endpoint giù, e nasconde il guasto.
- Verifica: manuale in review + test con dipendenza finta che fallisce sempre (numero di chiamate atteso).

### PY-ERR-07 [CONSIGLIATA] Esito dei comandi esterni sempre controllato
- DO: `check=True` oppure controllo esplicito di `returncode`; in caso di errore includere comando e stderr (troncato) nel messaggio.
- DO NOT: lanciare un comando e usare `stdout` senza guardare l'esito.
- Perché: un comando fallito restituisce stdout vuoto, che sembra "nessun problema".
- Verifica: `grep -n "subprocess.run" *.py` e controllare `check=` o `returncode`.
Esempio: `if r.returncode != 0: log.error("%s fallito: %s", cmd[0], r.stderr[-500:]); return 2`
