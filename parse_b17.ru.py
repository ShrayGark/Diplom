from PrepareData import BaseParser, Finder
from models.models import Site, Data

bp = BaseParser()

url = f'https://www.b17.ru/psiholog/tomsk/?page='
bp.set_url(url)


def find_links(page):
    finder = Finder()
    finder.set_data(page)
    ref_pattern = '<a href="/(.+)/" name=.+ class=h>([А-Я][а-я]+ [А-Я][а-я]+ [А-Я][а-я]+)</a>'
    ref = finder.find_references(ref_pattern)
    return ref


def find_id(page):
    finder = Finder()
    finder.set_data(page)
    ref_pattern = "show_kontakt_new\('spec_id_new','(.+)'\)"
    ref = finder.find_references(ref_pattern)
    # print(ref)
    return ref[0]


def find_phone(page):
    finder = Finder()
    finder.set_data(page)
    ref = finder.find_phone()
    return ref


res = bp.start_parse(find_links, options=(1, 10))

s = Site(name='b17.ru')
s.save()


progress = 0
max_ = len(res)

for link, fio in res:
    progress += 1
    print(f'{round(progress / max_ * 100, 2)}%')

    bp.set_url(f'https://www.b17.ru/{link}/')
    id = bp.start_parse(find_id, False)
    new_link = f'https://www.b17.ru/telefon_backend.php?mod=spec_id_new&id={id}'
    bp.set_url(new_link)
    phones = bp.start_parse(find_phone, False)
    d = Data(site_id=s.id, fullname=fio, email='', phone=phones)
    d.save()
