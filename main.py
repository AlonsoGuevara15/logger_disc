import discord
import os
from discord.ext import commands
from init_data import pinned_channels_ids
from utils import BotUtils

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='-', intents=intents)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    bot_utils = BotUtils(client)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="-help"))

    @client.event
    async def on_message(message):
        if message.channel.id not in pinned_channels_ids.values():
            await client.process_commands(message)
        else:
            if bot_utils.staff_roles.get('juez') in message.author.roles:
                await message.delete()

    def is_support(ctx):
        role_permission = bot_utils.staff_roles.get('support') in ctx.author.roles
        channel_permission = bot_utils.copa_channels.get('prueba') == ctx.channel
        return role_permission and channel_permission

    @client.command()
    @commands.check(is_support)
    async def send_welcome(ctx, *, arg):
        for member in ctx.message.mentions:
            await bot_utils.send_welcome_message(member)

    if os.getenv('DEPLOY', None):
        @client.event
        async def on_member_join(member):
            await bot_utils.send_welcome_message(member, cast=True)

    @client.event
    async def on_member_update(before, after):
        if len(before.roles) < len(after.roles):  # si se agregó un rol
            new_role = next(role for role in after.roles
                            if role not in before.roles)
            if str(new_role.id) in list(bot_utils.team_roles.keys()):  # si el nuevo rol es de un equipo
                for rol in after.roles:
                    if str(rol.id) in list(bot_utils.team_roles.keys()) and rol != new_role:  # elimina los roles de los otros equipos
                        await after.remove_roles(rol)
                print("send_team_embed")
                await bot_utils.send_team_embed(after, new_role.id)
            if new_role == bot_utils.staff_roles.get('support'):  # no se puede asignar el rol de soporte
                await after.remove_roles(new_role)
        else:  # si se eliminó un rol
            await after.move_to(None)  # se desconecta de los canales de voz

    def can_join_member(ctx):
        team_role = discord.utils.find(lambda r: str(r.id) in bot_utils.team_roles.keys(), ctx.author.roles)
        channel_permission = bot_utils.copa_channels.get('general') == ctx.channel
        return team_role is not None and channel_permission

    @client.command(
        brief='Invita un nuevo miembro a tu equipo',
        description='Seguido del comando, etiqueta a los nuevos miembros que quieras agregar a tu equipo'
    )
    @commands.check(can_join_member)
    async def join(ctx, *, arg):
        if bot_utils.staff_roles.get('juez') not in ctx.author.roles:

            new_role = discord.utils.find(lambda r: str(r.id) in bot_utils.team_roles.keys(), ctx.author.roles)
            for member in ctx.message.mentions:
                member_team_role = discord.utils.find(lambda r: r.id in bot_utils.team_roles.keys(), member.roles)
                if member_team_role is None:
                    await member.add_roles(new_role)
                    role_data = bot_utils.team_roles.get(str(new_role.id), None)
                    embed = discord.Embed(
                        colour=discord.Colour(role_data.get('colour')),
                        description="{} fue unid@ al equipo **{}**".format(member.mention, role_data.get('nombre')))
                    embed.set_author(icon_url=role_data.get('img'), name="NUEVO MIEMBRO")
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(
                        colour=discord.Colour(0x607D8B),
                        description=":warning: **{}** ya pertenece al equipo **{}**".format(member.display_name, member.roles[1].name))
                    await ctx.send(embed=embed)

    @client.command(brief='rules/retos')
    @commands.check(is_support)
    async def update_info(ctx, arg):
        if arg == "rules":
            ind_channel = bot_utils.copa_channels.get('rules')
            await ind_channel.purge(limit=100)

            await bot_utils.send_rules(channel_name='rules')

            await bot_utils.send_horario(channel_name='rules')
            await bot_utils.send_role_indication(channel_name='rules')
        elif arg == "retos":
            retos_channel = bot_utils.copa_channels.get('retos')
            await retos_channel.purge(limit=100)
            await bot_utils.send_retos(channel_name='retos')
        else:
            await ctx.send(
                "Argumentos de update_info: ```-update_info rules/retos```")

    @client.command(brief='roles/horario/retos')
    @commands.check(is_support)
    async def cast(ctx, arg):
        if arg == "roles":
            await bot_utils.send_role_indication(channel_name='general',
                                                 tag_everyone=True)
        elif arg == "horario":
            await bot_utils.send_horario(channel_name='general', tag_everyone=True)
        elif arg == "retos":
            await bot_utils.send_retos(channel_name='general', tag_everyone=True)
        else:
            await ctx.send("Argumentos de cast: ```-cast horario/roles/retos```")

    @client.command(brief='clean message history')
    @commands.check(is_support)
    async def clean(ctx):
        await ctx.channel.purge(limit=100)

    # @client.command()
    # @commands.check(is_support)
    # async def congrats(ctx):
    #     ang_role = get(bot_utils.copa_server.roles, id=880952067135537212)
    #     mentions = [user.mention for user in ang_role.members]
    #     public_message = "🟦 Felicidades 🟦﹒{}, ganadores de la :bat: **Copa Telecom 2021 - Edición Bicentenario** :flag_pe:! Gracias a los miembros {} por su participación :blue_heart:".format(
    #         ang_role.mention, " ".join(mentions))

    #     await general_channel.send(public_message, file=discord.File('angurrientos.jpeg'))

    #     for user in ang_role.members:
    #         private_message = "🟦 Felicidades 🟦﹒**@Angurrientos**, ganadores de la :bat: **Copa Telecom 2021 - Edición Bicentenario** :flag_pe:! Gracias {} por tu participación  :blue_heart:".format(
    #             user.mention)
    #         await user.send(private_message, file=discord.File('angurrientos.jpeg'))
    #         print("enviado a "+ user.name)

    # @client.command()
    # @commands.check(is_support)
    # async def send_bot_text(ctx, *, arg):
    #     for member in ctx.message.mentions:
    #       await send_text(member)

    # async def send_text(member=None):
    #     pm = copa_channels.get('welcome').get_partial_message(949551956538572820)
    #     fm = await pm.fetch()

    #     # embed = discord.Embed(colour=discord.Colour(0x1CBEE3),
    #     #                       description=fm.content)
    #     embed = fm.embeds[0]
    #     embed.set_author(icon_url=fm.author.avatar_url,
    #                                      name=fm.author.display_name)
    #     embed.set_footer(text=fm.author.display_name, icon_url=fm.author.avatar_url)
    #     await member.send(embed=embed)
    #     await copa_channels.get('bots').send(embed=embed)


if os.getenv('DEPLOY', None):
    from keep_alive import keep_alive

    keep_alive()

client.run(os.getenv('TOKEN'))
