import os
import asyncio
from itertools import product
import aiohttp


connector = aiohttp.TCPConnector(share_cookies=True, verify_ssl=False)
sem = asyncio.Semaphore(20)


@asyncio.coroutine
def get_data(*args, **kwargs):
    response = yield from aiohttp.request('GET', *args, **kwargs)
    return (yield from response.text())


@asyncio.coroutine
def filter_data(url):

    try:
        with (yield from sem):
            body = yield from get_data(url, compress=True, connector=connector)
            # Do stuff with reponse body
    except:
        pass

    print(url)


def execution_time(fn):
    def time_diff():
        from datetime import datetime
        start = datetime.now()
        fn()
        d = datetime.now() - start
        print('Total time: ', d.total_seconds())

    return time_diff


def get_urls():
    return [
        'http://www.google.com',
        'http://www.facebook.com',
        'http://www.quora.com',
        'http://www.twitter.com',
        # more urls
    ]


@execution_time
def main():
    loop = asyncio.get_event_loop()
    url_list = get_urls()
    u = [filter_data(url) for url in url_list]
    c = asyncio.wait(u)
    loop.run_until_complete(c)


if __name__ == '__main__':
    main()
