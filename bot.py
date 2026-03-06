
import datetime
import asyncio
import random
import discord
import time
from systems.itens import sortear_drop, ITENS
from systems.rpg import CombateView, verificar_level_up, InventarioView, calcular_status_total
from systems.bosses import BOSSES
from systems.economia import salvar_dados, carregar_dados, garantir_jogador
from systems.loja import ITENS_LOJA
import json
import yt_dlp
import os
from shindo import genkais, elementos, kenjutsus
from config import token
from discord.ext import commands
from discord.ui import View, Select
from discord import app_commands
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

pasta_audios = "audios"

ARQUIVO_ECONOMIA = "economia.json"

music_queues = {}
cooldown = 600
cooldown2 = 300
cooldown_aventura = 300
ultimo_trigger = 0

cooldown_aventura_usuarios = {}

bot = commands.Bot(command_prefix="f!", intents=intents)

GUILD_ID = 1452866624288981017

gif_bryan = "https://cdn.discordapp.com/attachments/1452866625211466004/1469411443442192395/image.png?ex=69878f8c&is=69863e0c&hm=dab26001f1c14499e473ae13cf8f69a971877cc93d9a2d538b2e4e7d3df8e666&"

def carregar_dados():
    if not os.path.exists(ARQUIVO_ECONOMIA):
        with open(ARQUIVO_ECONOMIA, "w") as f:
            json.dump({}, f)

    with open(ARQUIVO_ECONOMIA, "r") as f:
        return json.load(f)
    

def salvar_dados(dados):
    with open(ARQUIVO_ECONOMIA, "w") as f:
        json.dump(dados, f, indent=4)


frases_esq = [
    "oi esq linda",
    "gostosa",
    "concordo linda rs",
    "vdd linda, solteira?",
    "gostosa e burra, do jeitinho q eu gosto 😍"
]


gifs_bom_dia = [
    "https://tenor.com/nX70kwiuXsY.gif",
    "https://tenor.com/bm219.gif",
    "https://tenor.com/jva2G5pIPRG.gif",
    "https://tenor.com/mvCDLPjQrqI.gif"
]

gifs_boa_tarde = [
    "https://tenor.com/bJAcc.gif",
    "https://tenor.com/UIzq.gif",
    "https://tenor.com/bV2Tw.gif"
]

gifs_boa_noite = [
    "https://tenor.com/bvt26.gif",
    "https://makeagif.com/i/u95arh",
    "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExa3dmMDluY240ZGRzdjA1cTlzNXAydDZncHdxeDVvODVsYzJoMzZqOSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/gfvjSoO2f2GVWFtAeN/giphy.gif",
    "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExdXR2eXh1d2ptM2drNjk1dWNjMWZ3amlyNGM2bDJhajZpbjNwbWxnMiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/oNko8T7OeQw6ibIuI4/giphy.gif"
]

############################

#  EVENTOS

###########################


@bot.event
async def on_ready():
    guild = discord.Object(id=GUILD_ID)
    await bot.tree.sync(guild=guild)
    print(f"Sucessfully logged in as {bot.user}")

    #canal = bot.get_channel(1452866625211466004)
    #if canal:
       # await canal.send("senhoras e senhores, eu me caguei.")

@bot.event
async def on_message(message):
    global ultimo_trigger
    if message.author.bot:
        return
    
    conteudo = message.content.lower()

    if "bom dia" in conteudo:
        gif = random.choice(gifs_bom_dia)
        await message.channel.send(gif)

    elif "boa tarde" in conteudo:
        gif = random.choice(gifs_boa_tarde)
        await message.channel.send(gif)

    elif "boa noite" in conteudo:
        gif = random.choice(gifs_boa_noite)
        await message.channel.send(gif)

    elif message.author.id == 1066038751127674950:
        agora = time.time()
        if agora - ultimo_trigger >= cooldown:
            await message.channel.send(f"{gif_bryan}")
            ultimo_trigger = agora
            return

    #elif message.author.id == 1231276502897655889:
       # agora = time.time()
       # if agora - ultimo_trigger >= cooldown2:
            #esq = random.choice(frases_esq)
           # await message.channel.send(esq)
           # ultimo_trigger = agora

    elif "do gojo" in conteudo:
        await message.channel.send("do gojo")

    elif "dr nefario" in conteudo:
        await message.channel.send("https://cdn.discordapp.com/attachments/1452866625211466004/1476308425620066314/a91089f9736d3119165d07bbafbabdd9.mp4?ex=69a1f85d&is=69a0a6dd&hm=867bccadc07752dc793d7be1ae82f3c6869e709a8e3ae0a6eff4276c97c27237&")

    elif "late" in conteudo:
        await message.channel.send("https://cdn.discordapp.com/attachments/1456416506324713628/1473502181381378149/image.png?ex=69967158&is=69951fd8&hm=f9f087a782be550648772e1fe7ad0fed605ec30559f54121a16b77637611e24c&")

    elif "juro" in conteudo:
        await message.channel.send("https://cdn.discordapp.com/attachments/1456416506324713628/1473503858629021736/image.png?ex=699672e8&is=69952168&hm=d4556fc64e1db0ab5a6912cbda69254adbc9489baf6886cfaa014de2fbc75616&")


    await bot.process_commands(message)

##################

# COMANDOS

#################

@bot.tree.command(name="teste", description="sla oq colocar aq tbm", guild=discord.Object(id=GUILD_ID))
async def teste(interaction: discord.Interaction):

    embed = discord.Embed(
        title=f"Tenha um bom dia *{interaction.user.display_name}*",
        color=discord.Color.red()
    )

    embed.set_footer(text=f"agora eu sei aonde fica esse texto, obrigado {interaction.user.display_name}")

    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="perfil", description="Veja seu perfil", guild=discord.Object(id=GUILD_ID))
async def perfil(interaction: discord.Interaction):
    
    dados = carregar_dados()
    user_id = str(interaction.user.id)

    jogador = garantir_jogador(dados, user_id)

    salvar_dados(dados)

    xp_necessaria = jogador["nivel"] * 100
    barra = int((jogador["xp"] / xp_necessaria) * 10)

    barra_visual = "🟩" * barra + "⬜" * (10 - barra)

    embed = discord.Embed(
        title=f"Perfil de {interaction.user.display_name}",
        color=discord.Color.purple()

    )

    embed.add_field(
        name="Carteira",
        value=f"{jogador['saldo']} SlashCoins",
        inline=False
    )

    embed.add_field(
        name="Progressão",
        value=(
            f"XP: {jogador['xp']} / {xp_necessaria} \n"
            f"{barra_visual} \n"
            f"Nível: {jogador['nivel']}\n"
            f"Rank: {jogador['rank']}"
        ),
        inline=False
    )

    embed.add_field(
        name="Status",
        value=(
            f"HP: {jogador['hp']}\n"
            f"Ataque: {jogador['ataque']}\n"
            f"Defesa: {jogador['defesa']}"
        ),
        inline=False
    )

    embed.set_footer(text="Continue derrotando bosses para melhorar seus status!")

    await interaction.response.send_message(embed=embed)

@bot.tree.command(
        name="teste2",
        description="apenas um teste",
        guild=discord.Object(id=GUILD_ID)
)
async def teste2(interaction: discord.Interaction):
    embed = discord.Embed(
        title="atumalaca",
        color=discord.Color.ash_theme()
    )

    embed.add_field(
        name="Carteira",
        value=f"{"saldo"}",
        inline=False
    )

    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="aventura", description="Ganhe SlashCoins!", guild=discord.Object(id=GUILD_ID))
async def aventura(interaction: discord.Interaction):
    
    user_id = str(interaction.user.id)
    agora = time.time()
    
    # Verificar cooldown do usuário (não aplica ao dono do bot)
    if str(interaction.user.id) != str(MEU_ID):
        if user_id in cooldown_aventura_usuarios:
            ultimo_tempo = cooldown_aventura_usuarios[user_id]
            tempo_restante = cooldown_aventura - (agora - ultimo_tempo)
            
            if tempo_restante > 0:
                minutos = int(tempo_restante // 60)
                segundos = int(tempo_restante % 60)
                await interaction.response.send_message(
                    f"⏳ Aguarde **{minutos}m {segundos}s** antes de fazer outra aventura!",
                    ephemeral=True
                )
                return
        
        # Atualizar o tempo do último uso
        cooldown_aventura_usuarios[user_id] = agora
    
    dados = carregar_dados()

    if user_id not in dados:
        dados[user_id] = {"saldo": 0}

    ganho = random.randint(200, 5000)
    dados[user_id]["saldo"] += ganho

    salvar_dados(dados)

    embed = discord.Embed(
        title="Aventura Concluída!",
        description=f"Você ganhou **{ganho} SlashCoins** por matar alguns monstros.",
        color=discord.Color.yellow()
    )

    embed.add_field(
        name="Novo Saldo",
        value=f"{dados[user_id]['saldo']} SlashCoins",
        inline=False
    )
    embed.set_footer(text=f"Próxima aventura disponível em {cooldown_aventura // 60} minutos!")
    await interaction.response.send_message(embed=embed)


async def boss_autocomplete(
        interaction: discord.Interaction,
        current: str
):
    choices = []

    for key, boss in BOSSES.items():
        if current.lower() in boss["nome"].lower():
            choices.append(
                app_commands.Choice(
                    name=boss["nome"],
                    value=key
                )
            )

    return choices[:25]

@bot.tree.command(
        name="boss",
        description="enfrente um boss para ganhar XP, Coins e items!",
        guild=discord.Object(id=GUILD_ID))
@app_commands.describe(boss="Escolha o boss para enfrentar")
@app_commands.autocomplete(boss=boss_autocomplete)

async def boss(interaction: discord.Interaction, boss: str):
    boss_key = boss

    if boss_key not in BOSSES:
        await interaction.response.send_message(
            "Boss inválido.",
            ephemeral=True
        )
        return
    
    dados = carregar_dados()
    user_id = str(interaction.user.id)

    garantir_jogador(dados, user_id)
    salvar_dados(dados)

    view = CombateView(str(interaction.user.id), boss_key, interaction.user)
    embed = await view.atualizar_embed()

    await interaction.response.send_message(
        embed=embed,
        view=view,
        ephemeral=True
    )

@bot.tree.command(name="loja", description="Veja os itens da loja", guild=discord.Object(id=GUILD_ID))
async def loja(interaction: discord.Interaction):

    dados = carregar_dados()
    user_id = str(interaction.user.id)

    jogador = garantir_jogador(dados, user_id)

    embed = discord.Embed(
        title="Lojinha dos aventureiros",
        description="Itens disponíveis",
        color=discord.Color.gold()
    )

    for key, item in ITENS_LOJA.items():
        embed.add_field(
            name=item["nome"],
            value=f" {item['raridade']}\n Preço: {item['preco']} SlashCoins\n",
            inline=False
        )

    view = LojaView(jogador, dados, user_id)

    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

class LojaView(View):  
    def __init__(self, jogador, dados, user_id):
        super().__init__(timeout=60)
        self.add_item(LojaSelect(jogador, dados, user_id))


class LojaSelect(Select):
    def __init__(self, jogador, dados, user_id):

        self.jogador = jogador
        self.dados = dados
        self.user_id = user_id

        options = []

        for key, item in ITENS_LOJA.items():
            options.append(
                discord.SelectOption(
                    label=item["nome"],
                    description=f"{item['raridade']} • 💰 {item['preco']}",
                    value=key
                )
            )

        super().__init__(
            placeholder="Escolha um item para comprar",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):

        if str(interaction.user.id) != self.user_id:
            await interaction.response.send_message(
                "❌ Você não pode usar a loja de outro jogador.",
                ephemeral=True
            )
            return

        key = self.values[0]
        item = ITENS_LOJA[key]

        if self.jogador["saldo"] < item["preco"]:
            await interaction.response.send_message(
                "❌ Você não tem SlashzCoins suficientes.",
                ephemeral=True
            )
            return

        self.jogador["saldo"] -= item["preco"]
        self.jogador["inventario"].append(item.copy())

        salvar_dados(self.dados)

        await interaction.response.send_message(
            f"✅ Você comprou **{item['nome']}**!",
            ephemeral=True
        )


@bot.tree.command(name="inventario", description="Veja e equipe seus itens", guild=discord.Object(id=GUILD_ID))
async def inventario(interaction: discord.Interaction):
    
    dados = carregar_dados()
    user_id = str(interaction.user.id)

    jogador = garantir_jogador(dados, user_id)

    if not jogador["inventario"]:
        embed = discord.Embed(
            title=f"Inventário de {interaction.user.display_name}",
            description="**Seu inventário está vazio!**\n\nMate bosses para conseguir itens.",
            color=discord.Color.blurple()
        )
        
        await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )
        return

    # Garante que o jogador tenha o dicionário de equipados
    jogador.setdefault("equipado", {"arma": None, "armadura": None, "acessorio": None})

    # Usa a nova função para criar o embed
    from systems.rpg import criar_embed_inventario
    embed = criar_embed_inventario(jogador, interaction.user.display_name, modo="equipar")

    view = InventarioView(jogador, dados, user_id, modo="equipar")

    await interaction.response.send_message(
        embed=embed,
        view=view,
        ephemeral=True
    )


@bot.command()
async def genkai(ctx):
    if len(genkais) < 4:
        await ctx.send("❌ Não há genkais suficientes para sortear.")
        return

    sorteadas = random.sample(genkais, 4)

    msg = "**Suas Genkais Sorteadas:**\n"
    for g in sorteadas:
        msg += f"• {g}\n"

    await ctx.send(msg)

@bot.command()
async def elemento(ctx):
    if len(elementos) < 4:
        await ctx.send("❌ Não há elementos suficientes para sortear.")
        return

    sorteados = random.sample(elementos, 4)

    msg = "**🌪️ Seus Elementos Sorteados:**\n"
    for e in sorteados:
        msg += f"• {e}\n"

    await ctx.send(msg)

@bot.command()
async def kenjutsu(ctx):
    if len(kenjutsus) < 1:
        await ctx.send("❌ Não há kenjutsus suficientes para sortear.")
        return
    
    sorteados = random.sample(kenjutsus, 1)

    msg = "**⚔️ Seu Kenjutsu Sorteado:**\n"
    for k in sorteados:
        msg += f"• {k}\n"

    await ctx.send(msg)

    
async def get_audio_info(search):

    def extract():
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'default_search': 'ytsearch'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search, download=False)

            if 'entries' in info:
                info = info['entries'][0]

            return info['url'], info['title']

    return await asyncio.to_thread(extract)

@bot.command()
async def hora(ctx):
    agora = datetime.datetime.now()
    hora_formatada = agora.strftime("%H:%M:%S")
    await ctx.send(f"Agora são {hora_formatada}")


@bot.command()
async def data(ctx):
    dias_semana = {
        'Monday': 'Segunda-feira',
        'Tuesday': 'Terça-feira',
        'Wednesday': 'Quarta-feira',
        'Thursday': 'Quinta-feira',
        'Friday': 'Sexta-feira',
        'Saturday': 'Sábado',
        'Sunday': 'Domingo'
    }
    agora = datetime.datetime.now()
    dia_en = agora.strftime("%A")
    dia_pt = dias_semana[dia_en]
    data_formatada = f"{dia_pt}, {agora.strftime('%d/%m')}"

    await ctx.send(f"Hoje é {data_formatada}")

@bot.command()
async def leave(ctx):
    if ctx.author.id != MEU_ID:
        await ctx.send("só o menino flex pode usar esse comando ai chefe")
        return
    if ctx.author.voice is None:
        await ctx.send("como vou sair de um canal se n estou em um? chapou fio")
        return
    canal = ctx.author.voice.channel

@bot.command()
async def join(ctx):
    if ctx.author.id != MEU_ID:
        await ctx.send("só o menino flex pode usar esse comando ai chefe")
        return
    if ctx.author.voice is None:
        await ctx.send("Você não está em um canal de voz!")
        return
    
    canal = ctx.author.voice.channel
    if ctx.voice_client is not None:
        await ctx.send("Já estou em um canal de voz!")
    await canal.connect()



async def music_player(ctx):

    vc = ctx.voice_client
    guild_id = ctx.guild.id

    while music_queues[guild_id]:

        url, title = music_queues[guild_id].pop(0)

        FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }

        source = discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS)

        vc.play(source)

        await ctx.send(f"🎵 Tocando agora: {title}")

        while vc.is_playing() or vc.is_paused():
            await asyncio.sleep(1)


@bot.command()
async def play(ctx, *, search):
    if ctx.author.id != MEU_ID:
        await ctx.send("só o menino flex pode usar esse comando ai chefe")
        return

    if ctx.author.voice is None:
        await ctx.send("Entre em um canal de voz primeiro.")
        return

    canal = ctx.author.voice.channel

    if ctx.voice_client is None:
        await canal.connect()

    vc = ctx.voice_client
    guild_id = ctx.guild.id

    if guild_id not in music_queues:
        music_queues[guild_id] = []

    audio_url, title = await get_audio_info(search)

    music_queues[guild_id].append((audio_url, title))

    await ctx.send(f"✅ Adicionado à fila: {title}")

    if not vc.is_playing():
        await music_player(ctx)

@bot.command()
async def skip(ctx):
    if ctx.author.id != MEU_ID:
        await ctx.send("só o menino flex pode usar esse comando ai chefe")
        return

    vc = ctx.voice_client

    if vc and vc.is_playing():
        vc.stop()
        await ctx.send("⏭️ Música pulada.")

@bot.command()
async def stop(ctx):
    if ctx.author.id != MEU_ID:
        await ctx.send("só o menino flex pode usar esse comando ai chefe")
        return

    vc = ctx.voice_client

    if vc:
        music_queues[ctx.guild.id] = []
        await vc.disconnect()
        await ctx.send("⏹️ Player encerrado.")

@bot.command()
async def sair(ctx):
    if ctx.author.id != MEU_ID:
        await ctx.send("só o menino flex pode usar esse comando ai chefe")
        return
    
    canal = ctx.author.voice.channel
    if canal is None:
        ctx.send("Não estou em um canal para sair")
        return
    await ctx.voice_client.disconnect()

@bot.command()
async def pause(ctx):
    if ctx.author.id != MEU_ID:
        await ctx.send("só o menino flex pode usar esse comando ai chefe")
        return
    
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()


@bot.command()
async def resume(ctx):
    if ctx.author.id != MEU_ID:
        await ctx.send("só o menino flex pode usar esse comando ai chefe")
        return
    
    vc = ctx.voice_client
    if vc is None:
        await ctx.send("Não estou tocando nada.")
        return

    if vc and vc.is_paused():
        vc.resume()

lista_audios = [
    app_commands.Choice(name=arquivo.replace(".ogg", ""), value=arquivo)
    for arquivo in os.listdir(pasta_audios)
    if arquivo.endswith(".ogg")
]

@bot.tree.command(name="audio",description="Escolha um áudio", guild=discord.Object(id=GUILD_ID))
@app_commands.choices(nome=lista_audios)
async def audio(interaction: discord.Interaction, nome:app_commands.Choice[str]):

    caminho = f"{pasta_audios}/{nome.value}"
    file = discord.File(caminho)

    await interaction.response.send_message(file=file)



@bot.tree.command(name="falar", description="Faz o bot falar", guild=discord.Object(id=GUILD_ID))
async def falar(interaction: discord.Interaction, mensagem: str,):

    
    await interaction.response.defer(ephemeral=True)

    
    await interaction.channel.send(mensagem)


@bot.command()
async def calc(ctx, a: int, operador: str, b: int):
    resultado = None
    if operador == "+":
        resultado = a + b

    elif operador == "-":
        resultado = a - b

    elif operador == "*":
        resultado = a * b

    elif operador == "/":
        if b == 0:
            await ctx.send("não é possivel dividir por 0!")
            return
        resultado = a / b

    elif operador == "**":
        resultado = a ** b

    elif operador == "//":
        resultado = a // b
    
    elif operador == "%":
        resultado = a % b

    if resultado is None:
        await ctx.send("Operador inválido!")
        return

    await ctx.send(f"resultado: {resultado}")


MEU_ID = 388819771564490755

@bot.command()
async def ez(ctx):
    if ctx.author.id != MEU_ID:
        await ctx.send("Você não tem permissao para executar esse comando!")
        return
    await ctx.send("https://tenor.com/kV3gCCSsFxL.gif")

@bot.command()
async def gojo(ctx):
    await ctx.send("https://tenor.com/r9dSlA4IFln.gif")



    
@bot.tree.command(name="limpar_mensagem", description="Limpa mensagens de um usuário", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(
    usuario="Usuário para apagar as mensagens",
    quantidade="Quantidade de mensagens para apagar"
)
async def limpar_mensagem(
    interaction: discord.Interaction,
    usuario: discord.Member,
    quantidade: int
):
    if interaction.user.id != MEU_ID:
        await interaction.response.send_message(
            "Você não tem permissao para executar esse comando!",
            ephemeral=True
        )
        return
    
    await interaction.response.defer(ephemeral=True)
    
    if quantidade <= 0:
        await interaction.response.send.message(
            "Numbers count must be more than 0",
            ephemeral=True
        )
        return
    
    canal = interaction.channel
    apagadas = 0

    async for mensagem in canal.history(limit=100):
        if mensagem.author == usuario:
            try:
                await mensagem.delete()
                apagadas += 1
            except:
                pass

        if apagadas >= quantidade:
            break

    await interaction.followup.send(
        f"Foram apagadas {apagadas} mensagens de {usuario.mention}"
    )


from PIL import Image, ImageDraw, ImageFont
import math


def proxima_potencia_2(n):
    return 1 if n == 0 else 2**math.ceil(math.log2(n))


def criar_bracket(participantes):

    participantes = participantes.copy()

    
    n_original = len(participantes)

    
    n = proxima_potencia_2(n_original)

    
    while len(participantes) < n:
        participantes.append(None)

    rounds = int(math.log2(n))

    largura = 300 + rounds * 200
    altura = n * 80

    img = Image.new("RGB", (largura, altura), (30,30,30))
    draw = ImageDraw.Draw(img)

    
    font = ImageFont.truetype("arial.ttf", 22)

    posicoes = []

    
    for i, user in enumerate(participantes):

        y = i * 80 + 40
        x = 20

        nome = user.display_name if user else "BYE"

        draw.text((x, y), nome, font=font, fill=(255,255,255))

        linha_inicio = x + 150

        draw.line(
            (linha_inicio, y+10, linha_inicio+50, y+10),
            fill=(255,255,255),
            width=2
        )

        posicoes.append((linha_inicio+50, y+10))

    
    for r in range(1, rounds+1):

        novas_posicoes = []

        for i in range(0, len(posicoes), 2):

            (x1, y1) = posicoes[i]
            (x2, y2) = posicoes[i+1]

            novo_x = x1 + 150
            meio_y = (y1 + y2)//2

            
            draw.line((x1, y1, x1, y2), fill=(255,255,255), width=2)

            
            draw.line((x1, meio_y, novo_x, meio_y), fill=(255,255,255), width=2)

            novas_posicoes.append((novo_x, meio_y))

        posicoes = novas_posicoes

    caminho = "bracket.png"
    img.save(caminho)

    return caminho

class TorneioView(discord.ui.View):

    def __init__(self, autor_id):
        super().__init__(timeout=120)
        self.autor_id = autor_id
        self.participantes = []

        self.select = discord.ui.UserSelect(
            placeholder="Selecione os participantes",
            min_values=2,
            max_values=10
        )

        self.select.callback = self.select_callback
        self.add_item(self.select)

    async def select_callback(self, interaction: discord.Interaction):

        if interaction.user.id != self.autor_id:
            await interaction.response.send_message(
                "❌ Só quem criou pode escolher.",
                ephemeral=True
            )
            return

        self.participantes = self.select.values

        nomes = ", ".join(user.mention for user in self.participantes)

        await interaction.response.send_message(
            f"✅ Participantes:\n{nomes}",
            ephemeral=True
        )

    @discord.ui.button(label="Iniciar Torneio", style=discord.ButtonStyle.green)
    async def iniciar(self, interaction: discord.Interaction, button: discord.ui.Button):

        if interaction.user.id != self.autor_id:
            await interaction.response.send_message(
                "❌ Só quem criou o torneio pode iniciar.",
                ephemeral=True
            )
            return

        if len(self.participantes) < 2:
            await interaction.response.send_message(
                "⚠️ Selecione participantes primeiro.",
                ephemeral=True
            )
            return

        random.shuffle(self.participantes)

        lutas = []

        for i in range(0, len(self.participantes), 2):

            if i + 1 < len(self.participantes):
                p1 = self.participantes[i]
                p2 = self.participantes[i + 1]
                lutas.append(f"⚔️ {p1.mention} vs {p2.mention}")
            else:
                lutas.append(f"🔥 {self.participantes[i].mention} avança automaticamente")

        mensagem = "**🏆 TORNEIO SHINDO LIFE INICIADO 🏆**\n\n"
        mensagem += "\n".join(lutas)

        arquivo_img = criar_bracket(self.participantes)

        file = discord.File(arquivo_img)

        await interaction.response.send_message(
            mensagem,
            file=file
        )

        self.stop()


    
@discord.ui.button(label="Iniciar Torneio", style=discord.ButtonStyle.green)
async def iniciar(self, interaction: discord.Interaction, button: discord.ui.Button):

    if interaction.user.id != self.autor_id:
        await interaction.response.send_message(
            "Só quem criou o torneio pode iniciar.",
            ephemeral=True
        )
        return

    if len(self.participantes) < 2:
        await interaction.response.send_message(
            "Selecione pelo menos 2 participantes.",
            ephemeral=True
        )
        return

    random.shuffle(self.participantes)

    lutas = []
    for i in range(0, len(self.participantes), 2):

        if i + 1 < len(self.participantes):
            p1 = self.participantes[i]
            p2 = self.participantes[i + 1]
            lutas.append(f"⚔️ {p1.mention} vs {p2.mention}")
        else:
            lutas.append(f"🔥 {self.participantes[i].mention} avança automaticamente")

    mensagem = "**🏆 TORNEIO SHINDO LIFE INICIADO 🏆**\n\n"
    mensagem += "\n".join(lutas)

    arquivo_img = criar_bracket(self.participantes)
    file = discord.File(arquivo_img)

    await interaction.response.send_message(
        mensagem,
        file=file
    )

    self.stop()

@bot.command()
async def torneio(ctx):

    view = TorneioView(ctx.author.id)

    await ctx.send(
        "🏆 **Torneio Shindo Life**\nSelecione os participantes abaixo:",
        view=view
    )



@bot.tree.command(
        name="ban",
        description="Bane um usuário.",
        guild=discord.Object(id=GUILD_ID))
@app_commands.describe(
    usuario="Selecione o usuário para banir"
)
async def ban(
    interaction: discord.Interaction,
    usuario: discord.Member
):
    if interaction.user.id != MEU_ID:
        await interaction.response.send_message(
            "Você não tem permissão para executar esse comando!",
            ephemeral=True
        )
        return
    await interaction.guild.ban(usuario)

    await interaction.response.send_message(
        f"{usuario.mention} foi banido com sucesso."
    )

async def autocomplete_banidos(
        interaction: discord.Interaction,
        current: str
):
    banidos = []

    async for entry in interaction.guild.bans():
        user = entry.user

        if current.lower() in user.name.lower():
            banidos.append(
                app_commands.Choice(
                    name=f"{user.name} ({user.id})",
                    value=str(user.id)
                )
            )
    return banidos[:25]

@bot.tree.command(
        name="unban",
        description="Desbane um usuário.",
        guild=discord.Object(id=GUILD_ID))
@app_commands.describe(
    user_id="ID do usuário para desbanir"
)
@app_commands.autocomplete(user_id=autocomplete_banidos)
async def unban(
    interaction: discord.Interaction,
    user_id: str
):
    if interaction.user.id != MEU_ID:
        await interaction.response.send_message(
            "Você não tem permissão!",
            ephemeral=True
        )
        return
    
    try:
        user = await bot.fetch_user(int(user_id))
        await interaction.guild.unban(user)

        await interaction.response.send_message(
        f"{user.name} foi desbanido."
        )

    except:
        await interaction.response.send_message(
            "Não consegui desbanir esse usuário.",
            ephemeral=True
        )



bot.run(token)