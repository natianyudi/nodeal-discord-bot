import asyncio

from discord.ext import commands


MAX_TIMER = 10


class Timer(commands.Cog):
    def __init__(self, discord_bot):
        self.bot = discord_bot
        self.running_channels = set()

    @commands.command(pass_context=True)
    async def timer(self, ctx, num: int, unit: str):
        """Create a timer with <num> <unit>"""
        if not self.is_timer_allowed(ctx.channel.id):
            await ctx.send("A timer is already started for this channel, please wait...")
            return
        # check arguments
        if not num or not unit:
            num = 20
            unit = 'min'
        else:
            if unit != 'min' and unit != 'sec':
                await ctx.send("Only min or sec is allowed")
                return
        await ctx.send(f'Time set to {num} {unit}')
        await self.countdown(num, unit, ctx.channel.id)

    async def countdown(self, num, unit, channel_id):
        total_seconds = num * 60 if unit == 'min' else num
        self.running_channels.add(channel_id)
        is_start = True
        while is_start:
            print(total_seconds)
            mins, secs = divmod(total_seconds, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            print(timer, end="\r")
            await asyncio.sleep(total_seconds)
            is_start = False
        channel = self.bot.get_channel(channel_id)
        await channel.send("Times up")
        self.running_channels.remove(channel_id)

    def is_timer_allowed(self, channel_id):
        if len(self.running_channels) >= MAX_TIMER:
            return False

        if channel_id in self.running_channels:
            return False

        return True
