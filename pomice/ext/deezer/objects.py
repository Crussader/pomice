class Title:
    """A helper class for Track, Artist, Album, Playlist Names"""

    def __init__(self, data):

        self.full = data.get('title')
        self.short = data.get('title_short')

    def __repr__(self) -> str:
        return f"<pomice.ext.deezer.Title full={self.full}>"

    def __str__(self) -> str:
        return self.full


class Picture:
    """A helper class for Album, Artist and Playlist Images"""

    def __init__(self, data):

        self.normal = data.get('cover') or data.get('picture')
        self.small = data.get('cover_small') or data.get('picture_small')
        self.medium = data.get('cover_medium') or data.get('picture_medium')
        self.big = data.get('cover_big') or data.get('picture_big')
        self.xl = data.get('cover_xl') or data.get('picture_xl')

    def __repr__(self) -> str:
        return f"<pomice.ext.deezer.Picture normal={self.normal}>"

    def __str__(self) -> str:
        return self.normal


class Track:
    """The Base class for Deezer Track"""

    def __init__(self, data: dict):

        self.id = data.get('id')
        self.title = Title(data)
        self.uri = data.get('link')
        self.duration = data.get('duration') * 1000  # it comes in seconds
        self.release_date = data.get('release_date')
        self.explict = data.get('explicit_lyrics')
        self.picture = Picture(data.get("album"))
        self.artists = ", ".join(i['name'] for i in data['contributors'])

    def __repr__(self) -> str:
        return (f"<pomice.ext.deezer.Track id={self.id} "
                f"title={self.title} duration={self.duration}>")

    def __eq__(self, __o) -> bool:
        return (isinstance(__o, Track) and __o.id == self.id)


class Album:
    """The Base class for Deezer Album"""

    def __init__(self, data: dict):

        self.id = data.get('id')
        self.title = data.get('title')
        self.uri = data.get('link')
        self.picture = Picture(data)
        self.release_date = data.get('release_date')
        self.explict = data.get('explicit_lyrics')
        self.track_count = data.get('nb_tracks')

        self.tracks = [Track(i) for i in data['tracks']['data']]

    def __repr__(self) -> str:
        return (f"<pomice.ext.deezer.Album id={self.id} "
                f"title={self.title} cover={self.picture}>")


class Artist:
    """The Base class for Deezer Artist"""

    def __init__(self, data: dict, tracks):

        self.id = data.get('id')
        self.name = data.get('name')
        self.uri = data.get('link')
        self.picture = Picture(data)

        self.tracks = tracks
        self.track_count = len(tracks)

    def __repr__(self) -> str:
        return (f"<pomice.ext.deezer.Artist id={self.id} "
                f"name={self.name} uri={self.uri} track_count={self.track_count}>")


class Playlist:
    """The base class for Deezer Playlists"""

    def __init__(self, data: dict, tracks) -> None:

        self.id = data.get('id')
        self.title = data.get('title')
        self.description = data.get('description') or 'None'
        self.track_count = data.get('nb_tracks')
        self.picture = Picture(data)
        self.uri = data.get('link')
        self.fans = data.get('fans')

        self.creator = data['creator']['name']

        self.tracks = tracks

    def __repr__(self) -> str:
        return (f"<pomice.ext.deezer.Playlist id={self.id} "
                f"title={self.title} description={self.description} "
                f"track_count={self.track_count} tracks={self.tracks}>")
