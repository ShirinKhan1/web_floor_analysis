from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import time

URL = 'https://www.cian.ru/cat.php?bbox=47.2724951814%2C39.6504574531%2C47.3168156636%2C39.811132502&deal_type=sale&engine_version=2&in_polygon%5B1%5D=39.7599774_47.3042369%2C39.7562009_47.3056388%2C39.752081_47.3072743%2C39.7483045_47.3086762%2C39.7445279_47.3098444%2C39.740408_47.3105454%2C39.7362882_47.310779%2C39.7321683_47.3110127%2C39.7273618_47.3110127%2C39.7232419_47.3112463%2C39.719122_47.3110127%2C39.7150022_47.3098444%2C39.7112256_47.3086762%2C39.7074491_47.3070407%2C39.7040158_47.3051715%2C39.7009259_47.3030687%2C39.698866_47.3004986%2C39.6971494_47.2976949%2C39.6961194_47.2946575%2C39.6954328_47.2918537%2C39.6947461_47.28905%2C39.6950894_47.2862462%2C39.6971494_47.2836761%2C39.6995526_47.2813396%2C39.7026425_47.2794705%2C39.7064191_47.2783022%2C39.710539_47.2773677%2C39.7150022_47.2769004%2C39.719122_47.2764331%2C39.7235852_47.2764331%2C39.7280484_47.2764331%2C39.7321683_47.2769004%2C39.7362882_47.277134%2C39.740408_47.277835%2C39.7441846_47.2794705%2C39.7472745_47.2815733%2C39.7503644_47.2836761%2C39.753111_47.2857789%2C39.7555142_47.2881154%2C39.7575742_47.2906855%2C39.7592908_47.2939565%2C39.7599774_47.2967603%2C39.7596341_47.299564%2C39.7575742_47.3021341%2C39.7555142_47.3047042%2C39.7599774_47.3042369&offer_type=flat&polygon_name%5B1%5D=Область+поиска&room1=1&room2=1&room3=1&room4=1&sort=creation_date_desc'


def parse(url):
    r = requests.get(url)
    bs = BeautifulSoup(r.content, 'html.parser')
    a_href = bs.find('a', class_='_93444fe79c--link--VtWj6')
    return a_href.get('href')


def monitoring(url):
    parsed_url = urlparse(url)
    if parsed_url.hostname == 'www.cian.ru':
        query_parameters = parse_qs(parsed_url.query)
        try:
            if query_parameters['sort'][0] == "creation_date_desc":
                return parse(url)
            else:
                query_parameters['sort'][0] = 'creation_date_desc'
                updated_query = urlencode(query_parameters, doseq=True)
                url = urlunparse(
                    (parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, updated_query,
                     parsed_url.fragment))
        except KeyError:
            url += '&sort=creation_date_desc'
    return False


def streaming(finish: int, url: str):
    start = time.time()
    while start - time.time() < finish * 60:
        monitoring(url)
        time.sleep(60)


if __name__ == '__main__':
    # print(parse(URL))
    pass
