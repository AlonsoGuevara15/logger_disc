import discord
import os
import requests
import datetime

client = discord.Client()
teams = {
    'angurrientos': {
        'colour': 0x206694,
        'name': 'angurrientos',
        'thumbnail': 'https://cdn.discordapp.com/embed/avatars/0.png'
    },
    'waifus': {
        'colour': 0x1F8B4C,
        'name': 'loving waifus',
        'thumbnail': 'https://cdn.discordapp.com/embed/avatars/2.png'
    },
    'shockers': {
        'colour': 0xF1C40F,
        'name': 'shockers',
        'thumbnail': 'https://cdn.discordapp.com/embed/avatars/3.png'
    },
    'antiwillies': {
        'colour': 0xA84300,
        'name': 'antiwillies',
        'thumbnail': 'https://cdn.discordapp.com/embed/avatars/4.png'
    },
}
telito_img = 'https://cdn.discordapp.com/avatars/812045187383558145/9fe96a12a5381f16601ad817de2e760d.webp?size=1024'


@client.event
async def on_message(message):
    #print(message)
    channel = client.get_channel(811815022862794812)
    if message.author == client.user:
        return
    #header = '_ _\n\n\n'
    #footer = ''
    name_team = message.channel.name.split('-')[-1]
    from_team = teams.setdefault(
        name_team, {
            'colour': 0xFFF9F7,
            'name': name_team,
            'thumbnail': 'https://cdn.discordapp.com/embed/avatars/1.png'
        })

    embedVar = discord.Embed(title=from_team['name'].upper(),
                             description=message.content,
                             color=from_team['colour'],
                             timestamp=datetime.datetime.now())
    # embedVar.set_author(name=message.author.nick,icon_url=message.author.avatar_url)
    # embedVar.set_footer(text="Telito", icon_url=telito_img)
    if message.author.nick is None:
        embedVar.set_footer(text=message.author.name,
                            icon_url=message.author.avatar_url)
    else:
        embedVar.set_footer(text=message.author.nick,
                            icon_url=message.author.avatar_url)
    embedVar.set_thumbnail(url=from_team['thumbnail'])
    #embedVar.add_field(name="a", value=embed, inline=False)

    #if not len(message.attachments) > 0 and not len(message.embeds) > 0 :
    # print('es solo mensaje')
    # await channel.send(header + '**-{}**:\n > {}'.format(message.author.nick,message.content)+footer)
    await channel.send(embed=embedVar)
    if len(message.attachments) > 0:
        print('tiene attachments')
        url = message.attachments[0].url
        filename = message.attachments[0].filename
        r = requests.get(url, allow_redirects=True)
        open(filename, 'wb').write(r.content)
        # await channel.send(file=discord.File(filename))
        os.remove(filename)
    # for embed in message.embeds:
    # await channel.send(embed=embed)
    # pass


#embed = discord.Embed(title="title ~~(did you know you can have markdown here too?)~~", colour=discord.Colour(0xd18a56), url="https://discordapp.com", description="this supports [named links](https://discordapp.com) on top of the previously shown subset of markdown. ```\nyes, even code blocks```", timestamp=datetime.datetime.utcfromtimestamp(1613698831))

#embed.set_image(url="https://cdn.discordapp.com/embed/avatars/0.png")
#embed.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/0.png")
#embed.set_author(name="author name", url="https://discordapp.com", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
#embed.set_footer(text="footer text", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")

#embed.add_field(name="🤔", value="some of these properties have certain limits...")
#embed.add_field(name="😱", value="try exceeding some of them!")
#embed.add_field(name="🙄", value="an informative error should show up, and this view will remain as-is until all issues are fixed")
#embed.add_field(name="<:thonkang:219069250692841473>", value="these last two", inline=True)
#embed.add_field(name="<:thonkang:219069250692841473>", value="are inline fields", inline=True)

#await bot.say(content="this `supports` __a__ **subset** *of* ~~markdown~~ 😃 ```js\nfunction foo(bar) {\n  console.log(bar);\n}\n\nfoo(1);```", embed=embed)
