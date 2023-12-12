import asyncio
import aiohttp


async def hh_get_vac():
    url = "https://api.hh.ru/vacancies"
    params = {
        "text": 'python',
        "area": [72],  # Specify the desired area ID (72:Perm, 2:SPB, 1:MSC, 3:EKB)
        "per_page": 1,  # Number of vacancies per page
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url,
                       params=params) as resp:
            print(await resp.text())



async def main():
    t1 = asyncio.create_task(hh_get_vac())
    await t1
asyncio.run(main())


