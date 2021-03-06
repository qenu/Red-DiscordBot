from redbot.core.bot import Red

from .filter import Filter


async def setup(bot: Red) -> None:
    cog = Filter(bot)
    await cog.initialize()
    bot.add_cog(cog)
