import asyncio

from discord.ext import commands


MAX_TIMER = 10


async def run_timer(seconds):
    is_start = True
    while is_start:
        print(seconds)
        mins, secs = divmod(seconds, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        await asyncio.sleep(seconds)
        is_start = False


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
        # Get total seconds
        total_seconds = num * 60 if unit == 'min' else num
        # Add channel id to set so that only one timer is allowed per channel
        self.running_channels.add(channel_id)
        # Start timer thread
        await run_timer(total_seconds)
        # Send message when timer is done
        channel = self.bot.get_channel(channel_id)
        await channel.send("Times up")
        # Remove channel from set to allow new timer
        self.running_channels.remove(channel_id)

    def is_timer_allowed(self, channel_id):
        if len(self.running_channels) >= MAX_TIMER:
            return False

        if channel_id in self.running_channels:
            return False

        return True
