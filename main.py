import json

import requests
from bs4 import BeautifulSoup

# pip3 install -r requirements.txt -t ./python     

# http://checkshorturl.com/
# https://asq.co.kr/
# https://lazyjubu.tistory.com/entry/%EB%8B%A8%EC%B6%95-url-%EC%83%9D%EC%84%B1-%EB%B0%8F-url-%EB%B3%B5%EC%9B%90-%EC%82%AC%EC%9D%B4%ED%8A%B8-%EC%86%8C%EA%B0%9Cbitlycom-bitlykr-bitlycokr

# bitly
# r = requests.get(url + '+')

# han.gl
# r = requests.get(url + '+', allow_redirects=True)

# url.kr
# r = requests.get(url, allow_redirects=False)

def bitly(url):
    print('bitly')
    r = requests.get(url + '+')
    html = r.text
    # print(html)

    start = html.index('window.InfoPlus.start(')
    end = html.index('}', start)
    text = html[start + 23: end + 1]
    # print(text)
    json_ = json.loads(text)
    return {
        'statusCode': 200,
        'body': json.dumps([
            {
                'label': '제목',
                'data': json_['title']
            },
            {
                'label': '단축 url',
                'data': url
            },
            {
                'label': '복원 url',
                'data': json_['long_url']
            }
        ])
    }


def urlkr(url):
    print('urlkr')
    r = requests.get(url + '*', allow_redirects=False)
    html = r.text

    # print(html)

    soup = BeautifulSoup(html, 'html.parser')
    stat = soup.select_one('#short_stat')
    tr_list = stat.select('tr')
    long_url = tr_list[4].select('td')[1].text
    return {
        'statusCode': 200,
        'body': json.dumps([
            {
                'label': '단축 url',
                'data': url
            },
            {
                'label': '복원 url',
                'data': tr_list[4].select('td')[1].text
            },
            {
                'label': '누적 방문자수',
                'data': tr_list[1].select('td')[1].text
            },
            {
                'label': '오늘 방문자수',
                'data': tr_list[2].select('td')[1].text
            }
        ])
    }

def hangl(url):
    print('hangl')
    r = requests.get(url + '+')
    html = r.text
    # print(html)
    soup = BeautifulSoup(html, 'html.parser')
    url_info = soup.select_one('.url-info')
    a = url_info.select_one('a')
    title = a.text
    long_url = a.attrs['href']
    infinity_url_stats = soup.select_one('.infinity-url-stats')

    count = infinity_url_stats.select('.url-stats')[0].text
    count = count[: count.find('통')]
    count = count.replace('\r', '')
    count = count.replace('\n', '')
    count = count.replace('\t', '')

    return {
        'statusCode': 200,
        'body': json.dumps([
            {
                'label': '제목',
                'data': title
            },
            {
                'label': '단축 url',
                'data': url
            },
            {
                'label': '복원 url',
                'data': long_url
            },
            {
                'label': '방문자수',
                'data': count
            }
        ])
    }

def rbgy(url):
    print('rbgy')
    r = requests.get('https://app.rebrandly.com/public/links/share?href=' + url)
    html = r.text
    print(html)

    # soup = BeautifulSoup(html, 'html.parser')
    # url_info = soup.select_one('.url-info')
    # a = url_info.select_one('a')
    # title = a.text
    # long_url = a.attrs['href']
    # infinity_url_stats = soup.select_one('.infinity-url-stats')

    # count = infinity_url_stats.select('.url-stats')[0].text
    # count = count[: count.find('통')]
    # count = count.replace('\r', '')
    # count = count.replace('\n', '')
    # count = count.replace('\t', '')

    # return {
    #     'statusCode': 200,
    #     'body': json.dumps([
    #         {
    #             'label': '제목',
    #             'data': title
    #         },
    #         {
    #             'label': '단축 url',
    #             'data': url
    #         },
    #         {
    #             'label': '복원 url',
    #             'data': long_url
    #         },
    #         {
    #             'label': '방문자수',
    #             'data': count
    #         }
    #     ])
    # }

def main(event):
    try:
        # url = event.get('queryStringParameters', {}).get('url', '')
        url = event.get('url', '')

        if 'bit.ly' in url:
            return bitly(url)
        elif 'url.kr' in url:
            return urlkr(url)
        elif 'han.gl' in url:
            return hangl(url)
        elif 'rb.gy' in url:
            return rbgy(url)

        return

        print(url)
        # r = requests.get(url + '+')
        r = requests.get(url, allow_redirects=True )
        html = r.text
        print(html)
    except Exception as e:
        print(e)
        return {
            'statusCode': 400,
            'body': json.dumps({'error': e})
        }

# url = 'http://bit.ly/2Qod0RX'
# url = 'https://bit.ly/2MBojqk'


# 네이버
# url = 'https://bit.ly/3vNpkMv'
# url = 'https://url.kr/oe3tdy'
# url = 'https://han.gl/r69Es'
url = 'https://rb.gy/eexxhr'

# 쿠팡 리다이렉트
# url = 'https://bit.ly/3sxxjwP'  # -> 'https://coupa.ng/bPOXDQ' -> 쿠팡
# url = 'https://url.kr/xv5wo2' # -> 쿠팡 리다이렉트
# url = 'https://han.gl/yjyaE'

# url = 'https://coupa.ng/bPOXDQ'

event = {
    # 'url': 'https://bit.ly/2MBojqk'
    'url': url
}

r = main(event)
print(r)

