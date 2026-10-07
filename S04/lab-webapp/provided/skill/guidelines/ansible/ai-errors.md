# ANS — Errori tipici dell'AI (indice)

| Difetto ricorrente | Regola |
|---|---|
| Applica senza `--check --diff` né approvazione | ANS-OPS-01 |
| Seconda run con `changed` > 0 (`command` nudo, restart fisso) | ANS-OPS-02, ANS-PAT-02 |
| `shell: apt/systemctl/sed` invece del modulo | ANS-PAT-01 |
| Modulo o parametro inventato | ANS-PAT-01, ANS-TST-01 |
| `ignore_errors: true` per far passare il test | ANS-ERR-01 |
| Modifica il test/check invece del playbook | ANS-TST-02 |
| `hosts: all` su playbook che scrive | ANS-STR-01 |
| `mode: "0777"` o bind `0.0.0.0` | ANS-SEC-03 |
| Password nei task / log senza `no_log` | ANS-SEC-01 |
| Segreto reale incollato | ANS-SEC-02 |
