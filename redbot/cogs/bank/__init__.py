from .bank import Bank, is_owner_if_bank_global

__all__ = ("is_owner_if_bank_global",)


def setup(bot):
    bot.add_cog(Bank(bot))
