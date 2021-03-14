"""Package for Trivia cog."""
from .trivia import Trivia, get_core_lists

__all__ = ("get_core_lists",)


def setup(bot):
    """Load Trivia."""
    cog = Trivia()
    bot.add_cog(cog)
