# Linee guida Ansible (versione corso)

Versione semplificata per il lab: poche regole, quelle che servono a non rompere
il sistema. Formato: `guidelines-kit.format.md`. Le password del lab sono finte:
qui **non si richiede Ansible Vault** (vedi `ANS-SEC-01`).

## 0. Regole non negoziabili

1. `ANS-OPS-01` — prima di ogni modifica: `--check --diff`, poi approvazione umana.
2. `ANS-OPS-02` — il playbook è idempotente: alla seconda run `changed: 0`.
3. `ANS-PAT-01` — moduli Ansible, non `shell`/`command` se esiste il modulo.
4. `ANS-ERR-01` — mai `ignore_errors: true` per far passare un test.
5. `ANS-STR-01` — ogni playbook ha nome, `become` esplicito e `hosts` mirati (mai `all` in scrittura).
6. `ANS-TST-01` — `ansible-lint` e `--syntax-check` a zero errori.
7. `ANS-SEC-02` — nessun segreto *reale* nel repo (quelli del lab sono finti).

## Indice delle aree (apri il file solo se il task tocca l'area)

| Area | File | Contenuto | Quando aprirlo |
|---|---|---|---|
| STR | ansible/str.md | layout cartelle, nomi, hosts | si crea/sposta un playbook |
| PAT | ansible/pat.md | moduli, handler, variabili | si scrive un task |
| ERR | ansible/err.md | fallire presto, no errori ignorati | si gestiscono errori/`failed_when` |
| OPS | ansible/ops.md | check/diff, idempotenza, rollback | il task modifica sistemi |
| SEC | ansible/sec.md | segreti e permessi (rilassato) | password, utenti, file sensibili |
| TST | ansible/tst.md | lint, syntax, idempotenza | prima di dichiarare finito |
| AI | ansible/ai-errors.md | errori tipici dell'AI → ID | in revisione del proprio output |
| DoD | ansible/dod.md | checklist di fine task | **sempre** a fine task |

Non coperte nella versione corso: `VER`, `ENV`, `DEBT` (N/A — un solo ambiente di lab, nessun debito da gestire).
