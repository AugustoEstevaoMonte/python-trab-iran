import asyncio
from contextlib import suppress
from datetime import datetime
from requests import get
from os import makedirs
from os.path import exists
from urllib.parse import urljoin
from pprint import pprint
from shutil import rmtree, copyfileobj

base_url = "https://pokeapi.co/api/v2/"
path = "download"

if exists(path):
    rmtree(path)
makedirs(path)

async def download_file(name, url, *, path=path, file_type='png'):
    response = await loop.run_in_executor(None, get, url)
    fname = f'{path}/{name}.{file_type}'
    with open(fname, 'wb') as file:
        copyfileobj(response.raw, file)
    return fname

async def get_sprite_url(url, sprite='front_default'):
    response = await loop.run_in_executor(None, get, url)
    return response.json()['sprites'][sprite]

async def main():
    start_time = datetime.now()

    pokemons = (await loop.run_in_executor(None, get, urljoin(base_url, 'pokemon/?limit=100'))).json()['results']
    image_url = {pokemon['name']: await get_sprite_url(pokemon['url']) for pokemon in pokemons}

    tasks = [download_file(name, url) for name, url in image_url.items()]
    files = await asyncio.gather(*tasks)

    time_elapsed = datetime.now() - start_time

    print(f'Tempo total: {time_elapsed.total_seconds():.2f} segundos')
    pprint(files)

loop = asyncio.get_event_loop()
with suppress(KeyboardInterrupt):
    loop.run_until_complete(main())
