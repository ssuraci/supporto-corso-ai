# ANS — Definition of done

Prima di dichiarare finito:
- [ ] `ansible-playbook <pb> --syntax-check` e `ansible-lint <pb>` a zero errori
- [ ] verifica dinamica passata (check/health reale)
- [ ] `--check --diff` mostrato e approvato dall'umano
- [ ] seconda run: `changed=0`
- [ ] nessun segreto reale nel diff (password del lab ammesse, `no_log` sui task che le usano)
- [ ] rollback descritto in una riga (se la modifica tocca host vivi)
