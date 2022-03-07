import discord
import os
import json
from build_image import build_welcome_image, temp_dir
from init_data import get_server_data

event_files_dir = "event_files/"


class BotUtils:
    def __init__(self, client):
        self.copa_channels, self.staff_roles, self.team_roles, self.copa_server = get_server_data(client)
        with open(event_files_dir + 'utils_data.json', encoding="utf-8") as json_file:
            data = json.load(json_file)
            self.filenames = data.get("filenames")
            self.welcome_message_text = data.get("welcome_message_text")

    async def send_welcome_message(self, member, cast=False):
        filename = await build_welcome_image(member)
        welcome_message = self.welcome_message_text.format(
            user_mention=member.mention,
            rules_mention=self.copa_channels.get('rules').mention)

        if cast:
            await self.copa_channels.get('welcome').send(
                welcome_message, file=discord.File(temp_dir + 'edited_' + filename))

        await member.send(welcome_message,
                          file=discord.File(temp_dir + 'edited_' + filename))
        for f in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, f))

    async def send_team_embed(self, member, role_data):
        embed = discord.Embed(colour=discord.Colour(role_data.get('colour')), description="Bienvenid@ a **{}**!".format(
            role_data.get('nombre')))
        embed.set_thumbnail(url=str(member.avatar_url))
        channel = role_data.get('channel')
        embed.add_field(name=":bust_in_silhouette: Miembro:", value="{}".format(member.mention), inline=False)
        embed.add_field(name=":speech_left: Chat:", value="{}".format(channel.mention), inline=False)
        embed.set_author(name=member.display_name.upper(), icon_url=role_data.get('img'))
        embed.set_footer(text=self.copa_server.name, icon_url=self.copa_server.icon_url)

        await channel.send(embed=embed)
        await member.send(embed=embed)

    async def send_rules(self, channel_name=''):
        channel = self.copa_channels.get(channel_name)
        await channel.send(embed=discord.Embed(colour=discord.Colour(0x607D8B), title="BASES DE LOS EVENTOS"))
        await channel.send(file=discord.File(
            event_files_dir + self.filenames.get("rules")))

    async def send_horario(self, channel_name='', tag_everyone=False):
        embed = discord.Embed(colour=discord.Colour(0x607D8B),
                              title="HORARIO DE EVENTOS")
        # embed.set_image(url=os.getenv('HORARIO'))

        channel = self.copa_channels.get(channel_name)
        if tag_everyone:
            await channel.send("@everyone", embed=embed)
        else:
            await channel.send(embed=embed)
        await channel.send(file=discord.File(event_files_dir + self.filenames.get("horario")))

    async def send_role_indication(self, channel_name='', tag_everyone=False):
        embed = discord.Embed(
            colour=discord.Colour(0x607D8B),
            title="ROLES: INDICACIONES",
            description=
            "Existen dos maneras de ser asignado al rol de tu equipo:")
        embed.add_field(name="1. :judge:",
                        value="Un JUEZ les asigna manualmente",
                        inline=False)
        embed.add_field(
            name="2. :busts_in_silhouette:",
            value="Uno de sus compañeros ya asignados puede unirlos en {}, **etiquetandolos** con el siguiente comando: ```-join @usuarioDiscord1 [@usuarioDiscord2 ...]```"
                .format(self.copa_channels.get('general').mention),
            inline=False)
        embed.add_field(
            name="_ _",
            value=
            ":warning: Solo los jueces pueden revertir la asignación de un rol",
            inline=False)
        channel = self.copa_channels.get(channel_name)
        if tag_everyone:
            await channel.send("@everyone", embed=embed)
        else:
            await channel.send(embed=embed)

    async def send_retos(self, channel_name='', tag_everyone=False):
        channel = self.copa_channels.get(channel_name)
        if tag_everyone:
            await channel.send("@everyone")
        await channel.send(embed=discord.Embed(colour=discord.Colour(0x607D8B), title="EXCEL DE RETOS"))
        await channel.send(file=discord.File(event_files_dir + self.filenames.get("retos")))
