import asyncio
import aiohttp
import requests
from database import filling_db


SW_API = 'https://swapi.dev/api/people/'


async def get_person(url: str):
    async with aiohttp.client.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


def name_generator(url_list):
    try:
        for url in url_list:
            req = requests.get(url)
            yield req.json()['name']
    except KeyError:
        for url in url_list:
            req = requests.get(url)
            yield req.json()['title']


async def get_homeworld_name(url: str):
    async with aiohttp.client.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


async def get_sw_persons():
    sw_persons_list = list()
    persons_tasks = [get_person(f'{SW_API}/{i}') for i in range(1, 25)]
    persons_info = await asyncio.gather(*persons_tasks)
    for person in persons_info:
        if person != {'detail': 'Not found'}:
            data = dict()
            data['birth_year'] = person['birth_year']
            data['eye_color'] = person['eye_color']
            data['films'] = ', '.join(name_generator(person['films']))
            data['gender'] = person['gender']
            data['hair_color'] = person['hair_color']
            data['height'] = person['height']
            planet = await get_homeworld_name(person['homeworld'])
            data['homeworld'] = planet['name']
            data['mass'] = person['mass']
            data['name'] = person['name']
            data['skin_color'] = person['skin_color']
            data['species'] = ', '.join(name_generator(person['species']))
            data['starships'] = ', '.join(name_generator(person['starships']))
            data['vehicles'] = ', '.join(name_generator(person['vehicles']))
            sw_persons_list.append(data)
    return list(sw_persons_list)


async def main():
    list_charact = await get_sw_persons()
    await filling_db(list_charact)


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
