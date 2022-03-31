class PomiceException(Exception):
    """Base of all Pomice exceptions."""


class NodeException(Exception):
    """Base exception for nodes."""


class NodeCreationError(NodeException):
    """There was a problem while creating the node."""


class NodeConnectionFailure(NodeException):
    """There was a problem while connecting to the node."""


class NodeConnectionClosed(NodeException):
    """The node's connection is closed."""
    

class NodeNotAvailable(PomiceException):
    """The node is currently unavailable."""


class NoNodesAvailable(PomiceException):
    """There are no nodes currently available."""
    

class TrackInvalidPosition(PomiceException):
    """An invalid position was chosen for a track."""
    

class TrackLoadError(PomiceException):
    """There was an error while loading a track."""
    

class FilterInvalidArgument(PomiceException):
    """An invalid argument was passed to a filter."""
    

class SpotifyAlbumLoadFailed(PomiceException):
    """The pomice Spotify client was unable to load an album."""
    

class SpotifyTrackLoadFailed(PomiceException):
    """The pomice Spotify client was unable to load a track."""
    

class SpotifyPlaylistLoadFailed(PomiceException):
    """The pomice Spotify client was unable to load a playlist."""
    

class InvalidSpotifyClientAuthorization(PomiceException):
    """No Spotify client authorization was provided for track searching."""

class QueueFull(PomiceException):
    """The Queue reached its max size."""

class NoTrack(PomiceException):
    """There is no Track which is Previous or next of the Queue."""