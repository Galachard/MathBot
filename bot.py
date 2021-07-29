import discord
import time
# import requests
# import json
import os
import asyncio
import random
import function_plotter
import calculating

token_file = open('TOKEN.txt', 'r')
TOKEN = token_file.readline()
token_file.close()

client = discord.Client()

# Commands
command_symbol = '%'    # Symbol used before every bot command
plot_text = 'plot'
calc_text = 'calc'

# Getting actual commands in every session of the bot
plot_com = command_symbol + plot_text + ' '
calc_com = command_symbol + calc_text + ' '

# def get_quote():
#     response = requests.get("https://zenquotes.io/api/random")
#     json_data = json.loads(response.text)
#     quote = json_data[0]['q'] + ' -' + json_data[0]['a']
#     return quote


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await message.channel.send(msg)

    if message.content.startswith('%???'):
        for i in range(20):
            await message.channel.send('????????????????????????????????????????????????????????????????????????????')
            time.sleep(0.6)

    if message.content.startswith('%start_loop'):
        for i in range(5):
            await message.channel.send('Hello world!')
            time.sleep(1)

    if message.content.startswith(plot_com):
        try:
            function_plotter.plot(message.content.replace(plot_com, ''))
        except ValueError:
            await message.channel.send('Plot command: Incorrect input!')
        except OverflowError:
            await message.channel.send('Plot command: Calculated number is too big!')
        except SyntaxError:
            await message.channel.send('Plot command: Are you okay in the head?!')
        else:
            await message.channel.send(file=discord.File("./images/graph.png"))
            os.remove("./images/graph.png")

    if message.content.startswith(calc_com):
        try:
            await message.channel.send('Calculated value: ' + str(calculating.calc(message.content.replace(calc_com, ''))))
        except ValueError:
            await message.channel.send('Calculate command: Incorrect input!')
        except OverflowError:
            await message.channel.send('Calculate command: Calculated number is too big!')


def main():
    client.run(TOKEN)


if __name__ == '__main__':
    main()
