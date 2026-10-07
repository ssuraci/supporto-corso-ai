# ANS — Testing

### ANS-TST-01 [BLOCCANTE] Verifica statica
- DO: `ansible-playbook <pb>.yml --syntax-check` e `ansible-lint <pb>.yml` a zero errori.
- Verifica: i due comandi, exit code 0.

### ANS-TST-02 [BLOCCANTE] Verifica dinamica
- DO: dopo l'apply, un task di verifica reale (porta in ascolto, `uri` 200, query riuscita) e seconda run con `changed=0` (`ANS-OPS-02`).
- DO NOT: modificare il test o il check per farlo passare (`ANS-ERR-01`).
- Verifica: output del playbook di test/health del lab.
Esempio:
```yaml
- ansible.builtin.uri: { url: "http://localhost/", status_code: 200 }
```
