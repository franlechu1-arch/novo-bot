import random

slots_equipamento = [
    "arma",
    "armadura",
    "acessorio"
]

ITENS = {
    "espada_enferrujada": {
        "nome": "Espada Enferrujada",
        "tipo": "equipamento",
        "slot": "arma",
        "ataque": 1,
        "raridade": "Comum"
    },

    "lanca_goblin_rei": {
        "nome": "Lança do Goblin Rei",
        "tipo": "equipamento",
        "slot": "arma",
        "ataque": 3,
        "raridade": "Comum"
    },

    "armadura_goblin_rei": {
        "nome": "Armadura do Goblin Rei",
        "tipo": "equipamento",
        "slot": "armadura",
        "defesa": "2",
        "raridade": "Comum"
    },

    "armadura_couro": {
        "nome": "Armadura de Couro",
        "tipo": "equipamento",
        "slot": "armadura",
        "defesa": 1,
        "raridade": "Comum"
    },

    "espada_ferro": {
        "nome": "Espada de Ferro",
        "tipo": "equipamento",
        "slot": "arma",
        "ataque": 4,
        "raridade": "Raro"
    },

    "armadura_ferro": {
        "nome": "Armadura de Ferro",
        "tipo": "equipamento",
        "slot": "armadura",
        "defesa": 4,
        "raridade": "Raro"
    },

    "lamina_sombria": {
        "nome": "Lâmina Sombria",
        "tipo": "equipamento",
        "slot": "arma",
        "ataque": 10,
        "raridade": "Lendário"
    },

    "armadura_abismo": {
        "nome": "Armadura do Abismo",
        "tipo": "equipamento",
        "slot": "armadura",
        "defesa": 10,
        "raridade": "Lendário"
    }
}

def sortear_drop(boss, jogador):

    tabela_drop = boss.get("drops", [])
    loot_tipo = boss.get("loot_tipo", "multiplo")

    drops_recebidos = []

    if loot_tipo == "unico":
        roll = random.randint(1, 100)
        acumulado = 0

        for drop in tabela_drop:
            acumulado += drop["chance"]

            if roll <= acumulado:
                item_id = drop["item"]
                drops_recebidos.append(
                    ITENS[item_id].copy()
                )
                break
    else:
        for drop in tabela_drop:
            if random.randint(1, 100) <= drop["chance"]:
                item_id = drop["item"]
                drops_recebidos.append(
                    ITENS[item_id].copy()
                )
        
    return drops_recebidos

def equipar_item(jogador, item):
    slot = item["slot"]

    antigo = jogador["equipado"].get(slot)

    jogador["equipado"][slot] = item

    return antigo

RARIDADES = {
    "Comum": "⚪",
    "Raro": "🔵",
    "Épico": "🟣",
    "Lendário": "🟠",
    "Mítico": "🔴"
}