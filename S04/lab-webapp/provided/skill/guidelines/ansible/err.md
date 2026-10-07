# ANS — Gestione errori

### ANS-ERR-01 [BLOCCANTE] Nessun errore ignorato per far passare il test
- DO: lasciare fallire il task; correggere la causa.
- DO NOT: `ignore_errors: true`, `failed_when: false` per "sistemare" un rosso.
- Perché: nasconde il problema e il report diventa falso.
- Verifica: `grep -rn "ignore_errors\|failed_when: false" .` deve essere vuoto (o con `# deroga`, solo nei check di osservabilità).

### ANS-ERR-02 [IMPORTANTE] Errore leggibile
- DO: `ansible.builtin.assert` / `fail` con `msg:` che dice cosa è sbagliato e cosa fare.
Esempio:
```yaml
- ansible.builtin.assert:
    that: ansible_distribution == "Ubuntu"
    fail_msg: "Playbook testato solo su Ubuntu: host {{ inventory_hostname }} non supportato"
```
