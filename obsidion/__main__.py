"""Initialise and run the bot."""
import logging

from discord import Intents, AllowedMentions, ActivityType, Activity
from discord.ext.commands import when_mentioned_or
from obsidion.core.help import Help

from obsidion import _update_event_loop_policy
from obsidion.core.bot import Obsidion
from obsidion.core import get_settings
from obsidion.core.config import prefix_callable

_update_event_loop_policy()

log = logging.getLogger("obsidion")


async def get_prefix(bot, message):
    """Get prefix for the bot."""
    if message.guild is None:
        # Use default prefix in DM's
        return when_mentioned_or(get_settings().DEFAULT_PREFIX)(bot, message)
    else:
        extras = await prefix_callable(bot, message.guild)
        # extras = [get_settings().DEFAULT_PREFIX]
        return when_mentioned_or(*extras)(bot, message)


def main():
    """Main initialisation script."""
    # So no one can abuse the bot to mass mention
    allowed_mentions = AllowedMentions(everyone=False, roles=False, users=True)

    # We don't need many mentions so this is the bare minimum we eed
    intents = Intents.none()
    intents.messages = True
    intents.guilds = True
    intents.reactions = True

    activity = activity = Activity(
        name=get_settings().ACTIVITY,
        type=ActivityType.watching,
    )

    args = {
        "command_prefix": get_prefix,
        "case_insensitive": True,
        "description": "",
        "self_bot": False,
        "help_command": Help(),
        "owner_ids": [],
        "activity": activity,
        "intents": intents,
        "allowed_mentions": allowed_mentions,
    }

    obsidion = Obsidion(**args)

    # obsidion.remove_command("help")

    log.info("Ready to go, spinning up the gears")
    obsidion.run(get_settings().DISCORD_TOKEN)

    log.info("GearBot shutting down, cleaning up")
    # obsidion.database_connection.close()

    log.info("Cleanup complete")


if __name__ == "__main__":
    """Run the bot."""
    main()
