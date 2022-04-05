import re

import aiohttp

APPLE_URL_REGEX_COUNTRY = re.compile(
    r"https?://music.apple.com/([a-z]+)/(?P<type>album|artist|track)/(?P<name>[a-zA-Z0-9-]+)/(?P<id>[0-9]+)"
)

APPLE_URL_REGEX = re.compile(
    r"https?://music.apple.com/(?P<type>album|artist|track)/(?P<name>[a-zA-Z0-9-]+)/(?P<id>[0-9]+)"
)

BASE_URL = "https://itunes.apple.com/lookup?id={id}"

class Client:

    def __init__(self):
        
        self.session = aiohttp.ClientSession()

    async def search(self, *, query: str):

        match = APPLE_URL_REGEX_COUNTRY.match(query)
        if not match:
            match = APPLE_URL_REGEX.match(query)
        
        type_ = match.group('type')
        id = match.group('id')

        request_url = BASE_URL.format(id=id)
        print(request_url)
        async with self.session.get(request_url) as resp:

            print(await resp.json(content_type="text/javascript"))
            

if __name__ == '__main__':
    import asyncio

    async def main():
        apple = Client()

        # url = "https://music.apple.com/in/artist/ark-patrol/848565657"
        url = "https://music.apple.com/in/album/close-eyes/1573608254?i=1573608260"
        await apple.search(query=url)

        await apple.session.close()

    asyncio.run(main())