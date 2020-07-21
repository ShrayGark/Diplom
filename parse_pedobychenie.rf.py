from PrepareData import BaseParser, Finder
from models.models import Site, Course, Offer

bp = BaseParser()

url = f'https://xn--90afccar8afg8b5b.xn--p1ai/catalog/prepodavatel_vuza_ssuza/?PAGEN_1='
bp.set_url(url)


def find_links(page):
    finder = Finder()
    finder.set_data(page)
    # print(page)
    ref_pattern = '<a href="(.+)" id="bx_.+" title="([А-Яа-я -]+)"'
    ref = finder.find_references(ref_pattern)
    return ref


def find_price(page):
    finder = Finder()
    finder.set_data(page)

    time_pattern = '(\d+) час[а-я]+,.+ (\d+) дн[а-я]+'
    time = finder.find_references(time_pattern)
    time = list(set(time))

    price_pattern = '\d+ \d{3} руб.'
    price = finder.find_references(price_pattern)

    result = []
    i0 = 0

    for item in time:
        result.append({
            'days': item[1],
            'hours': item[0],
            'full_price': price[i0],
            'special_price': price[i0 + 1]})
        i0 += 2
    return result


res = bp.start_parse(find_links, options=(1, 4))

s = Site(name='pedobychenie.rf')
s.save()

progress = 0
max_ = len(res)

for link, name in res:
    progress += 1
    print(f'{round(progress / max_ * 100, 2)}%')

    bp.set_url(f'https://xn--90afccar8afg8b5b.xn--p1ai{link}')
    prices = bp.start_parse(find_price, False)
    c = Course(site_id=s.id, name=name)
    c.save()
    for price in prices:
        Offer(course_id=c.id,
              duration_hours=price['hours'],
              duration_days=price['days'],
              price=price['full_price']).save()
