# ANS — Struttura

### ANS-STR-01 [IMPORTANTE] Playbook leggibile e mirato
- DO: dare un `name:` a play e task; `become: true` solo dove serve; `hosts:` sul gruppo giusto (`web`, `db`).
- DO NOT: `hosts: all` in playbook che modificano.
- Perché: blast radius chiaro e output leggibile.
- Verifica: `ansible-lint`.
Esempio:
```yaml
- name: Installa nginx sul web
  hosts: web
  become: true
  tasks:
    - name: Pacchetto nginx presente
      ansible.builtin.apt: { name: nginx, state: present }
```

### ANS-STR-02 [CONSIGLIATA] Un playbook = un obiettivo
- DO: un file per scopo (`install-nginx.yml`, `observe-db.yml`), nomi in `kebab-case`.
- DO NOT: un playbook unico che fa tutto.
