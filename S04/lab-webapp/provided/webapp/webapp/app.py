#!/usr/bin/env python3
"""Applicazione Python — API + UI del LAB S04 (Fase 2 · provisioning).

Endpoints:
  /health        — check di sopravvivenza: sempre 200 se il processo gira.
  /ready         — check della dipendenza da MariaDB: 200 solo se il DB
                   risponde a una lettura.
  /api/clienti   — elenco clienti (JSON).
  /api/prodotti  — elenco prodotti (JSON).
  /api/ordini    — elenco ordini con nome cliente/prodotto (JSON, JOIN).
  /              — pagina jQuery che naviga le tre tabelle via le API sopra.

La configurazione viene letta UNA volta all'avvio (come un servizio reale):
modificare config.json ha effetto solo dopo un restart del servizio webapp.
"""

import json
import os
from datetime import datetime
from decimal import Decimal

from flask import Flask, jsonify, render_template
import pymysql

app = Flask(__name__)

CONFIG_PATH = os.environ.get("APP_CONFIG", "/opt/webapp/config.json")


def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)


# Config letta una sola volta, all'avvio, non a ogni richiesta.
CONFIG = load_config()


def get_db_connection():
    cfg = CONFIG
    return pymysql.connect(
        host=cfg["db_host"],
        user=cfg["db_user"],
        password=cfg["db_password"],
        database=cfg["db_name"],
        port=cfg.get("db_port", 3306),
        connect_timeout=5,
        cursorclass=pymysql.cursors.DictCursor,
    )


def query(sql):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()
    finally:
        conn.close()
    # Decimal e date non sono serializzabili in JSON di default.
    for row in rows:
        for key, value in row.items():
            if isinstance(value, Decimal):
                row[key] = float(value)
            elif hasattr(value, "isoformat"):
                row[key] = value.isoformat()
    return rows


@app.route("/health")
def health():
    # Sempre 200 finche' il processo e' in esecuzione.
    return jsonify({"status": "healthy", "timestamp": datetime.utcnow().isoformat()})


@app.route("/ready")
def ready():
    # 200 solo se MariaDB raggiungibile (query su una tabella reale del DB).
    try:
        rows = query("SELECT 1 AS ok")
        if rows and rows[0]["ok"] == 1:
            return jsonify({"status": "ready", "db": "connected"})
        return jsonify({"status": "degraded", "db": "query failed"}), 503
    except Exception as e:
        return jsonify({"status": "unavailable", "db": repr(e)}), 503


@app.route("/api/clienti")
def api_clienti():
    return jsonify(query("SELECT id, nome, email, citta FROM clienti ORDER BY id"))


@app.route("/api/prodotti")
def api_prodotti():
    return jsonify(query("SELECT id, nome, prezzo, categoria FROM prodotti ORDER BY id"))


@app.route("/api/ordini")
def api_ordini():
    return jsonify(query("""
        SELECT o.id, c.nome AS cliente, p.nome AS prodotto,
               o.quantita, o.data_ordine, (p.prezzo * o.quantita) AS totale
        FROM ordini o
        JOIN clienti c ON c.id = o.cliente_id
        JOIN prodotti p ON p.id = o.prodotto_id
        ORDER BY o.id
    """))


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
