# Formato standard delle linee guida (guardrail per l'AI)

Per ogni strumento (ansible, terraform, python, bash): un file indice
`guidelines/<strumento>.md` + una cartella `guidelines/<strumento>/` con un file
per area. Stessa struttura per tutti, così l'AI sa dove trovare ogni regola.

```
guidelines/
  ansible.md            # indice: sezione 0 + tabella area → file (sempre in contesto)
  ansible/
    ver.md str.md env.md pat.md err.md ops.md sec.md tst.md debt.md   # sezioni 1-9
    ai-errors.md        # sezione 10 (indice, rimanda agli ID)
    dod.md              # sezione 11 (Definition of done)
```

## Principi

- **Progressive disclosure a più file**: l'indice `<strumento>.md` (sezione 0 +
  tabella area → file) è l'unico sempre in contesto (o in `AGENTS.md`); i file di
  area si leggono **solo quando il task tocca quell'area** (es. si scrive un
  `terraform apply` → si apre `ops.md`). Il `dod.md` si legge sempre a fine task.
- **Il file indice**: sezione 0 completa, poi una riga per file di area:
  `| OPS | ops.md | anteprima, idempotenza, rollback, approvazione | quando il task modifica sistemi |`
  (area, file, contenuto in una riga, quando aprirlo). Nessuna regola nell'indice
  oltre la sezione 0.
- **Riferimenti tra file**: sempre via ID (`ANS-OPS-01`), mai copiando il testo;
  un ID vive in un solo file.
- **Ogni regola ha: ID, severità, titolo e almeno uno tra DO / DO NOT.** Perché,
  Verifica ed Esempio sono facoltativi; la Verifica è obbligatoria per le
  BLOCCANTE (senza, la regola non può bloccare). Se manca: "manuale in review".
- **Esempi: soprattutto positivi (corretti)**, brevi (5-10 righe). Un controesempio
  ("Evitare:") si aggiunge solo quando l'errore è subdolo o tipico dell'AI.
- **Sezione non applicabile**: si scrive `N/A — perché`, non si omette.
- Lunghezza obiettivo: indice ≤ 40 righe, ogni file di area ≤ 60 righe.

## Formato di una regola

```
### <TOOL>-<AREA>-<NN> [BLOCCANTE|IMPORTANTE|CONSIGLIATA] Titolo breve
- DO: cosa fare
- DO NOT: cosa evitare
- Perché: la motivazione (una riga, se applicabile)
- Verifica: comando, tool o hook che la fa rispettare (obbligatoria se BLOCCANTE)
Esempio: (codice corretto)
```

Severità: **BLOCCANTE** = la modifica non passa; **IMPORTANTE** = serve
giustificazione scritta (commento `# deroga: <ID> — motivo` accanto al codice,
vedi sezione 9); **CONSIGLIATA** = warning.
Prefissi: `ANS`, `TF`, `PY`, `SH`. Aree: `VER`, `STR`, `ENV`, `PAT`, `ERR`,
`OPS`, `SEC`, `TST`, `DEBT`.

## Struttura dei file

Le sezioni 1-9 vanno ciascuna nel proprio file di area (nome in minuscolo del
prefisso, es. `ops.md`); 10 e 11 in `ai-errors.md` e `dod.md`. Ogni file di area
inizia con `# <TOOL> — <Area>` e contiene solo le regole di quell'area.

### 0. Regole non negoziabili
Max 7, una riga ciascuna, con ID. Sta nell'indice `<strumento>.md`, l'unica parte sempre caricata.

### 1. Versioni e convenzioni (`VER`)
Versione del linguaggio/tool e dei provider/collection (pinnate, mai `latest`),
naming, stile, formato dei file.

### 2. Struttura del progetto (`STR`)
Layout delle cartelle, dove va cosa, file obbligatori.

### 3. Ambienti dev / qa / prod (`ENV`)
Come si separano (inventory, workspace, variabili), cosa cambia tra ambienti,
cosa non deve mai essere condiviso. Per Bash/Python: configurazione via
variabili d'ambiente.

### 4. Pattern e modularità (`PAT`)
Idiomi del linguaggio da usare, quando estrarre un modulo/ruolo/funzione,
interfacce (input/output) esplicite, riuso.

### 5. Gestione errori (`ERR`)
Fallire presto e in modo leggibile, exit code, nessun errore ignorato in silenzio,
messaggi azionabili.

### 6. Operatività sicura (`OPS`)
Anteprima prima dell'azione (`--check --diff`, `plan`), idempotenza,
blast radius, rollback verificabile, approvazione umana.

### 7. Security (`SEC`)
Segreti, privilegi minimi, input non fidato, dipendenze, log senza dati sensibili.

### 8. Testing (`TST`)
- **Verifica statica**: format, lint, analisi statica (con i comandi esatti).
- **Verifica dinamica**: unit test, integration test, test di idempotenza.

### 9. Guardrail debito tecnico (`DEBT`)
Soglie misurabili (lunghezza funzione, complessità, duplicazione), policy su
`TODO`/`FIXME` (con riferimento a un ticket), regole sulle deroghe: formato
`# deroga: <ID> — motivo`, ammesse solo per regole IMPORTANTE/CONSIGLIATA.

### 10. Errori tipici dell'AI
Indice, non nuove regole: ogni difetto ricorrente rimanda all'ID che lo copre.
Esempio: `ignore_errors: true` per far passare un test → `ANS-ERR-02`.
Casi tipici: moduli/flag inventati, versioni `latest`, permessi `777`, segreti
in chiaro, test modificati per farli passare.

### 11. Definition of done
Checklist che l'AI esegue prima di dichiarare finito il task. Ogni file la
compila con i comandi esatti del proprio strumento; voce non pertinente → `N/A`.
- [ ] format + lint a zero errori
- [ ] test statici e dinamici passati
- [ ] anteprima rivista (Ansible `--check --diff`, Terraform `plan`;
      script: `--dry-run` se previsto)
- [ ] idempotenza verificata (Ansible: seconda run `changed: 0`; Terraform:
      `plan` dopo `apply` = "No changes"; script: seconda esecuzione senza
      modifiche allo stato)
- [ ] nessun segreto nel diff
- [ ] rollback descritto (se la modifica tocca sistemi vivi)

## Esempio compilato (una regola)

```
### ANS-SEC-01 [BLOCCANTE] Segreti solo da Ansible Vault o variabili d'ambiente
- DO: riferire i segreti con variabili (`vault_*`) cifrate con Ansible Vault o da ambiente.
- DO NOT: scrivere password/token letterali in playbook, inventory, log.
- Perché: finirebbero nel repo e nei log.
- Verifica: `ansible-lint` + hook `secret-guard`.
Esempio: password: "{{ vault_db_password }}"
```
