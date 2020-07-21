from PrepareData import BaseParser, Finder
from models.models import Site, Data

bp = BaseParser()

url = f'https://www.9111.ru/uristy/russia/?p='
bp.set_url(url)


def find_links(page):
    finder = Finder()
    finder.set_data(page)
    ref_pattern = 'href="(.+)" target="_blank">([А-Я][а-я]+ [А-Я][а-я]+ [А-Я][а-я]+)</a>'
    ref = finder.find_references(ref_pattern)
    return ref


def find_email(page):
    finder = Finder()
    finder.set_data(page)
    ref = finder.find_email()
    return ref


res = bp.start_parse(find_links, options=(40, 45))


s = Site(name='9111.ru')
s.save()


progress = 0
max_ = len(res)

for link, fio in res:
    progress += 1
    print(f'{round(progress/max_*100, 2)}%')
    bp.set_url(link+'contacts/')
    emails = ','.join(bp.start_parse(find_email, False))
    d = Data(site_id=s.id, fullname=fio, email=emails, phone='')
    d.save()
