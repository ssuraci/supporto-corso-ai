-- seed.sql — dati di test di appdb (estratti da install-db.yml); idempotente

INSERT IGNORE INTO clienti (id, nome, email, citta) VALUES
  (1, 'Alice Bianchi',  'alice@example.com',  'Milano'),
  (2, 'Bruno Verdi',    'bruno@example.com',  'Roma'),
  (3, 'Carla Neri',     'carla@example.com',  'Torino'),
  (4, 'Davide Rossi',   'davide@example.com', 'Napoli'),
  (5, 'Elena Gialli',   'elena@example.com',  'Bologna');

INSERT IGNORE INTO prodotti (id, nome, prezzo, categoria) VALUES
  (1, 'Notebook 14"',    799.00, 'Informatica'),
  (2, 'Mouse wireless',   19.90, 'Informatica'),
  (3, 'Sedia ufficio',   149.00, 'Arredo'),
  (4, 'Monitor 27"',     249.00, 'Informatica'),
  (5, 'Lampada LED',      34.50, 'Arredo');

INSERT IGNORE INTO ordini (id, cliente_id, prodotto_id, quantita, data_ordine) VALUES
  (1, 1, 1, 1, '2025-01-10'),
  (2, 1, 2, 2, '2025-01-10'),
  (3, 2, 3, 1, '2025-01-12'),
  (4, 3, 4, 1, '2025-02-03'),
  (5, 4, 5, 3, '2025-02-15'),
  (6, 5, 1, 1, '2025-03-01'),
  (7, 2, 4, 2, '2025-03-05');
