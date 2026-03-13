import discord
from discord.ui import Select, View
import random
from systems.itens import sortear_drop, RARIDADES
from systems.economia import carregar_dados, salvar_dados, garantir_jogador
from systems.bosses import BOSSES

class CombateView(discord.ui.View):
    def __init__(self, user_id, boss_key, user):
        super().__init__(timeout=60)

        self.user_id = user_id
        self.user = user
        self.dados = carregar_dados()
        self.jogador = garantir_jogador(self.dados, user_id)
        self.boss = BOSSES[boss_key].copy()

    def get_status_total(self):
        ataque = self.jogador["ataque"]
        defesa = self.jogador["defesa"]

        for slot in self.jogador["equipado"].values():
            if slot:
                ataque += slot.get("ataque", 0)
                defesa += slot.get("defesa", 0)

        return ataque, defesa


    async def atualizar_embed(self):
        ataque_total, defesa_total = self.get_status_total()

        embed = discord.Embed(
            title=f"⚔️ Batalha contra {self.boss['nome']}",
            color=discord.Color.red()
        )

        embed.add_field(
            name="🧍 Jogador HP",
            value=(
                f"HP: {self.jogador['hp']}\n"
                f"Ataque: {ataque_total}\n"
                f"Defesa: {defesa_total}"
            ),
            inline=True
        )

        embed.add_field(
            name="👾 Boss",
            value=f"HP: {self.boss['hp']}",
            inline=True
        )

        return embed

    @discord.ui.button(label="⚔️ Atacar", style=discord.ButtonStyle.red)
    async def atacar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if str(interaction.user.id) != self.user_id:
            await interaction.response.send_message(
                "Essa batalha não é sua!",
                ephemeral=True
            )
            return
        
        ataque_total, defesa_total = self.get_status_total()

        dano = max(1, ataque_total - 2)
        self.boss["hp"] -= dano

        if self.boss["hp"] <= 0:
            self.jogador["hp"] = 100
            self.jogador["xp"] += self.boss["xp"]
            self.jogador["saldo"] += self.boss["coins"]

            itens = sortear_drop(self.boss, self.jogador)

            mensagem_drop = ""

            for item in itens:
                self.jogador["inventario"].append(item)
                mensagem_drop += f"\n {item['nome']} dropado!"

            if not itens:
                mensagem_drop = "\n Nenhum item dropou."

            upou, mensagens = verificar_level_up(self.jogador)

            salvar_dados(self.dados)

            mensagem_final = "Boss derrotado!\n"

            if mensagens:
                mensagem_final += "\n".join(mensagens)

            mensagem_final += mensagem_drop



            embed = discord.Embed(
                title="Boss Derrotado!",
                description=f"**{self.user.display_name}** derrotou **{self.boss['nome']}**!",
                color=discord.Color.gold()
            )
        
            embed.add_field(name="XP", value=self.boss["xp"])
            embed.add_field(name="SlashCoins", value=self.boss["coins"])

            if mensagem_drop:
                embed.add_field(name="Drop", value=mensagem_drop, inline=False)

            if mensagens:
                embed.add_field(
                    name="Level Up",
                    value="\n".join(mensagens),
                    inline=False
                )

            await interaction.response.edit_message(
                content="Combate Encerrado",
                embed=None,
                view=None
            )

            await interaction.channel.send(embed=embed)
            return

        dano_boss = max(1, self.boss["ataque"] - defesa_total)
        self.jogador["hp"] -= dano_boss

        if self.jogador["hp"] <= 0:
            self.jogador["hp"] = 100
            salvar_dados(self.dados)

            await interaction.response.edit_message(
                content="💀 Você foi derrotado...",
                embed=None,
                view=None
            )
            return
        salvar_dados(self.dados)

        embed = await self.atualizar_embed()

        await interaction.response.edit_message(
            content=f"Você causou {dano} de dano!\nO boss causou {dano_boss} de dano!",
            embed=embed,
            view=self
        )

    @discord.ui.button(label="🧪 Usar poção", style=discord.ButtonStyle.green)
    async def usar_pocao(self, interaction: discord.Interaction, button: discord.ui.Button):

        if str(interaction.user.id) != self.user_id:
            await interaction.response.send_message(
                "Essa batalha não é sua!",
                ephemeral=True
            )
            return
        
        pocao_index = None
        for i, item in enumerate(self.jogador["inventario"]):
            if item['tipo'] == "consumivel" and "cura" in item:
                pocao_index = i
                break

        if pocao_index is None:
            await interaction.response.send_message(
                "Você não tem poção!",
                ephemeral=True
            )
            return
        
        item = self.jogador["inventario"].pop(pocao_index)

        cura = item["cura"]
        self.jogador["hp"] += cura
        
        def get_hp_max(self):
            hp = 100
            
            for slot in self.jogador["equipado"].values():
                if slot:
                    hp += slot.get("hp", 0)

                return hp
            

        hp_max = self.get_hp_max()
        if self.jogador["hp"] > hp_max:
            self.jogador["hp"] = hp_max
        
        ataque_total, defesa_total = self.get_status_total()

        dano_boss = max(1, self.boss["ataque"] - defesa_total)
        self.jogador["hp"] -= dano_boss


        if self.jogador["hp"] <= 0:
            self.jogador["hp"] = 100
            salvar_dados(self.dados)

            await interaction.response.send_message(
                "Você usou poção mas o boss te matou..",
                embed=None,
                view=None
            )
            return
        
        salvar_dados(self.dados)
        
        embed = await self.atualizar_embed()
        await interaction.response.edit_message(
            content=f"Você usou uma poção e recuperou {cura} HP!",
            embed=embed,
            view=self
        )

def calcular_xp_necessaria(nivel):
    return int(100 * (nivel ** 1.2))

def verificar_level_up(jogador):
    upou = False
    mensagens = []

    while jogador["xp"] >= calcular_xp_necessaria(jogador["nivel"]):
        jogador["xp"] -= calcular_xp_necessaria(jogador["nivel"])
        jogador["nivel"] += 1
        jogador["hp"] += 10
        jogador["ataque"] += 2
        jogador["defesa"] += 1

        mensagens.append(f"Você subiu para o nível {jogador['nivel']}!")
        upou + True

    rank_upou, rank_antigo, novo_rank = atualizar_rank(jogador)

    if rank_upou:
        jogador["hp"] += 20
        jogador["ataque"] += 5
        jogador["defesa"] += 3

        mensagens.append(
            f" RANK UP! {rank_antigo} ➜ {novo_rank}!\n"
            "Você recebeu bônus extra!"
        )
    return upou, mensagens

def atualizar_rank(jogador):
    rank_antigo = jogador.get("rank", "E")

    nivel = jogador["nivel"]

    if nivel >= 280:
        novo_rank = "SSS"
    
    elif nivel >= 250:
        novo_rank = "SS"

    elif nivel >= 200:
        novo_rank = "S"

    elif nivel >= 140:
        novo_rank = "A"

    elif nivel >= 90:
        novo_rank = "B"

    elif nivel >= 50:
        novo_rank = "C"

    elif nivel >= 20:
        novo_rank = "D"

    else:
        novo_rank = "E"

    jogador["rank"] = novo_rank

    if rank_antigo != novo_rank:
        return True, rank_antigo, novo_rank
    
    return False, rank_antigo, novo_rank


def calcular_status_total(jogador):
    ataque = jogador['ataque']
    defesa = jogador['defesa']
    hp = jogador['hp']

    for item in jogador["equipado"].values():
        if item:
            ataque += item.get("ataque", 0)
            defesa += item.get("defesa", 0)
            hp += item.get("hp", 0)

    return ataque, defesa, hp
        
class InventarioSelect(Select):
    def __init__(self, jogador, dados, user_id, modo="equipar"):
        self.jogador = jogador
        self.dados = dados
        self.user_id = user_id
        self.modo = modo

        options = []

        if modo == "equipar":
            # Mostra itens do inventário para equipar
            for index, item in enumerate(jogador["inventario"]):
                if item.get("tipo") == "equipamento":
                    options.append(
                        discord.SelectOption(
                            label=item["nome"],
                            description=f"{item['raridade']} • {item['slot']} • +{item.get('ataque', 0)}⚔️/{item.get('defesa', 0)}🛡️",
                            value=str(index)
                        )
                    )
            
            super().__init__(
                placeholder="Selecione itens para EQUIPAR (múltiplo)",
                min_values=1,
                max_values=min(10, len(options)) if options else 1,
                options=options
            )
        else:
            # Mostra itens equipados para desequipar
            for slot, item in jogador["equipado"].items():
                if item:
                    options.append(
                        discord.SelectOption(
                            label=item["nome"],
                            description=f"{item['raridade']} • {slot}",
                            value=slot
                        )
                    )
            
            super().__init__(
                placeholder="Selecione itens para DESEQUIPAR (múltiplo)",
                min_values=1,
                max_values=len(options) if options else 1,
                options=options
            )

    async def callback(self, interaction: discord.Interaction):
        if str(interaction.user.id) != self.user_id:
            await interaction.response.send_message(
                "Você não pode mexer no inventário de outro jogador.",
                ephemeral=True
            )
            return
        
        if self.modo == "equipar":
            # Equipar múltiplos itens
            indices_ordenadas = sorted([int(v) for v in self.values], reverse=True)
            itens_equipados = []
            erros = []
            
            for index in indices_ordenadas:
                if index >= len(self.jogador["inventario"]):
                    continue
                    
                item = self.jogador["inventario"][index]
                
                if item.get("tipo") != "equipamento":
                    erros.append(f"*{item['nome']}* não é um equipamento")
                    continue
                
                slot = item["slot"]
                
                # Remove item do inventário
                self.jogador["inventario"].pop(index)
                
                # Guarda item antigo do slot
                antigo = self.jogador["equipado"].get(slot)
                if antigo:
                    self.jogador["inventario"].append(antigo)
                
                # Equipa novo item
                self.jogador["equipado"][slot] = item
                itens_equipados.append(f"**{item['nome']}**")
            
            salvar_dados(self.dados)
            
            mensagem = "✅ Itens equipados:\n" + "\n".join(f"• {item}" for item in itens_equipados)
            if erros:
                mensagem += "\n⚠️ Erros:\n" + "\n".join(erros)
            
            await interaction.response.send_message(
                mensagem,
                ephemeral=True
            )
        else:
            # Desequipar múltiplos itens
            slots_selecionados = self.values
            itens_desequipados = []
            
            for slot in slots_selecionados:
                item = self.jogador["equipado"].get(slot)
                if item:
                    self.jogador["equipado"][slot] = None
                    self.jogador["inventario"].append(item)
                    itens_desequipados.append(f"**{item['nome']}**")
            
            salvar_dados(self.dados)
            
            mensagem = "✅ Itens desequipados:\n" + "\n".join(f"• {item}" for item in itens_desequipados)
            
            await interaction.response.send_message(
                mensagem,
                ephemeral=True
            )


class InventarioView(View):
    def __init__(self, jogador, dados, user_id, modo="equipar"):
        super().__init__(timeout=60)
        self.jogador = jogador
        self.dados = dados
        self.user_id = user_id
        self.modo = modo
        self.atualizar_view()
    
    def atualizar_view(self):
        # Limpa itens antigos
        self.clear_items()
        
        # Adiciona o select com o modo atual
        self.add_item(InventarioSelect(self.jogador, self.dados, self.user_id, self.modo))
        
        # Adiciona botões de modo
        self.add_item(BotaoModo(modo="equipar", modo_atual=self.modo, label="🎮 Equipar"))
        self.add_item(BotaoModo(modo="desequipar", modo_atual=self.modo, label="🔓 Desequipar"))
        self.add_item(BotaoAtualizar(jogador=self.jogador, dados=self.dados, user_id=self.user_id, modo=self.modo))


class BotaoModo(discord.ui.Button):
    def __init__(self, modo, modo_atual, label):
        super().__init__(
            label=label,
            style=discord.ButtonStyle.primary if modo == modo_atual else discord.ButtonStyle.secondary,
            custom_id=f"modo_{modo}"
        )
        self.modo = modo
    
    async def callback(self, interaction: discord.Interaction):
        if str(interaction.user.id) != self.user_id:
            await interaction.response.send_message(
                "Você não pode mexer no inventário de outro jogador.",
                ephemeral=True
            )
            return
        
        # Recria a view com o novo modo
        view = InventarioView(self.view.jogador, self.view.dados, self.view.user_id, self.modo)
        
        # Atualiza o embed
        embed = criar_embed_inventario(self.view.jogador, interaction.user.display_name, self.modo)
        
        await interaction.response.edit_message(embed=embed, view=view)


class BotaoAtualizar(discord.ui.Button):
    def __init__(self, jogador, dados, user_id, modo):
        super().__init__(
            label="🔄 Atualizar",
            style=discord.ButtonStyle.gray,
            custom_id="atualizar_inventario"
        )
        self.jogador = jogador
        self.dados = dados
        self.user_id = user_id
        self.modo = modo
    
    async def callback(self, interaction: discord.Interaction):
        if str(interaction.user.id) != self.user_id:
            await interaction.response.send_message(
                "Você não pode mexer no inventário de outro jogador.",
                ephemeral=True
            )
            return
        
        # Recarrega os dados
        from systems.economia import carregar_dados
        dados_atuais = carregar_dados()
        self.jogador = dados_atuais[self.user_id]
        
        view = InventarioView(self.jogador, dados_atuais, self.user_id, self.modo)
        embed = criar_embed_inventario(self.jogador, interaction.user.display_name, self.modo)
        
        await interaction.response.edit_message(embed=embed, view=view)


def criar_embed_inventario(jogador, nome_usuario, modo="equipar"):
    embed = discord.Embed(
        title=f"🎒 Inventário de {nome_usuario}",
        description=f"**Modo atual:** {modo.upper()}\n*Selecione múltiplos itens para equipar/desequipar de uma vez*",
        color=discord.Color.blurple()
    )
    
    # Itens equipados
    texto_equipado = ""
    slots = ["arma", "armadura", "acessorio"]
    
    for slot in slots:
        item = jogador["equipado"].get(slot)
        if item:
            texto_equipado += f"**{slot.title()}:** {item['nome']} ({item['raridade']})\n"
        else:
            texto_equipado += f"**{slot.title()}:** *Vazio*\n"
    
    embed.add_field(
        name="⚔️ Equipados",
        value=texto_equipado,
        inline=True
    )
    
    # Inventário
    if modo == "equipar":
        itens_equipamento = [item for item in jogador["inventario"] if item.get("tipo") == "equipamento"]
        
        if itens_equipamento:
            texto_inventario = ""
            for i, item in enumerate(itens_equipamento):
                texto_inventario += f"{i+1}. {item['nome']} ({item['raridade']}) - {item['slot']}\n"
        else:
            texto_inventario = "*Nenhum equipamento no inventário*"
        
        embed.add_field(
            name="🎒 Inventário (Equipamentos)",
            value=texto_inventario,
            inline=True
        )
    else:
        # Modo desequipar - mostra resumo do inventário
        total_itens = len(jogador["inventario"])
        embed.add_field(
            name="🎒 Inventário",
            value=f"Total de {total_itens} itens no inventário",
            inline=True
        )
    
    return embed
