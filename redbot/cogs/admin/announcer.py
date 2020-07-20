import asyncio
import contextlib
import logging
from typing import Optional

import discord
from redbot.core import commands
from redbot.core.i18n import Translator
from redbot.core.utils import AsyncIter
from redbot.core.utils.chat_formatting import humanize_list, inline

_ = Translator("Announcer", __file__)

log = logging.getLogger("red.cogs.admin.announcer")


class Announcer:
    def __init__(self, ctx: commands.Context, message: str, config=None):
        """
        :param ctx:
        :param message:
        :param config: Used to determine channel overrides
        """
        self.ctx = ctx
        self.message = message
        self.config = config

        self.active = None
        self._task = None
        self._failed = None

    def start(self):
        """
        Starts an announcement.
        :return:
        """
        if self.active is None:
            self.active = True
            asyncio.create_task(self.announcer())

    def cancel(self):
        """
        Cancels a running announcement.
        :return:
        """
        if self._task is not None:
            self._task.cancel()

    async def _get_announce_channel(self, guild: discord.Guild) -> Optional[discord.TextChannel]:
        channel_id = await self.config.guild(guild).announce_channel()
        channel = None

        if channel_id is not None:
            channel = guild.get_channel(channel_id)

        if channel is None:
            channel = guild.system_channel

        if channel is None:
            with contextlib.suppress(IndexError):
                channel = guild.text_channels[0]

        return channel

    async def guild_announce(self, guild: discord.Guild) -> None:
        if await self.config.guild(guild).announce_ignore():
            return

        channel = await self._get_announce_channel(guild)

        if channel is None:
            # No channel to send to
            self._failed.append(str(guild.id))
            return

        try:
            if not channel.permissions_for(guild.me).send_messages:
                raise RuntimeError
            await channel.send(self.message)
        except (discord.Forbidden, RuntimeError):
            # Bot doesn't have permission to send messages in announcement channel.
            self._failed.append(str(guild.id))
            return

    async def announcer(self):
        guild_list = list(self.ctx.bot.guilds)
        self._failed = []
        self._task = asyncio.gather(
            *(self.guild_announce(guild) for guild in guild_list), return_exceptions=True
        )

        try:
            results = await self._task
        except asyncio.CancelledError:
            # The running announcement was cancelled
            pass
        else:
            for idx, result in enumerate(results):
                if result is not None:
                    guild_id = str(guild_list[idx].id)
                    log.error(
                        "There was an unhandled exception during announcement for guild with ID %s",
                        guild_id,
                        exc_info=result,
                    )
                    self._failed.append(guild_id)

        if self._failed:
            msg = (
                _("I could not announce to the following server: ")
                if len(self._failed) == 1
                else _("I could not announce to the following servers: ")
            )
            msg += humanize_list(tuple(map(inline, self._failed)))
            await self.ctx.bot.send_to_owners(msg)

        self.active = False
