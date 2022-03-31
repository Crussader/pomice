import re

SOUNDCLOUD_URL_REGEX = re.compile(
    r"^(https?:\/\/)?(www.)?(m\.)?soundcloud\.com\/[\w\-\.]+(\/)+[\w\-\.]+/?$"
)

SPOTIFY_URL_REGEX = re.compile(
    r"https?://open.spotify.com/(?P<type>album|playlist|track)/(?P<id>[a-zA-Z0-9]+)"
)

DISCORD_MP3_URL_REGEX = re.compile(
    r"https?://cdn.discordapp.com/attachments/(?P<channel_id>[0-9]+)/"
    r"(?P<message_id>[0-9]+)/(?P<file>[a-zA-Z0-9_.]+)+"
)

URL_REGEX = re.compile(
    r"https?://(?:www\.)?.+"
)

SPOTIFY_URL_REGEX = re.compile(
    r"https?://open.spotify.com/(?P<type>album|playlist|track|artist)/(?P<id>[a-zA-Z0-9]+)"
)

APPLE_URL_REGEX = re.compile(
    r"https?://music.apple.com/(?P<type>album|artist|track)/(?P<name>[a-zA-Z0-9]+)+/(?P<id>[0-9]+)"
)