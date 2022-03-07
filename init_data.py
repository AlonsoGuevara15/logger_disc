from discord.utils import get

pinned_channels_ids = {
    'welcome_channel': 944809159298252800,
    'rules_channel': 944809197378343042,
    'retos_channel': 944809173068161025,
    'bots_channel': 944809106970140702,
}
roles_id = {
    'juez_role': 944814500345966672,
    'support_role': 944814825257730129,
}

other_channels_id = {
    'general_channel': 944807983286726701,
    'prueba_channel': 950392223864864898,
}

teams_init = [
    {
        'role_id': '944813737360125962',
        'channel_id': 944810001405472789,
        'colour': 0x0078d7,
        'img': 'https://media.discordapp.net/attachments/881035342789099540/882888290536157245/t1.png',
        'nombre': 'T1',
    },
    {
        'role_id': '944814018948898826',
        'channel_id': 944810039695269929,
        'colour': 0x16c60c,
        'img': 'https://media.discordapp.net/attachments/881035342789099540/882888295422492702/t2.png',
        'nombre': 'T2',
    },
    {
        'role_id': '944814080219287633',
        'channel_id': 944810065918034000,
        'colour': 0xfff100,
        'img': 'https://media.discordapp.net/attachments/881035342789099540/882888296806629416/t3.png',
        'nombre': 'T3',
    },
    {
        'role_id': '944814113610145792',
        'channel_id': 944810088248537088,
        'colour': 0xf7630c,
        'img': 'https://media.discordapp.net/attachments/881035342789099540/882888301235830784/t4.png',
        'nombre': 'T4',
    },
]


def get_server_data(client):
    copa_channels = {
        'welcome': client.get_channel(pinned_channels_ids.get('welcome_channel')),
        'prueba': client.get_channel(other_channels_id.get('prueba_channel')),
        'rules': client.get_channel(pinned_channels_ids.get('rules_channel')),
        'retos': client.get_channel(pinned_channels_ids.get('retos_channel')),
        'bots': client.get_channel(pinned_channels_ids.get('bots_channel')),
        'general': client.get_channel(other_channels_id.get('general_channel')),
    }
    copa_server = client.guilds[0]

    staff_roles = {
        'juez': get(copa_server.roles, id=roles_id.get('juez_role')),
        'support': get(copa_server.roles, id=roles_id.get('support_role')),
    }
    # await general_channel.purge(limit=100)
    team_roles = {}
    for team in teams_init:
        team_roles.update({
            team.get('role_id'): {
                'channel': client.get_channel(team.get('channel_id')),
                **team
            }
        })

    return copa_channels, staff_roles, team_roles, copa_server
