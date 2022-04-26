"""
Pomice Re-write
~~~~~~
The modern Lavalink wrapper designed for discord.py.
"""
import discord

if not discord.__version__.startswith("2.0"):
    class DiscordPyOutdated(Exception):
        pass

    raise DiscordPyOutdated(
        "You must have discord.py 2.0 or a discord.py fork that uses the 'discord' namespace "
        "(a.k.a: you import the libary using 'import discord') to use this library. "
        "Uninstall your current version and install discord.py 2.0 or a compatible fork."
    )

__version__ = "1.2"
__title__ = "pomice"
__author__ = "cloudwithax"

from .enums import *
from .exceptions import *
from .ext import deezer, spotify
from .filters import *
from .objects import *
from .player import *
from .queues import *
from .regex import *
