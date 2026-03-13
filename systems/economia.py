import json
import os
from systems.itens import slots_equipamento

ARQUIVO_ECONOMIA = "economia.json"

def carregar_dados():
    if not os.path.exists(ARQUIVO_ECONOMIA):
        with open(ARQUIVO_ECONOMIA, "w") as f:
            json.dump({}, f)

    with open(ARQUIVO_ECONOMIA, "r") as f:
        return json.load(f)

def salvar_dados(dados):
    with open(ARQUIVO_ECONOMIA, "w") as f:
        json.dump(dados, f, indent=4)

def garantir_jogador(dados, user_id):

    if user_id not in dados:
        dados[user_id] = {}

    jogador = dados[user_id]

    defaults = {
        "saldo": 0,
        "xp": 0,
        "nivel": 1,
        "rank": "E",
        "hp": 100,
        "ataque": 15,
        "defesa": 6,
        "inventario": [],
        "equipado": {
            "arma": None,
            "armadura": None,
            "acessorio": None
        },
        "drops_unicos": []
    }

    if "inventario" not in jogador:
        jogador["inventario"] = []

    for item in jogador["inventario"]:
        if "tipo" not in item:
            item["tipo"] = "arma"
        if "defesa" not in item:
            item["defesa"] = 0
        if "ataque" not in item:
            item["ataque"] = 0

    jogador = dados[user_id]
    jogador.setdefault("drops_unicos", [])
    jogador.setdefault("inventario", [])
    jogador.setdefault("equipado", {})

    for slot in slots_equipamento:
        jogador["equipado"].setdefault(slot, None)

    salvar_dados(dados)

    for chave, valor in defaults.items():
        if chave not in jogador:
            jogador[chave] = valor

    return jogador

