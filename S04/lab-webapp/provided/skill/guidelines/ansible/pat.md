# ANS — Pattern

### ANS-PAT-01 [IMPORTANTE] Modulo dedicato prima di shell/command
- DO: `apt`, `service`, `template`, `copy`, `lineinfile`, `mysql_user`… con nome completo (`ansible.builtin.*`).
- DO NOT: `shell: apt install …` o `shell: systemctl restart …`; non inventare moduli o parametri.
- Perché: i moduli sono idempotenti e supportano `--check`.
- Verifica: `ansible-lint` (regola `command-instead-of-module`).
- Se `shell`/`command` è inevitabile: `changed_when`/`creates` e commento `# deroga: ANS-PAT-01 — motivo`.

### ANS-PAT-02 [CONSIGLIATA] Handler per i riavvii
- DO: `notify` + `handlers` per riavviare un servizio dopo una modifica di config.
- DO NOT: `state: restarted` incondizionato (rompe l'idempotenza).
Esempio:
```yaml
- ansible.builtin.template: { src: nginx.conf.j2, dest: /etc/nginx/nginx.conf }
  notify: Riavvia nginx
```

### ANS-PAT-03 [CONSIGLIATA] Valori in variabili
- DO: porte, utenti, percorsi in `vars:` in testa al playbook.
- DO NOT: ripeterli come letterali nei task.
