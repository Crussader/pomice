from cmath import atan
from typing import TYPE_CHECKING, Optional, Tuple, Union, overload

from discord import AutoShardedClient, Client
from discord.ext import commands

from .exceptions import NoTrack, QueueFull
from .ext import spotify
from .objects import Playlist, Track


PlaylistType = Union[spotify.Playlist, spotify.Album, spotify.Artist]
TrackType = Union[spotify.Track, Track]

class Queue:
    """The Base Class for Queue"""

    def __init__(self, ctx: commands.Context = None, limit: int = None) -> None:
        self._ctx = ctx
        self._limit = limit
        self._player = ctx.voice_client

        self._queue = []
        self._current_pos = 0

    @property
    def size(self):
        """Returns the size of the Queue"""
        return len(self._queue)

    @property
    def queue(self):
        """Returns the Queue List"""
        return self._queue

    @property
    def ctx(self) -> Optional[commands.Context]:
        """Returns Context if Present else None is returned"""
        return self._ctx

    @property
    def player(self):
        """Returns Player if Present else None is returned"""
        return self._player

    @property
    def bot(self) -> Optional[Union[Client, AutoShardedClient]]:
        """Return the Bot Object itself if Present else None is Returned"""
        return self._ctx.bot if self._ctx else None

    @property
    def current(self) -> TrackType:
        """Returns the current song that is being Played."""
        if (self._limit is not None and self._limit >= self._current_pos) or \
           (self._limit is None and self._current_pos >= len(self._queue) - 1):
            return self._queue[self._current_pos]
        else:
            return None

    @property
    def is_full(self) -> bool:
        return False if self._limit is None else self.size == self._limit

    @property
    def next(self) -> TrackType:
        """Property that returns the Next Track in the queue.
           Note: This does not update the position of the queue.
        """
        if self._limit is None:
            if self._current_pos < len(self._queue) - 1:
                return self._queue[self._current_pos + 1]
        else:
            if self._limit > self._current_pos < len(self._queue) - 1:
                return self._queue[self._current_pos + 1]
        
        return None

    @property
    def previous(self) -> TrackType:
        """Property that returns """

        if 0 < self._current_pos <= len(self._queue) - 1:
            return self._queue[self._current_pos-1]

        return None

    def _append(self, obj):
        """Internal function"""
        if self.is_full:
            raise QueueFull("Max size of Queue has been reached.")
            
        self._queue.append(obj)

    def _extend(self, objs):
        """Adds tracks to the queue and if there is a limit to that queue
           then the remaining space in the Queue is filled with the tracks.
        """
        if self.is_full:
            raise QueueFull("Max size of Queue has been reached.")
        else:
            if self._limit is not None:
                space_left = self._limit - self.size
                self._queue.extend(objs[:space_left])
            else:
                self._queue.extend(objs)

    @overload
    def add_tracks(
        self,
        *tracks: TrackType
    ) -> None: ...

    @overload
    def add_tracks(
        self,
        playlist: PlaylistType
    ) -> None: ...

    def add_tracks(self, obj):
        """Add Tracks to a Playlist you can pass a playlist or a single Track also"""

        if isinstance(obj, (Playlist, spotify.Playlist, spotify.Album, spotify.Artist)):
            self._extend(obj.tracks)
        elif isinstance(obj, (spotify.Track, Track)):
            self._append(obj)
        elif isinstance(obj, tuple):
            self._extend(obj)

    def go_next(self) -> TrackType:
        """Go to the next track. This is not the same as `Queue.next` as
           this only returns the next track but this changes the position as well.
        """
        track = self.next
        if not track:
            raise NoTrack("There is no upnext Track.")

        self._current_pos += 1
        return track

    def pop(self) -> Tuple[int, TrackType]:
        """Pop a song from the Queue."""
        return self._current_pos, self._queue.pop(self._current_pos)

    @overload
    def insert_at(
        self,
        at: int,
        *tracks: TrackType
    ) -> None: ...
    
    @overload
    def insert_at(
        self,
        at: int,
        track: TrackType
    ) -> None: ...

    def insert_at(self, at, obj):

        if isinstance(obj, tuple):
            for track in obj:
                if self.is_full:
                    break

                self._queue.insert(at, track)
                at += 1
        else:
            if self.is_full:
                raise QueueFull("Max size of the Queue has reached.")
            else:
                self._queue.insert(at, obj)

        
