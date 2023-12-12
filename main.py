
from aiohttp import web
import aiohttp

routes = web.RouteTableDef()

@routes.get('/python')
async def hh_get_vac(request):
    url = "https://api.hh.ru/vacancies"
    params = {
        "text": 'python',
        "area": [72],  # Specify the desired area ID (72:Perm, 2:SPB, 1:MSC, 3:EKB)
        "per_page": 1,  # Number of vacancies per page
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url,
                       params=params) as resp:
            test = await resp.text()
            return web.Response(text = test, content_type='application/json')



@routes.get('/')
async def main(request):
    return web.Response(text='start')

            
# @routes.get('/{name}')
# async def variable_handler(request):
#     return web.Response(
#         text="Hello, {}".format(request.match_info['name']))

app = web.Application()
app.add_routes(routes)


if __name__ == '__main__':
    web.run_app(app)