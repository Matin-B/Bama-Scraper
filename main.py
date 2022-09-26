import requests


def scrape_ads(city: str) -> list:
    main_url = f'https://bama.ir/cad/api/search?region={city}'
    ads_list = []
    count = 2

    response = requests.get(main_url, headers=headers)
    data = response.json()
    metadata = data['metadata']
    has_next = metadata['has_next']
    ads = data['data']['ads']
    ads_list.extend(ads)

    while has_next is True:
        url = main_url + f'&pageIndex={count}'
        response = requests.get(url, headers=headers)
        data = response.json()
        metadata = data['metadata']
        has_next = metadata['has_next']
        ads = data['data']['ads']
        ads_list.extend(ads)
        print(f'Page {count}')
        count += 1
    return ads_list


def get_phone_number():
    ads_list = scrape_ads('isfahan')
    ads_code = set([ad['detail']['code'] for ad in ads_list])
    phone_numbers = []
    count = 1
    for ad_code in ads_code:
        url = f'https://bama.ir/cad/api/detail/{ad_code}/phone'
        response = requests.get(url, headers=headers)
        data = response.json()['data']
        try:
            phone_numbers.extend(data['mobile'])
        except Exception:
            continue
        print(count + '. ' + ad_code)
        count += 1


headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9,fa;q=0.8",
    "sec-ch-ua": (
        "'Google Chrome';v='105', 'Not)A;Brand';v='8', 'Chromium';v='105'"
    ),
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "'Linux'",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
        " (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
    ),
}

