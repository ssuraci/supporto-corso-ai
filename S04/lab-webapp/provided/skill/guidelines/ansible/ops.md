# ANS — Operatività sicura

### ANS-OPS-01 [BLOCCANTE] Anteprima + approvazione umana
- DO: lanciare `ansible-playbook … --check --diff`, mostrare l'esito, **attendere il via dell'umano**, poi applicare.
- DO NOT: applicare direttamente su host vivi; auto-approvarsi.
- Perché: S04 è Run, blast radius immediato.
- Verifica: manuale in review (l'umano scrive "ok" prima dell'apply).

### ANS-OPS-02 [BLOCCANTE] Idempotenza
- DO: eseguire il playbook due volte; la seconda deve dare `changed=0`.
- DO NOT: task che cambiano sempre (`command` senza `changed_when`, timestamp nei file).
- Verifica: `ansible-playbook … | grep -E "changed=0"` alla seconda run.

### ANS-OPS-03 [IMPORTANTE] Backup prima di toccare una config
- DO: `backup: true` su `template`/`copy`/`lineinfile` per file di config esistenti.
- DO NOT: sovrascrivere senza copia.

### ANS-OPS-04 [CONSIGLIATA] Rollback in una riga
- DO: dire nel messaggio finale come tornare indietro (es. ripristino del `.bak`, `state: absent`).
