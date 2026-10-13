"""Smoke test dell'accesso ai modelli LLM con LangChain (modello base e evoluto).

Uso (dalla radice del progetto):  python llm_test/smoke_test.py
Per ogni livello controlla due cose, quelle su cui si appoggia il workflow:
una chiamata semplice e un output strutturato (with_structured_output).
Exit code: 0 tutto ok, 1 un controllo è fallito.
"""

import sys
import time
from pathlib import Path

from pydantic import BaseModel

# Lanciato come script, Python mette in path llm_test/ e non la radice.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common.llm import get_llm  # noqa: E402


class Esito(BaseModel):
    ok: bool


errori = 0


def check(ok: bool, msg: str) -> None:
    global errori
    print(("OK      " if ok else "FALLITO ") + msg)
    errori += not ok


for livello in ("base", "advanced"):
    llm = get_llm(livello)
    print(f"[{livello}] modello={llm.model_name} endpoint={llm.openai_api_base}")
    try:
        t = time.time()
        r = llm.invoke("Rispondi solo con la parola: pong")
        check(bool(r.content.strip()), f"{livello}: invoke -> {r.content.strip()[:40]!r} ({time.time() - t:.1f}s)")
    except Exception as e:
        check(False, f"{livello}: invoke fallito ({type(e).__name__}: {e})")
    try:
        e = llm.with_structured_output(Esito).invoke("Rispondi con ok=true.")
        check(isinstance(e, Esito) and e.ok, f"{livello}: output strutturato -> {e}")
    except Exception as ex:
        check(False, f"{livello}: output strutturato fallito ({type(ex).__name__}: {ex})")

sys.exit(1 if errori else 0)
