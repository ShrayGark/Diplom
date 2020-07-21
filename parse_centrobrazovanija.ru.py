from PrepareData import BaseParser, Finder
from models.models import Site, Course, Offer

bp = BaseParser()

url = f'https://centrobrazovanija.ru/servisy/kursy_povysheniya_kvalifikacii/?p='
bp.set_url(url)

s = Site(name='centrobrazovanija.ru')
s.save()


def find_course(page):
    finder = Finder()
    finder.set_data(page)
    name_pattern = '&quot;(.+)&quot;'
    names = finder.find_references(name_pattern)

    price_pattern = '(\d+) дн / (\d+) р.'
    prices = finder.find_references(price_pattern)

    i0 = 0
    for name in names:
        print(name)
        c = Course(site_id=s.id, name=name)
        c.save()
        of1 = Offer(course_id=c.id, duration_hours=0, duration_days=prices[i0][0],  price=prices[i0][1])
        of2 = Offer(course_id=c.id, duration_hours=0, duration_days=prices[i0 + 1][0],  price=prices[i0 + 1][1])
        i0 += 2
        of1.save()
        of2.save()
    return []


bp.start_parse(find_course, options=(1, 69))


