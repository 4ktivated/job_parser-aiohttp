
from aiohttp import web
import aiohttp

routes = web.RouteTableDef()

@routes.get('/')
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
            #вот тут надо распарсить 
            # date['items'][0]['schedule'] занятость insite/remote
            #  date['items'][0]['apply_alternate_url'] ссылка на apply
            #   date['items'][0]['professional_roles'] роль 
            date = await resp.json()
            test = date.get("items", {}) # первый элемант items это list в идеале просто распаковать 
            vacancy_title = test.get("name")
            vacancy_url = test.get("alternate_url")
            company_name = test.get("employer", {}).get("name")
            experience = test.get('experience', {}).get('name')
            
            #Костыль с зарплатой из-за неправильного форматирования
            if test.get('salary', {}) and test.get('salary', {}).get("from") and test.get('salary', {}).get('to'):
               salary_from = test.get('salary', {}).get("from")
               salary_to = test.get('salary', {}).get('to')
               salary = f'{salary_from} - {salary_to}'
            elif test.get('salary', {}) and not test.get('salary', {}).get("from"):
                salary = test.get('salary', {}).get('to')
            elif test.get('salary', {}) and not test.get('salary', {}).get("to"):
                salary = test.get('salary', {}).get('from')
            else:
                salary = 'Не указанна'

            #это выглядит ужасно да и не работает, надо разобрать json который шлёт HH в запросе по параметрам 
            answer = f'lang: text, Title: {vacancy_title}, Company: {company_name}, URL: {vacancy_url}, Salary: {salary}, Info: {experience}'
            return web.Response(body=answer, content_type='application/json')



@routes.get('/1')
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