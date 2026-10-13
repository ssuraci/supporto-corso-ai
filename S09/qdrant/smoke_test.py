"""Smoke test di Qdrant: raggiungibilità, collection popolate, ricerca che torna risultati.

Uso (dalla radice del progetto):  python qdrant/smoke_test.py
Usa la chiave in sola lettura: QDRANT_ENDPOINT e QDRANT_API_KEY_RO nel .env.
Exit code: 0 tutto ok, 1 un controllo è fallito, 2 configurazione mancante.
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Document

RADICE = Path(__file__).resolve().parent.parent
# Lo stesso modello usato dagli script popola_*.py: query e documenti devono combaciare.
MODELLO = "sentence-transformers/all-minilm-l6-v2"
# collection -> domanda di prova
PROVE = {
    "aruba-kb": "come si configura una casella di posta?",
    "aruba-past-incidents": "VM irraggiungibile via SSH per disco pieno",
}

load_dotenv(RADICE / ".env")
for v in ("QDRANT_ENDPOINT", "QDRANT_API_KEY_RO"):
    if not os.environ.get(v):
        sys.exit(f"variabile mancante nel .env: {v}")

qdrant = QdrantClient(
    url=os.environ["QDRANT_ENDPOINT"],
    api_key=os.environ["QDRANT_API_KEY_RO"],
    cloud_inference=True,
)

errori = 0


def check(ok: bool, msg: str) -> bool:
    global errori
    print(("OK    " if ok else "FALLITO ") + msg)
    errori += not ok
    return ok


try:
    esistenti = {c.name for c in qdrant.get_collections().collections}
    check(True, "connessione a Qdrant")
except Exception as e:
    sys.exit(f"FALLITO connessione a Qdrant: {e}")

for nome, domanda in PROVE.items():
    if not check(nome in esistenti, f"{nome}: collection presente"):
        continue
    n = qdrant.count(nome).count
    check(n > 0, f"{nome}: {n} punti")
    try:
        hit = qdrant.query_points(
            nome, query=Document(text=domanda, model=MODELLO), limit=3, with_payload=True
        ).points
        check(len(hit) > 0, f"{nome}: ricerca '{domanda}' -> {len(hit)} risultati")
        if hit:
            p = hit[0].payload or {}
            print(f"      primo: score={hit[0].score:.2f} fonte={p.get('fonte') or p.get('id', '?')}")
    except Exception as e:
        check(False, f"{nome}: ricerca fallita ({e})")

sys.exit(1 if errori else 0)
