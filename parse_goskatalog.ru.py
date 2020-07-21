import json
from PrepareData import BaseParser
from models.models import Museum, Employee, Site


bp = BaseParser()

url = 'https://goskatalog.ru/muzfo-rest/rest/museums?cacheEnabled=true&offset=0&publicationLimit=false'
bp.set_url(url)


def find_name_and_id(page):
    museums = json.loads(page)["museums"]
    result = []
    for museum in museums:
        result.append({
            "id": museum["id"],
            "name": museum["name"]
        })
    return result


def find_email_and_employees(page):
    museum_data = json.loads(page)
    email = ""
    employees = []

    for contact in museum_data["contacts"]:
        if contact["typeId"] == 2:
            email = contact["contactValue"]

    for employ in museum_data["employees"]:
        employees.append({
            "name": employ["name"],
            "job": employ["jobTitle"]["name"]
        })

    return {
        "email": email,
        "employees": employees
    }


museums_data = bp.start_parse(find_name_and_id, False)

s = Site(name='goskatalog.ru')
s.save()


progress = 0
max_ = len(museums_data)

for museum_data in museums_data:
    progress += 1
    print(f'{round(progress / max_ * 100, 2)}%')

    detail_url = f'https://goskatalog.ru/muzfo-rest/rest/museums/{museum_data["id"]}'
    bp.set_url(detail_url)
    data = bp.start_parse(find_email_and_employees, False)
    m = Museum(site_id=s.id, name=museum_data['name'], email=data['email'])
    m.save()
    for employee in data['employees']:
        Employee(museum_id=m.id, job_title=employee['job'], fullname=employee['name']).save()
