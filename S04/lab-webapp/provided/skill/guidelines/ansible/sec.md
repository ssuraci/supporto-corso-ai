# ANS — Security (rilassata per il corso)

### ANS-SEC-01 [CONSIGLIATA] Password del lab: ammesse in chiaro, ma in variabile
- DO: tenere le password finte del lab in `vars:` o `group_vars/` (es. `db_password`), mai sparse nei task; aggiungere `no_log: true` sui task che le usano.
- DO NOT: richiedere/introdurre Ansible Vault, né valutare la robustezza delle password del lab.
- Perché: i segreti sono finti; Vault è fuori programma. In produzione si userebbe Vault (`vault_*`).
Esempio:
```yaml
vars: { db_password: "lab-password" }   # finta, solo lab
tasks:
  - community.mysql.mysql_user: { name: app, password: "{{ db_password }}", state: present }
    no_log: true
```

### ANS-SEC-02 [BLOCCANTE] Nessun segreto reale
- DO: usare solo credenziali del lab.
- DO NOT: incollare token, chiavi private o password di sistemi veri.
- Verifica: hook `secret-guard` (se presente) o revisione del diff.

### ANS-SEC-03 [IMPORTANTE] Permessi espliciti e minimi
- DO: `mode:` e `owner:` su file di config (`0644`; `0600` se contiene password).
- DO NOT: `mode: "0777"`; MariaDB/servizi in ascolto su `0.0.0.0` senza motivo.
