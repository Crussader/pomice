from typing import Optional

from discord.ext import commands

from pomice_rewrite.ext.deezer.objects import Artist


from .ext import spotify, deezer
from .enums import SearchType
from .regex import SOUNDCLOUD_URL_REGEX


class Track:
    """The base track object. Returns critical track information needed for parsing by Lavalink.
       You can also pass in commands.Context to get a discord.py Context object in your track.
    """

    def __init__(
        self,
        *,
        track_id: str,
        info: dict,
        ctx: Optional[commands.Context] = None,
        search_type: SearchType = SearchType.ytsearch,
        other_source: bool = False,
        source_track = None
    ):
        self.track_id = track_id
        self.info = info
        self.other_source = other_source

        self.original: Optional[Track] = None if other_source else self
        self._search_type = search_type
        self.source_track = source_track

        self.title = info.get("title")
        self.author = info.get("author")
        self.uri = info.get("uri")
        self.identifier = info.get("identifier")
        
        if info.get("thumbnail"):
            self.thumbnail = info.get("thumbnail")
        elif SOUNDCLOUD_URL_REGEX.match(self.uri):
            # ok so theres no feasible way of getting a Soundcloud image URL
            # so we're just gonna leave it blank for brevity
            self.thumbnail = None
        else:
            self.thumbnail = f"https://img.youtube.com/vi/{self.identifier}/mqdefault.jpg"

        self.length = info.get("length")
        self.ctx = ctx
        self.requester = self.ctx.author if ctx else None
        self.is_stream = info.get("isStream")
        self.is_seekable = info.get("isSeekable")
        self.position = info.get("position")

    def __eq__(self, other):
        if not isinstance(other, Track):
            return False

        if self.ctx and other.ctx:
            return other.track_id == self.track_id and other.ctx.message.id == self.ctx.message.id

        return other.track_id == self.track_id

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"<Pomice.track title={self.title!r} uri=<{self.uri!r}> length={self.length}>"

    @classmethod
    def from_spotify_track(
        cls, 
        track: spotify.Track,
        search_type: SearchType = SearchType.ytsearch,
        ctx: Optional[commands.Context] = None, 
    ):
        """classmethod which converts a `spotify.Track` to `Track`"""
        
        if not isinstance(track, spotify.Track):
            raise TypeError(f"You have to pass a Spotify Track not {track!r}")
        
        return cls(
                track_id=track.id,
                ctx=ctx,
                search_type=search_type,
                other_source=True,
                source_track=track,
                info={
                    "title": track.name,
                    "author": track.artists,
                    "length": track.length,
                    "identifier": track.id,
                    "uri": track.uri,
                    "isStream": False,
                    "isSeekable": True,
                    "position": 0,
                    "thumbnail": track.image
                }
            )

    @classmethod
    def from_deezer_track(
        cls,
        track: deezer.Track,
        search_type: SearchType = SearchType.ytsearch,
        ctx: Optional[commands.Context] = None
    ):
        """Classmethod which converts a `deezer.Track` to `Track`"""

        if not isinstance(track, deezer.Track):
            raise TypeError(f"You have to pass a Deezer Track not {track!r}")
        
        return cls(
                track_id=track.id,
                ctx=ctx,
                search_type=search_type,
                other_source=True,
                source_track=track,
                info={
                    "title": track.title,
                    "author": track.artists,
                    "lenght": track.duration,
                    "identifier": track.id,
                    "uri": track.uri,
                    "isStream": False,
                    "isSeekable": True,
                    "position": 0,
                    "thumbnail": track.picture.normal
                }
            )


class Playlist:
    """The base playlist object.
       Returns critical playlist information needed for parsing by Lavalink.
       You can also pass in commands.Context to get a discord.py Context object in your tracks.
    """

    def __init__(
        self,
        *,
        playlist_info: dict,
        tracks: list,
        ctx: Optional[commands.Context] = None,
        other_source: bool = False,
        source_playlist = None
    ):
        self.playlist_info = playlist_info
        self.tracks_raw = tracks
        self.other_source = other_source
        self.name = playlist_info.get("name")
        self.source_playlist = source_playlist

        self._thumbnail = None
        self._uri = None
        
        if self.other_source:
            self.tracks = tracks
            if isinstance(self.source_playlist, (spotify.Playlist, spotify.Album, spotify.Artist)):
                self._thumbnail = self.source_playlist.image
            elif isinstance(self.source_playlist, (deezer.Playlist, deezer.Artist, deezer.Album)):
                self._thumbnail = self.source_playlist.picture.normal
                
            self._uri = self.source_playlist.uri
        else:
            self.tracks = [
                Track(track_id=track["track"], info=track["info"], ctx=ctx)
                for track in self.tracks_raw
            ]
            self._thumbnail = None
            self._uri = None

        if (index := playlist_info.get("selectedTrack")) == -1:
            self.selected_track = None
        else:
            self.selected_track = self.tracks[index]

        self.track_count = len(self.tracks)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Pomice.playlist name={self.name!r} track_count={len(self.tracks)}>"

    @property
    def uri(self) -> Optional[str]:
        """Spotify album/playlist URI, or None if not a Spotify object."""
        return self._uri

    @property
    def thumbnail(self) -> Optional[str]:
        """Spotify album/playlist thumbnail, or None if not a Spotify object."""
        return self._thumbnail
