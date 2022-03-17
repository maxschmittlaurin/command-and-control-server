# Author : Maximilien Schmitt-Laurin

from datetime import datetime
import aiohttp
import asyncio
import sys


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://127.0.0.1:7000/validate/status') as resp:
            print(resp.status)
            print(await resp.text())

if __name__ ==  '__main__':
    asyncio.run(main())