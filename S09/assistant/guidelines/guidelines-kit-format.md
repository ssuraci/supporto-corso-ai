# Formato standard delle linee guida (guardrail per l'AI)

Un file per linguaggio o strumento: `guidelines/<strumento>.md` (es. ansible,
terraform, python, bash, javascript, go, sql). Stessa struttura per tutti, così
l'AI sa dove trovare ogni regola.

## Principi

- **Progressive disclosure**: la sezione 0 è sempre in contesto (o in `AGENTS.md`);
  il resto si carica a richiesta.
- **Ogni regola ha: ID, severità, titolo, Perché e almeno uno tra DO / DO NOT.**
  Il Perché serve a chi rivede (sistemisti, non programmatori). Verifica ed
  Esempio sono facoltativi; la Verifica è obbligatoria per le BLOCCANTE (senza,
  la regola non può bloccare). Se manca: "manuale in review".
- **Esempi**: soprattutto corretti, brevi (5-10 righe). Un controesempio
  ("Evitare:") solo se l'errore è subdolo o tipico dell'AI.
- **Sezione non applicabile**: `N/A — perché`, non si omette.
- Lunghezza obiettivo: ≤ 150 righe per file. Se si sfora, si tagliano prima
  gli Esempi, mai il Perché.

## Formato di una regola

```
### <TOOL>-<AREA>-<NN> [BLOCCANTE|CONSIGLIATA] Titolo breve
- DO: cosa fare
- DO NOT: cosa evitare
- Perché: motivazione (una riga)
- Verifica: comando, tool o hook che la fa rispettare (obbligatoria se BLOCCANTE)
Esempio: (codice corretto)
```

- **Severità**: BLOCCANTE = la modifica non passa; CONSIGLIATA = warning, si
  può derogare.
- **Deroga** (solo CONSIGLIATA): commento `deroga: <ID> — motivo` accanto al
  codice (sintassi di commento del linguaggio).
- **Prefisso `<TOOL>`**: 2-3 lettere maiuscole, unico nel progetto
  (es. `ANS`, `TF`, `PY`, `SH`, `JS`, `GO`).
- **Aree**: `VER`, `ENV`, `PAT`, `ERR`, `OPS`, `SEC`, `TST`.

## Struttura del file

### 0. Regole non negoziabili
Max 7, una riga ciascuna (solo ID e titolo). È l'unica sezione sempre caricata.

### 1. Versioni, stile e struttura (`VER`)
Versione di linguaggio/tool e dipendenze (pinnate, mai `latest`; per script
operativi: solo libreria standard se possibile), naming, stile, file obbligatori.

### 2. Ambienti dev / qa / prod (`ENV`)
Come si separano (config, variabili d'ambiente); il codice non contiene valori
di un ambiente. Per script piccoli spesso `N/A — perché`.

### 3. Pattern e modularità (`PAT`)
Idiomi del linguaggio da usare, input/output espliciti. Per script piccoli
spesso `N/A — perché`.

### 4. Gestione errori (`ERR`)
Fallire presto e in modo leggibile, exit code, nessun errore ignorato in
silenzio, messaggi azionabili.

### 5. Operatività (`OPS`)
Anteprima prima dell'azione (dry-run, diff, plan), idempotenza, blast radius,
rollback verificabile, approvazione umana. Senza effetti su sistemi vivi:
`N/A — perché`.

### 6. Security (`SEC`)
Segreti, privilegi minimi, input non fidato, dipendenze, log senza dati sensibili.

### 7. Testing e qualità (`TST`)
- **Statica**: format, lint, analisi statica (comandi esatti).
- **Dinamica**: test, test di idempotenza.

### 8. Errori tipici dell'AI e Definition of done
**Errori tipici**: indice, non nuove regole; ogni difetto rimanda all'ID che lo
copre. Es.: errore ignorato per far passare un test → `<TOOL>-ERR-02`.
Casi tipici: API/flag inventati, versioni `latest`, permessi `777`, segreti in
chiaro, comandi shell costruiti con stringhe, test modificati per farli passare.

**Definition of done** (l'AI la esegue prima di dichiarare finito; comandi
esatti dello strumento; voce non pertinente → `N/A`):
- [ ] format + lint a zero errori (es. Python: `ruff format --check . && ruff check .`)
- [ ] test passati (es. Python: `pytest -q`)
- [ ] nessun segreto nel diff

## Esempio compilato

```
### PY-SEC-01 [BLOCCANTE] Segreti solo da variabili d'ambiente o secret store
- DO: leggere i segreti dall'ambiente o da un secret store.
- DO NOT: scrivere password/token letterali in codice, config, log.
- Perché: finirebbero nel repo e nei log.
- Verifica: `ruff check --select S` + hook `secret-guard`.
Esempio: password = os.environ["DB_PASSWORD"]
```
