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
help_text = 'help'
plot_text = 'plot'
calc_text = 'calc'

# Getting actual commands in every session of the bot
help_com = command_symbol + help_text
plot_com = command_symbol + plot_text + ' '
calc_com = command_symbol + calc_text + ' '

# def get_quote():
#     response = requests.get("https://zenquotes.io/api/random")
#     json_data = json.loads(response.text)
#     quote = json_data[0]['q'] + ' -' + json_data[0]['a']
#     return quote


@client.event
async def on_ready():
    print('')
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('')


@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if message.content.startswith(help_com):
        if message.content == help_com or message.content == help_com + ' ':
            await message.channel.send('General help')  # General help and list of commands
        else:   # Help with specific commands
            message.content = message.content[len(help_com) + 1:]
            if message.content == plot_text:
                await message.channel.send('Plots the graph of a given function.'
                                           'Example: ' + plot_com + '2 * x^2 - 4 * x + 7')
            if message.content.startswith(calc_text):
                if message.content == calc_text:
                    await message.channel.send('Calculates the value of a given mathematical expression.\n' +
                                               'Example: ' + calc_com + '7 ^ 3 - 3! + sin(0)\n' +
                                               'Help for a specific function: ' + help_com + calc_text +
                                               'function (e.g. gcd)')
                else:
                    message.content = message.content[len(calc_text) + 1:]
                    for index in range(len(calculating.functions)):
                        f = calculating.functions[index].get_help(message.content)
                        if f is not None:
                            await message.channel.send(f[0] + ': ' + f[1] + '\n' +
                                                       'Example: ' + f[2][0] + ' ---> ' + f[2][1])
                            break

    if message.content.startswith('%hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await message.channel.send(msg)

    if message.content.startswith('%???'):
        for i in range(20):
            await message.channel.send('????????????????????????????????????????????????????????????????????????????')
            time.sleep(0.6)

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
        except ZeroDivisionError:
            await message.channel.send('Calculate command: Division by zero detected!')
        except ArithmeticError:
            await message.channel.send('Calculate command: Incorrect amount of arguments of a function!')


def main():
    calculating.load_functions()
    if not os.path.isdir('images'):
        print('"/images" not found. Creating a directory for images.')
        os.mkdir('./images')
    client.run(TOKEN)


if __name__ == '__main__':
    main()
