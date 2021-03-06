from redbot.core.bot import Red

from .alias import Alias


async def setup(bot: Red):
    cog = Alias(bot)
    bot.add_cog(cog)
    cog.sync_init()
