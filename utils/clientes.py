
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
CLIENTES_DIR = ROOT / "data" / "clientes"

def listar_clientes():
    clientes = []
    for arq in sorted(CLIENTES_DIR.glob("*.json")):
        try:
            clientes.append(json.loads(arq.read_text(encoding="utf-8")))
        except Exception:
            pass
    return clientes

def carregar_cliente(cliente_id):
    arq = CLIENTES_DIR / f"{cliente_id}.json"
    return json.loads(arq.read_text(encoding="utf-8"))

def salvar_cliente(data):
    CLIENTES_DIR.mkdir(parents=True, exist_ok=True)
    arq = CLIENTES_DIR / f"{data['id']}.json"
    arq.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return arq
