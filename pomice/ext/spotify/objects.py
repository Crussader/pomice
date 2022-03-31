from typing import List

class PartialTracks:
    """The base class for Partial Tracks

       This holds the url which will searched 
       when the song is going to be played along 
       with the next 100 songs that is returned by the api.
    """

    def __init__(self, uri: str, obj):
        self._uri = uri
        self._list = obj

    def __repr__(self):
        return f"<Pomice.ext.spotify.PartialTracks url={self._uri}>"

class Track:
    """The base class for a Spotify Track"""

    def __init__(self, data: dict, image = None) -> None:
        self.name = data["name"]
        self.artists = ", ".join(artist["name"] for artist in data["artists"])
        self.length = data["duration_ms"]
        self.id = data["id"]

        if data.get("album") and data["album"].get("images"):
            self.image = data["album"]["images"][0]["url"]
        else:
            self.image = image

        if data["is_local"]:
            self.uri = None
        else:
            self.uri = data["external_urls"]["spotify"]

    def __repr__(self) -> str:
        return (
            f"<Pomice.ext.spotify.Track name={self.name} artists={self.artists} "
            f"length={self.length} id={self.id}>"
        )

class Album:
    """The base class for a Spotify album"""

    def __init__(self, data: dict) -> None:
        self.name = data["name"]
        self.artists = ", ".join(artist["name"] for artist in data["artists"])
        self.image = data["images"][0]["url"]
        self.tracks = [Track(track, image=self.image) for track in data["tracks"]["items"]]
        self.total_tracks = data["total_tracks"]
        self.id = data["id"]
        self.uri = data["external_urls"]["spotify"]

    def __repr__(self) -> str:
        return (
            f"<Pomice.ext.spotify.Album name={self.name} artists={self.artists} id={self.id} "
            f"total_tracks={self.total_tracks} tracks={self.tracks}>"
        )


class Artist:
    """The base class for a Spotify artist"""

    def __init__(self, data: dict, tracks: list) -> None:
        self.name = f"Top tracks for {data['name']}" 
        self.genres = ", ".join(genre for genre in data["genres"])
        self.followers = data["followers"]["total"]
        self.image = data["images"][0]["url"]
        self.tracks = tracks
        self.total_tracks = len(tracks)
        self.id = data["id"]
        self.uri = data["external_urls"]["spotify"]

    def _create_partial(self, next_urls: list):
        if next_urls:
            self.tracks.extend(PartialTracks(url, self) for url in next_urls)

    def __repr__(self) -> str:
        return (
            f"<Pomice.ext.spotify.Artist name={self.name} id={self.id} "
            f"total_tracks={self.total_tracks} tracks={self.tracks}>"
        )

class Playlist:
    """The base class for a Spotify playlist"""

    def __init__(self, data: dict, tracks: List[Track]) -> None:
        self.name = data["name"]
        self.tracks = tracks
        self.owner = data["owner"]["display_name"]
        self.total_tracks = data["tracks"]["total"]
        self.id = data["id"]
        if data.get("images") and len(data["images"]):
            self.image = data["images"][0]["url"]
        else:
            self.image = None
        self.uri = data["external_urls"]["spotify"]

    def _create_partial(self, next_urls: list):
        if next_urls:
            self.tracks.extend(PartialTracks(url, self) for url in next_urls)

    def __repr__(self) -> str:
        return (
            f"<Pomice.ext.spotify.Playlist name={self.name} owner={self.owner} id={self.id} "
            f"total_tracks={self.total_tracks} tracks={self.tracks}>"
        )

