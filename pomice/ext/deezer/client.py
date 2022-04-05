import asyncio
import itertools
import re

import aiohttp

try:
    import orjson
    json = orjson
except ImportError:
    import json

from ...regex import DEEZER_URL_REGEX
from .exceptions import DeezerRequestException, InvalidDeezerURL
from .objects import *

API_URL = "https://api.deezer.com/{type}/{id}{ext}?limit=50&index={index}"


class Client:
    """The Base client for the Deezer module of Pomice.
       This class will do alll the leg work of getting the data
       from any of Deezer Track, Album, Artist and Playlist URL you give it.

        NOTE: Sometimes it will slower because, the API does not use
              a Key, it uses the IP address from where the request is coming from
              and the rate limit of the API is 50 every 5 seconds so 10 per second.
    """

    def __init__(self):
        # threading will be faster since the api is slower.
        self.session = aiohttp.ClientSession()

    async def close(self):
        await self.session.close()

    async def search(self, *, query: str):

        async def _fetch_async(url, count):
            async with self.session.get(url) as resp:
                if resp.status != 200:
                    raise DeezerRequestException(
                        "Error while fetching results: %d %s" % (
                            resp.status, resp.reason)
                    )

                next_data = await resp.json(loads=json.loads)
                inner = [count]
                inner.extend(Track(track) for track in next_data['data'])
                tracks.append(inner)

        match = DEEZER_URL_REGEX.match(query)

        if not match:
            raise InvalidDeezerURL(
                "Invalid Deezer URL was passed to the Client. (%s)" % query)

        deezer_type = match.group('type')
        deezer_id = match.group('id')

        request_url = API_URL.format(type=deezer_type, id=deezer_id, 
                                     ext='', index=0)

        async with self.session.get(request_url) as resp:
            if resp.status != 200:
                raise DeezerRequestException(
                    "Error while fetching results: %d %s" % (
                        resp.status, resp.reason)
                )

            data = await resp.json(loads=json.loads)

        if deezer_type == 'track':
            return Track(data)
        elif deezer_type == 'album':
            return Album(data)
        else:
            tracks = []

            if deezer_type == 'playlist':
                cls = Playlist(data, [])
                inner = [0]
                inner.extend(Track(i) for i in data['tracks']['data'])
                tracks.append(inner)
                urls = [API_URL.format(type=deezer_type, id=deezer_id, ext='/tracks', index=off)
                        for off in range(50, data['nb_tracks']+50, 50)]
            else:
                cls = Artist(data, [])
                urls = [data['tracklist']]

            processes = [_fetch_async(url, count)
                         for count, url in enumerate(urls, start=1)]

            try:
                await asyncio.gather(*processes)
            except TimeoutError:
                for process in processes:
                    try:
                        await process
                    except RuntimeError:
                        continue


        tracks.sort(key=lambda i: False if isinstance(i, Track) else i[0])
        tracks = [track for track in itertools.chain(
                  *tracks) if not isinstance(track, int)]

        cls.tracks = tracks
        if cls.track_count == 0:
            cls.track_count = len(tracks)

        return cls

