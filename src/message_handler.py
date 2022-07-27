import os

from discord.ext import commands
from src.apps.timer import Timer

help_command = commands.DefaultHelpCommand(
    no_category='Commands'
)

bot = commands.Bot(command_prefix='$', help_command=help_command)


@bot.event
async def on_ready():
    print('Bot is now online and ready to roll')


@bot.listen('on_message')
async def whatever_you_want_to_call_it(message):
    if message.author == bot.user:
        return

    if message.content == 'hello':
        await message.channel.send(f'hey')

bot.add_cog(Timer(bot))

bot.run(os.environ['BOT_SECRET'])



