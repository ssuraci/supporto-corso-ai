# Python — 2. Ambienti dev / qa / prod (`ENV`) — via variabili d'ambiente

Script piccoli: niente file di config per ambiente. Lo script è identico ovunque;
cambiano solo argomenti e variabili d'ambiente.

### PY-ENV-01 [CONSIGLIATA] Valori d'ambiente da variabili, con override da CLI
- DO: endpoint, modello, cartelle e host letti da variabili d'ambiente come default di `argparse`; l'argomento esplicito vince.
- DO NOT: URL, IP, hostname o percorsi di un ambiente scritti nel codice; default che puntano a produzione (ammesso solo `localhost`).
- Perché: lo stesso script passa da laptop a endpoint LAN a cloud senza modifiche, e un errore di default non tocca la produzione.
- Verifica: `grep -nE "https?://|[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+" *.py` mostra solo `localhost`/`127.0.0.1`.
Esempio:
```python
p.add_argument(
    "--endpoint",
    default=os.environ.get("LLM_BASE_URL", "http://localhost:4000"),
    help="URL OpenAI-compatibile (env LLM_BASE_URL)",
)
```

### PY-ENV-02 [CONSIGLIATA] Variabili documentate, `.env` mai versionato
- DO: elencare le variabili usate in `--help` e in `.env.example` (valori finti); `.env` in `.gitignore`; caricarlo con `python-dotenv` (`load_dotenv()`, senza `override`: le variabili già nell'ambiente vincono) o, negli script senza dipendenze, dalla shell (`set -a; . ./.env; set +a`).
- DO NOT: committare `.env`; scrivere un parser `.env` fatto in casa; `load_dotenv(override=True)`. `python-dotenv` solo dove LC-VER-01 lo pinna.
- Perché: chi esegue sa cosa impostare; i valori reali restano fuori dal repo.
- Verifica: `.env` compare in `.gitignore` (`git check-ignore .env` lo stampa).
